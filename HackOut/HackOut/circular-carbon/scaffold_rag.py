import os
import json

base_dir = r"c:\Users\Anuj\Desktop\HackOut\circular-carbon"

def write_file(path, content):
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# --- 1. RAG SERVICE ---
write_file("rag-service/requirements.txt", """
fastapi==0.110.0
uvicorn==0.27.1
psycopg2-binary==2.9.9
pgvector==0.2.5
langchain-google-genai==1.0.1
python-dotenv==1.0.1
pydantic==2.6.4
httpx==0.27.0
""")

write_file("data/interventions.json", json.dumps([
    {
        "id": "INT-001", "title": "Switch from Coal to Biomass for Process Heat", "category": "ENERGY", "applicable_industries": ["Steel", "Cement", "Food Processing"],
        "description": "Replacing coal-fired boilers with biomass (agricultural residue, wood pellets) for process heat generation.",
        "co2_reduction_percent": "40-60%", "estimated_cost_savings": "10-25% reduction in fuel costs after initial investment", "implementation_complexity": "Medium", "payback_period": "2-4 years"
    },
    {
        "id": "INT-002", "title": "Implement Closed-Loop Water & Heat Recovery", "category": "ENERGY", "applicable_industries": ["Textile", "Food Processing", "Chemical"],
        "description": "Capture waste heat from exhaust gases and wastewater to preheat incoming water or air.",
        "co2_reduction_percent": "15-30%", "estimated_cost_savings": "20% reduction in heating costs", "implementation_complexity": "High", "payback_period": "3-5 years"
    },
    {
        "id": "INT-003", "title": "Use Recycled Scrap Steel (Electric Arc Furnace)", "category": "MATERIAL", "applicable_industries": ["Steel", "Automotive", "Manufacturing"],
        "description": "Increase the proportion of recycled steel scrap in production using EAF instead of blast furnaces.",
        "co2_reduction_percent": "70%", "estimated_cost_savings": "Varies by scrap price, typically cost-neutral or slight savings", "implementation_complexity": "High", "payback_period": "5+ years"
    },
    {
        "id": "INT-004", "title": "Industrial Symbiosis: Waste to Raw Material", "category": "WASTE", "applicable_industries": ["Chemical", "Cement", "Agriculture"],
        "description": "Sell or exchange industrial by-products (e.g., slag, fly ash, chemical waste) to be used as raw materials in other industries like cement or agriculture.",
        "co2_reduction_percent": "100% of waste emission", "estimated_cost_savings": "Converts waste disposal cost into a revenue stream", "implementation_complexity": "Medium", "payback_period": "1-2 years"
    },
    {
        "id": "INT-005", "title": "Optimize Logistics with Route Planning and EV Fleet", "category": "TRANSPORT", "applicable_industries": ["All"],
        "description": "Transition internal and local delivery fleets to electric vehicles and use AI-driven route optimization.",
        "co2_reduction_percent": "30-50%", "estimated_cost_savings": "15% in fuel and maintenance", "implementation_complexity": "Medium", "payback_period": "3-5 years"
    }
], indent=2))

write_file("rag-service/main.py", """
import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import psycopg2
from pgvector.psycopg2 import register_vector
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

load_dotenv()
app = FastAPI()

DB_URL = "postgresql://postgres:postgres@localhost:5432/circular_carbon"

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
    conn = psycopg2.connect(DB_URL)
    register_vector(conn)
    return conn

@app.on_event("startup")
def startup_event():
    # Initialize DB and seed embeddings if empty
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
    if cur.fetchone()[0] == 0:
        print("Seeding embeddings...")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        with open("../data/interventions.json") as f:
            data = json.load(f)
        for item in data:
            content = json.dumps(item)
            vec = embeddings.embed_query(item['title'] + " " + item['description'])
            cur.execute(
                "INSERT INTO intervention_embeddings (id, title, category, content, embedding) VALUES (%s, %s, %s, %s, %s)",
                (item['id'], item['title'], item['category'], content, vec)
            )
        conn.commit()
    cur.close()
    conn.close()

@app.post("/api/recommend")
def recommend(req: RecommendRequest):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        retrieved_contexts = []
        for source in req.top_emissions:
            query = f"{source.category} emission reduction for {source.item_name} in {req.industry_type} industry"
            vec = embeddings.embed_query(query)
            # Find top 2 similar interventions
            cur.execute('''
                SELECT content FROM intervention_embeddings 
                ORDER BY embedding <-> %s::vector LIMIT 2
            ''', (vec,))
            for row in cur.fetchall():
                if row[0] not in retrieved_contexts:
                    retrieved_contexts.append(row[0])
                    
        cur.close()
        conn.close()

        prompt = f'''
        You are a sustainability consultant. A {req.industry_type} company named {req.company_name} has a total carbon footprint of {req.total_co2e} kg CO2e.
        Their top emissions are:
        {json.dumps([s.dict() for s in req.top_emissions], indent=2)}
        
        Based on these retrieved circular economy interventions:
        {json.dumps(retrieved_contexts, indent=2)}
        
        Suggest 2-3 specific, actionable recommendations for this company to reduce their footprint.
        Output ONLY a JSON array of objects with keys: "title", "description", "estimated_co2_reduction", "cost_impact", "implementation_steps", "justification".
        Do not include markdown blocks like ```json.
        '''
        
        response = llm.invoke(prompt)
        text = response.content.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
""")

print("RAG Service scaffolded.")
