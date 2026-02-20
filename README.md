# AI Resume Screening & Job Matching Platform

A production-style project that:
- Extracts resume text from PDF
- Uses NLP skill matching + embedding similarity
- Returns match score + missing skills
- Stores analysis history in PostgreSQL
- Runs with Docker Compose

## Tech
- FastAPI, SQLAlchemy, PostgreSQL
- Sentence Transformers embeddings (all-MiniLM-L6-v2)
- pdfplumber for PDF parsing
- Streamlit UI (optional)

## Run locally (Docker)
1) Copy env
   cp .env.example .env

2) Start
   docker compose up --build

3) API Docs
   http://localhost:8000/docs
   Health: http://localhost:8000/health

## Run Streamlit UI
In another terminal:
cd frontend
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
streamlit run streamlit_app.py

## Key endpoints
- POST /analyze (PDF + JD) -> score + matched/missing skills
- POST /jobs, GET /jobs
- GET /analyses

## Next steps (nice upgrades)
- Auth (JWT) + RBAC for HR/Admin
- Alembic migrations
- Vector DB (pgvector) for large-scale matching
- Async processing (Celery/RQ) for heavy PDFs
