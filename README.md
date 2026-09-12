# Circular Carbon — Industrial Emission Leak-Point Detector & Circular Alternative Recommender

## Live URL : https://circular-carbon-frontend.onrender.com/

HackOut'26 | Theme: Circular Carbon Ecosystem

A production-ready platform where SMEs input process data (energy sources, raw materials, waste streams) and the system:
1. Identifies top emission sources (leak-points) with precise CO₂e calculation breakdown.
2. Retrieves and recommends specific circular interventions with estimated cost & CO₂ reduction using RAG + Google Gemini LLM.

---

## Tech Stack
- **Backend**: Spring Boot 3 (Java 21), Maven — Emission calculation engine, JPA, OpenAPI REST API
- **RAG Service**: Python FastAPI — Vector retrieval with pgvector & LangChain Google GenAI (Gemini)
- **Database**: PostgreSQL 16 + pgvector — Relational emission factors + 768-dim vector embeddings
- **Frontend**: React 19 + Vite + TypeScript + Tailwind CSS + Recharts — Responsive analytics dashboard

---

## Quick Start (Docker Compose)

The entire full stack (database, RAG service, backend, frontend) is containerized and runs with a single command:

```bash
# 1. (Optional) Copy environment variables template and add your Gemini API key:
cp .env.example .env

# 2. Build and start all services:
docker-compose up -d --build
```

### Access Services:
- **Frontend App**: `http://localhost` (or `http://localhost:5173` in local dev)
- **Backend API & Swagger Docs**: `http://localhost:8080/swagger-ui`
- **RAG Recommendation Service**: `http://localhost:8000/docs`
- **PostgreSQL + pgvector**: `localhost:5433` (DB: `circular_carbon`, User: `postgres`)

---

## Local Development (Without Docker)

1. **Start Database**:
   ```bash
   docker-compose up -d postgres
   ```
2. **Start RAG Service**:
   ```bash
   cd rag-service
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```
3. **Start Backend**:
   ```bash
   cd backend
   mvn spring-boot:run
   ```
4. **Start Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

---

## Environment Variables

See `.env.example` for the complete list of configurable variables:
- `GOOGLE_API_KEY` / `GEMINI_API_KEY`: API key for Gemini LLM recommendations & embeddings.
- `DB_URL` / `DATABASE_URL`: PostgreSQL JDBC and Python database URLs.
- `RAG_SERVICE_URL`: URL where the backend connects to the Python RAG service.
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins.
- `VITE_API_BASE_URL`: API base URL for the frontend.
