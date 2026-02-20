import re

# Simple, explainable skill dictionary (edit anytime)
SKILLS = {
    "python", "java", "node.js", "javascript", "typescript",
    "spring", "spring boot", "django", "fastapi", "flask",
    "sql", "mysql", "postgresql", "mongodb", "redis",
    "docker", "kubernetes", "terraform", "ci/cd", "circleci", "bitbucket", "github actions",
    "aws", "azure", "gcp",
    "rest", "microservices",
    "nlp", "machine learning", "deep learning",
    "linux", "bash", "git",
}

def normalize(text: str) -> str:
    t = text.lower()
    t = t.replace("nodejs", "node.js")
    t = re.sub(r"\s+", " ", t).strip()
    return t

def extract_skills(text: str) -> set[str]:
    t = normalize(text)
    found: set[str] = set()
    for s in SKILLS:
        pattern = r"(^|[^a-z0-9])" + re.escape(s) + r"([^a-z0-9]|$)"
        if re.search(pattern, t):
            found.add(s)
    return found

def make_highlights(resume_text: str) -> list[str]:
    t = normalize(resume_text)
    highlights = []
    if "terraform" in t and ("circleci" in t or "bitbucket" in t):
        highlights.append("Hands-on Infrastructure-as-Code + CI/CD exposure (Terraform + pipelines).")
    if "kubernetes" in t and ("aws" in t or "azure" in t or "gcp" in t):
        highlights.append("Kubernetes + Cloud experience mentioned together (good for DevOps roles).")
    if "fastapi" in t or "django" in t or "spring boot" in t:
        highlights.append("Backend API framework experience present (FastAPI/Django/Spring Boot).")
    return highlights[:5]
