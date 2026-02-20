from sqlalchemy.orm import Session
from . import models, schemas

def create_job(db: Session, job: schemas.JobCreate) -> models.Job:
    obj = models.Job(title=job.title, description=job.description)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_jobs(db: Session, limit: int = 50) -> list[models.Job]:
    return db.query(models.Job).order_by(models.Job.id.desc()).limit(limit).all()

def get_job(db: Session, job_id: int) -> models.Job | None:
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def save_analysis(db: Session, job_id: int | None, candidate_name: str | None, score: float, missing_skills: list[str]) -> models.Analysis:
    obj = models.Analysis(
        job_id=job_id,
        candidate_name=candidate_name,
        score=float(score),
        missing_skills_csv=",".join(missing_skills),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_analyses(db: Session, limit: int = 50) -> list[models.Analysis]:
    return db.query(models.Analysis).order_by(models.Analysis.id.desc()).limit(limit).all()
