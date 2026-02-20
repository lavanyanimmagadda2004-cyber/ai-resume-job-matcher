import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Matcher", layout="centered")

API_URL = st.sidebar.text_input("API URL", "http://localhost:8000")

st.title("AI Resume Screening & Job Matching")
st.write("Upload a resume PDF + paste a Job Description. Get match score and missing skills.")

pdf = st.file_uploader("Resume PDF", type=["pdf"])
jd = st.text_area("Job Description", height=220)
name = st.text_input("Candidate Name (optional)")

if st.button("Analyze"):
    if not pdf or not jd.strip():
        st.error("Please upload PDF and paste JD.")
    else:
        files = {"resume_pdf": (pdf.name, pdf.getvalue(), "application/pdf")}
        data = {"jd_text": jd, "candidate_name": name}
        r = requests.post(f"{API_URL}/analyze", files=files, data=data, timeout=120)
        if r.status_code != 200:
            st.error(r.text)
        else:
            out = r.json()
            st.metric("Match Score (%)", out["score"])
            st.subheader("Matched Skills")
            st.write(out["matched_skills"])
            st.subheader("Missing Skills")
            st.write(out["missing_skills"])
            st.subheader("Highlights")
            st.write(out["highlights"])
            st.subheader("Notes")
            st.write(out["notes"])
