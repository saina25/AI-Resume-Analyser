import streamlit as st
import PyPDF2
import re

def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file."""
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def clean_text(text):
    """Basic cleanup for text."""
    return re.sub(r'\s+', ' ', text).strip().lower()

def calculate_resume_score(resume_text, job_desc):
    """Compare resume with job description and give score + missing keywords."""
    resume_words = set(resume_text.split())
    jd_words = set(job_desc.split())

    matched = resume_words.intersection(jd_words)
    missing = jd_words.difference(resume_words)

    score = int((len(matched) / len(jd_words)) * 100) if len(jd_words) > 0 else 0
    return score, matched, missing


st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and paste a job description to see how well you match!")


uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste the job description here:")

if uploaded_file and job_desc:
    resume_text = extract_text_from_pdf(uploaded_file)
    resume_text = clean_text(resume_text)
    job_desc = clean_text(job_desc)

    score, matched, missing = calculate_resume_score(resume_text, job_desc)

    st.subheader("✅ Results")
    st.write(f"**Resume Match Score:** {score}%")

    st.write("**Matched Keywords:**")
    st.write(", ".join(list(matched)[:20]))

    st.write("**Missing Keywords:**")
    st.write(", ".join(list(missing)[:20]))

    if score < 60:
        st.warning("⚠️ Your resume could use some improvement to better match this job description!")
    else:
        st.success("🎉 Great! Your resume matches well with this job description.")

