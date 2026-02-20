from pydantic import BaseModel, Field
from typing import List, Optional

class JobCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str = Field(min_length=10)

class JobOut(BaseModel):
    id: int
    title: str
    description: str
    class Config:
        from_attributes = True

class AnalyzeResponse(BaseModel):
    score: float
    matched_skills: List[str]
    missing_skills: List[str]
    highlights: List[str]
    notes: List[str]

class AnalysisOut(BaseModel):
    id: int
    job_id: Optional[int]
    candidate_name: Optional[str]
    score: float
    missing_skills_csv: str
    class Config:
        from_attributes = True
