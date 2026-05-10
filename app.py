import streamlit as st
import PyPDF2
import re
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')

from sentence_transformers import SentenceTransformer, util

import pandas as pd

# Download tokenizer once
nltk.download('punkt')

# Load embedding model once
model = SentenceTransformer('all-MiniLM-L6-v2')


# ---------------- PDF TEXT EXTRACTION ---------------- #

def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF."""
    reader = PyPDF2.PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


# ---------------- TEXT CLEANING ---------------- #

def clean_text(text):
    """Basic cleanup without destroying semantic meaning."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ---------------- CHUNKING LOGIC ---------------- #

def extract_resume_chunks(text):
    """
    Extract meaningful resume chunks.
    Uses:
    - bullet points
    - line splitting
    - sentence splitting
    """

    chunks = []

    # Split by newlines first
    lines = text.split('\n')

    for line in lines:

        line = line.strip()

        # Ignore very short junk
        if len(line) < 20:
            continue

        # Split long paragraphs into sentences
        sentences = nltk.sent_tokenize(line)

        for sentence in sentences:

            sentence = sentence.strip()

            if len(sentence) > 20:
                chunks.append(sentence)

    return chunks


def extract_jd_chunks(text):
    """
    Extract job description requirements.
    """

    chunks = []

    sentences = nltk.sent_tokenize(text)

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) > 20:
            chunks.append(sentence)

    return chunks


# ---------------- SEMANTIC MATCHING ---------------- #

def semantic_match(resume_text, job_desc):

    resume_chunks = extract_resume_chunks(resume_text)
    jd_chunks = extract_jd_chunks(job_desc)

    if not resume_chunks or not jd_chunks:
        return 0, [], []

    # Encode chunks once
    resume_embeddings = model.encode(
        resume_chunks,
        convert_to_tensor=True
    )

    jd_embeddings = model.encode(
        jd_chunks,
        convert_to_tensor=True
    )

    matched = []
    missing = []

    similarity_scores = []

    # Compare every JD chunk against resume
    for i, jd_chunk in enumerate(jd_chunks):

        similarities = util.pytorch_cos_sim(
            jd_embeddings[i],
            resume_embeddings
        )[0]

        best_score = similarities.max().item()

        similarity_scores.append(best_score)

        best_match_idx = similarities.argmax().item()

        # Threshold tuning
        if best_score >= 0.55:

            matched.append({
                "requirement": jd_chunk,
                "resume_match": resume_chunks[best_match_idx],
                "score": round(best_score * 100, 2)
            })

        else:

            missing.append({
                "requirement": jd_chunk,
                "score": round(best_score * 100, 2)
            })

    # Final resume score
    final_score = int(
        (sum(similarity_scores) / len(similarity_scores)) * 100
    )

    return final_score, matched, missing

def generate_suggestion(requirement):

    req = requirement.lower()

    # Backend
    if any(word in req for word in [
        "api", "backend", "express", "node", "server"
    ]):
        return (
            "Build backend projects with REST APIs and highlight "
            "database integration or authentication features."
        )

    # Frontend
    elif any(word in req for word in [
        "react", "frontend", "javascript", "ui", "css"
    ]):
        return (
            "Add frontend projects demonstrating responsive UI design "
            "and component-based development."
        )

    # Machine Learning
    elif any(word in req for word in [
        "machine learning", "tensorflow", "pytorch",
        "deep learning", "ai", "data science"
    ]):
        return (
            "Include ML projects with datasets, model evaluation metrics, "
            "and deployment or visualization components."
        )

    # SQL / Database
    elif any(word in req for word in [
        "sql", "mysql", "postgresql", "database", "mongodb"
    ]):
        return (
            "Mention database-related work involving schema design, "
            "queries, or full-stack data handling."
        )

    # Cloud / DevOps
    elif any(word in req for word in [
        "docker", "aws", "kubernetes", "cloud", "devops"
    ]):
        return (
            "Add deployment experience using cloud or containerization "
            "tools in your projects."
        )

    # Communication / Teamwork
    elif any(word in req for word in [
        "communication", "teamwork", "collaboration", "leadership"
    ]):
        return (
            "Highlight collaborative projects, leadership roles, "
            "or presentations demonstrating soft skills."
        )

    # Generic fallback
    else:
        return (
            "Strengthen your resume by adding measurable achievements, "
            "relevant projects, or practical experience related to this requirement."
        )


# ---------------- STREAMLIT UI ---------------- #

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)

st.title("📄 AI Resume Analyzer")
st.write("Semantic Resume Matching using Sentence Transformers 🚀")

uploaded_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

job_desc = st.text_area(
    "Paste the job description here:",
    height=250
)

if st.button("MATCH"):

    if uploaded_file is not None and job_desc:

        with st.spinner("Analyzing Resume..."):

            # Extract resume text
            resume_text = extract_text_from_pdf(uploaded_file)

            # Clean text
            resume_text = clean_text(resume_text)
            job_desc = clean_text(job_desc)

            # Semantic matching
            score, matched, missing = semantic_match(
                resume_text,
                job_desc
            )

            # ---------------- RESULTS ---------------- #

            st.subheader("✅ Resume Match Score")

            st.metric(
                label="Match Score",
                value=f"{score}%"
            )

            # Feedback
            if score >= 75:
                st.success("🎉 Strong match for this role!")

            elif score >= 55:
                st.warning("⚠️ Moderate match. Some improvements recommended.")

            else:
                st.error("❌ Low match. Resume needs significant improvement.")

            # ---------------- MATCHED ---------------- #

            st.subheader("✅ Matched Requirements")

            if matched:

                matched_data = []

                for item in matched[:10]:

                    matched_data.append({
                        "Job Requirement": item['requirement'],
                        "Matched Resume Content": item['resume_match'],
                        "Similarity Score": f"{item['score']}%"
                    })

                matched_df = pd.DataFrame(matched_data)

                st.table(
                    matched_df.style.set_properties(
                        **{
                            'white-space': 'pre-wrap',
                            'word-wrap': 'break-word'
                        }
                    )
                )

            else:
                st.write("No strong semantic matches found.")

            # ---------------- MISSING ---------------- #

            st.subheader("❌ Weak Areas / Missing Requirements")

            if missing:

                weak_data = []

                for item in missing[:10]:

                    suggestion = generate_suggestion(item['requirement'])
                    weak_data.append({
                        "Missing Requirement": item['requirement'],
                        "Suggested Improvement": suggestion,
                        "Match Confidence": f"{item['score']}%"
                    })

                weak_df = pd.DataFrame(weak_data)

                st.table(
                    weak_df.style.set_properties(
                        **{
                            'white-space': 'pre-wrap',
                            'word-wrap': 'break-word'
                        }
                    )
                )

            else:
                st.success("No major missing requirements detected!")

    else:
        st.warning(
            "Please upload your resume and paste the job description."
        )