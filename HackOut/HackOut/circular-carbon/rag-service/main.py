import os
import json
import re
import hashlib
import numpy as np
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import psycopg2
    # pyrefly: ignore [missing-import]
    from pgvector.psycopg2 import register_vector
    PG_AVAILABLE = True
except ImportError:
    psycopg2 = None
    register_vector = None
    PG_AVAILABLE = False

app = FastAPI(title="Circular Carbon RAG Service")

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5433/circular_carbon")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

class EmissionSource(BaseModel):
    item_name: str
    category: str
    co2e: float
    percentage: float

class RecommendRequest(BaseModel):
    company_name: str
    industry_type: str
    top_emissions: List[EmissionSource]
    total_co2e: float

class Recommendation(BaseModel):
    title: str
    description: str
    estimated_co2_reduction: str
    cost_impact: str
    implementation_steps: str
    justification: str

def get_db_connection():
    if not PG_AVAILABLE or psycopg2 is None:
        raise RuntimeError("psycopg2 or pgvector library is not installed in the current environment")
    conn = psycopg2.connect(DB_URL)
    if register_vector:
        register_vector(conn)
    return conn

def find_interventions_file() -> Path:
    env_path = os.getenv("INTERVENTIONS_FILE_PATH")
    if env_path and Path(env_path).is_file():
        return Path(env_path)
    
    current_dir = Path(__file__).resolve().parent
    candidates = [
        current_dir.parent / "data" / "interventions.json",
        current_dir / "data" / "interventions.json",
        current_dir / "interventions.json",
        Path("/app/data/interventions.json"),
        Path("/data/interventions.json")
    ]
    for p in candidates:
        if p.is_file():
            return p
    return candidates[0]

def generate_fallback_embedding(text: str, dim: int = 768) -> List[float]:
    """Generates a deterministic 768-dim normalized embedding for similarity search when offline/no API key."""
    tokens = re.findall(r"\w+", text.lower())
    vec = np.zeros(dim, dtype=np.float32)
    for token in tokens:
        idx = int(hashlib.md5(token.encode('utf-8')).hexdigest(), 16) % dim
        vec[idx] += 1.0
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()

def get_embedding(text: str) -> List[float]:
    if GOOGLE_API_KEY:
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/text-embedding-004",
                google_api_key=GOOGLE_API_KEY
            )
            return embeddings.embed_query(text)
        except Exception as e:
            print(f"Warning: Gemini embedding failed ({e}), using fallback embedding.")
    return generate_fallback_embedding(text)

@app.on_event("startup")
def startup_event():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS intervention_embeddings (
                id TEXT PRIMARY KEY,
                title TEXT,
                category TEXT,
                content TEXT,
                embedding vector(768)
            )
        ''')
        cur.execute("SELECT COUNT(*) FROM intervention_embeddings")
        count = cur.fetchone()[0]
        if count == 0:
            interventions_path = find_interventions_file()
            print(f"Seeding intervention embeddings from {interventions_path}...")
            if interventions_path.is_file():
                with open(interventions_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in data:
                    content = json.dumps(item)
                    text_to_embed = f"{item.get('title', '')} {item.get('category', '')} {item.get('description', '')} {' '.join(item.get('applicable_industries', []))}"
                    vec = get_embedding(text_to_embed)
                    cur.execute(
                        "INSERT INTO intervention_embeddings (id, title, category, content, embedding) VALUES (%s, %s, %s, %s, %s)",
                        (item['id'], item['title'], item['category'], content, vec)
                    )
                conn.commit()
                print("Interventions seeded successfully.")
            else:
                print(f"Warning: Interventions file not found at {interventions_path}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Notice: Startup database initialization deferred ({e})")

@app.post("/api/recommend", response_model=List[Recommendation])
def recommend(req: RecommendRequest):
    try:
        retrieved_contexts = []
        retrieved_ids = set()
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            for source in req.top_emissions:
                query = f"{source.category} {source.item_name} emission reduction circular economy {req.industry_type}"
                vec = get_embedding(query)
                
                cur.execute('''
                    SELECT id, content FROM intervention_embeddings 
                    ORDER BY embedding <-> %s::vector LIMIT 2
                ''', (vec,))
                
                for row in cur.fetchall():
                    item_id, content = row[0], row[1]
                    if item_id not in retrieved_ids:
                        retrieved_ids.add(item_id)
                        retrieved_contexts.append(json.loads(content))
                        
            cur.close()
            conn.close()
        except Exception as db_err:
            print(f"Database query notice ({db_err}), using in-memory retrieval.")

        # If no contexts found from DB query, fallback to rank from interventions.json
        if not retrieved_contexts:
            interventions_path = find_interventions_file()
            if interventions_path.is_file():
                with open(interventions_path, "r", encoding="utf-8") as f:
                    all_interventions = json.load(f)
                
                scored = []
                for item in all_interventions:
                    item_text = f"{item.get('title', '')} {item.get('category', '')} {item.get('description', '')} {' '.join(item.get('applicable_industries', []))}"
                    item_vec = np.array(get_embedding(item_text))
                    
                    max_sim = -1.0
                    for source in req.top_emissions:
                        query_vec = np.array(get_embedding(f"{source.category} {source.item_name} {req.industry_type}"))
                        sim = float(np.dot(item_vec, query_vec) / (np.linalg.norm(item_vec) * np.linalg.norm(query_vec) + 1e-9))
                        if sim > max_sim:
                            max_sim = sim
                    scored.append((max_sim, item))
                
                scored.sort(key=lambda x: x[0], reverse=True)
                retrieved_contexts = [x[1] for x in scored[:3]]

        # Try real LLM recommendation first if GOOGLE_API_KEY is available
        if GOOGLE_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GOOGLE_API_KEY)
                
                prompt = f"""
You are an expert industrial sustainability and circular economy consultant.
Analyze the following company profile and emission breakdown to recommend the top 2-3 highest-impact circular economy interventions.

Company Profile:
- Company Name: {req.company_name}
- Industry: {req.industry_type}
- Total Carbon Footprint: {req.total_co2e:,.2f} kg CO2e

Top Emission Breakdown:
{json.dumps([s.model_dump() for s in req.top_emissions], indent=2)}

Retrieved Circular Interventions Knowledge:
{json.dumps(retrieved_contexts, indent=2)}

Instructions:
1. Provide 2-3 specific, actionable recommendations directly aligned with their top emission leak-points and industry.
2. Return ONLY a valid JSON array of objects conforming to this schema:
[
  {{
    "title": "Clear action title",
    "description": "Detailed explanation of the circular intervention and technology",
    "estimated_co2_reduction": "e.g. 35-50% reduction in category emissions",
    "cost_impact": "e.g. Initial capex with 2-3 yr ROI / 15% operational savings",
    "implementation_steps": "1. Conduct site audit... 2. Procure and integrate... 3. Measure savings...",
    "justification": "Why this specific intervention addresses their major emission sources"
  }}
]
Do not include any markdown formatting such as ```json or ```. Return plain JSON only.
"""
                for model_name in ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-2.5-flash"]:
                    try:
                        model = genai.GenerativeModel(model_name)
                        response = model.generate_content(prompt)
                        raw_text = response.text.strip()
                        cleaned_text = re.sub(r"^```json\s*", "", raw_text, flags=re.IGNORECASE)
                        cleaned_text = re.sub(r"^```\s*", "", cleaned_text)
                        cleaned_text = re.sub(r"\s*```$", "", cleaned_text)
                        
                        parsed = json.loads(cleaned_text.strip())
                        if isinstance(parsed, list) and len(parsed) > 0:
                            return parsed
                    except Exception as model_err:
                        print(f"Model {model_name} failed: {model_err}")
                        continue
            except Exception as llm_err:
                print(f"LLM generation failed ({llm_err}), utilizing structured fallback engine.")

        # Graceful, high-quality fallback recommendation engine
        results = []
        for i, ctx in enumerate(retrieved_contexts[:3]):
            matching_source = req.top_emissions[i % len(req.top_emissions)] if req.top_emissions else None
            source_name = matching_source.item_name if matching_source else "Process Energy"
            source_pct = f"{matching_source.percentage:.1f}%" if matching_source else "primary"
            
            results.append({
                "title": ctx.get("title", f"Circular Intervention for {source_name}"),
                "description": ctx.get("description", "Deploy closed-loop resource recovery and circular material substitution."),
                "estimated_co2_reduction": ctx.get("co2_reduction_percent", "25-45%"),
                "cost_impact": ctx.get("estimated_cost_savings", "10-20% operational cost savings"),
                "implementation_steps": f"1. Audit {source_name} consumption and leak points in {req.industry_type} process. 2. Integrate {ctx.get('title', 'circular technology')} into production workflow. 3. Monitor efficiency and verify CO2e reductions against baseline.",
                "justification": f"Directly targets {source_name} ({source_pct} of total emissions) in {req.company_name}'s {req.industry_type} facility to maximize decarbonization ROI."
            })
            
        return results

    except Exception as e:
        print(f"Error in recommend endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
