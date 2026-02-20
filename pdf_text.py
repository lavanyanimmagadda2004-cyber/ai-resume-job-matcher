import pdfplumber

def extract_text_from_pdf(pdf_bytes: bytes, max_chars: int = 120000) -> str:
    text_parts: list[str] = []
    with pdfplumber.open(io=pdf_bytes) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            if t.strip():
                text_parts.append(t)
            joined = "\n".join(text_parts)
            if len(joined) >= max_chars:
                return joined[:max_chars]
    joined = "\n".join(text_parts).strip()
    return joined[:max_chars]
