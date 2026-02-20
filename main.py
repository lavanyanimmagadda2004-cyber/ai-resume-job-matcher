import os
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import schemas, crud
from .services.pdf_text import extract_text_from_pdf
from .services.skill_extract import extract_skills, make_highlights
from .services.similarity import SimilarityEngine

MAX_TEXT_CHARS = int(os.getenv("MAX_TEXT_CHARS", "120000"))
MODEL_NAME = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

app = FastAPI(title="AI Resume Screening & Job Matcher", version="1.0.0")

Base.metadata.create_all(bind=engine)

engine_sim = SimilarityEngine(MODEL_NAME)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/jobs", response_model=schemas.JobOut)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db, job)

@app.get("/jobs", response_model=list[schemas.JobOut])
def list_jobs(db: Session = Depends(get_db), limit: int = 50):
    return crud.list_jobs(db, limit=limit)

@app.post("/analyze", response_model=schemas.AnalyzeResponse)
async def analyze_resume(
    resume_pdf: UploadFile = File(...),
    jd_text: str = Form(...),
    candidate_name: str | None = Form(None),
    job_id: int | None = Form(None),
    db: Session = Depends(get_db),
):
    if resume_pdf.content_type not in ("application/pdf", "application/octet-stream"):
        raise HTTPException(status_code=400, detail="Please upload a PDF resume.")

    pdf_bytes = await resume_pdf.read()
    resume_text = extract_text_from_pdf(pdf_bytes, max_chars=MAX_TEXT_CHARS)

    if not resume_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF (try another resume PDF).")

    jd_text = jd_text.strip()
    if len(jd_text) < 30:
        raise HTTPException(status_code=400, detail="Job description text is too short.")

    if job_id is not None:
        job = crud.get_job(db, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="job_id not found")
        jd_text = job.description

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    matched = sorted(list(resume_skills.intersection(jd_skills)))
    missing = sorted(list(jd_skills.difference(resume_skills)))

    sim = engine_sim.score(resume_text, jd_text)
    score_percent = round(sim * 100, 2)

    crud.save_analysis(db, job_id=job_id, candidate_name=candidate_name, score=score_percent, missing_skills=missing)

    notes = []
    if len(matched) == 0 and len(jd_skills) > 0:
        notes.append("No keyword-skill overlap detected; similarity score still uses embeddings, but add explicit skill keywords in resume.")
    if len(missing) > 8:
        notes.append("Many JD skills missing; prioritize top 5 and update resume/projects accordingly.")

    return schemas.AnalyzeResponse(
        score=score_percent,
        matched_skills=matched,
        missing_skills=missing,
        highlights=make_highlights(resume_text),
        notes=notes,
    )

@app.get("/analyses", response_model=list[schemas.AnalysisOut])
def list_analyses(db: Session = Depends(get_db), limit: int = 50):
    return crud.list_analyses(db, limit=limit)
