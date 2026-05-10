# AI Resume Analyzer

An AI-powered resume analysis tool that evaluates how well a resume matches a job description using semantic similarity and Natural Language Processing (NLP).

Built with Python, Streamlit, and Sentence Transformers, the application provides recruiter-style analysis including match scoring, semantic requirement matching, weak area detection, and intelligent improvement suggestions.

---

# Features

* Upload resumes in PDF format
* Semantic similarity matching using Sentence Transformers
* Resume-job description match scoring
* Detection of semantically matched requirements
* Identification of weak or missing areas
* Intelligent resume improvement suggestions
* Structured recruiter-style analysis tables
* Interactive Streamlit web interface

---

# Tech Stack

| Technology            | Purpose                        |
| --------------------- | ------------------------------ |
| Python                | Core Programming Language      |
| Streamlit             | Web Application Framework      |
| Sentence Transformers | Semantic Embedding Generation  |
| PyTorch               | Backend for Transformer Models |
| Pandas                | Structured Data Handling       |
| PyPDF2                | PDF Text Extraction            |
| Regex + NLP           | Resume Parsing & Processing    |

---

# How It Works

1. The user uploads a resume in PDF format
2. The application extracts and cleans the resume text
3. Both the resume and job description are split into meaningful chunks
4. Sentence embeddings are generated using the `all-MiniLM-L6-v2` model
5. Semantic similarity is calculated between job requirements and resume content
6. The system:

   * calculates an overall match score
   * identifies matching requirements
   * detects weak areas
   * generates improvement suggestions

---

# Installation & Setup

## Clone the Repository

```bash
git clone https://github.com/saina25/AI-Resume-Analyser.git
cd AI-Resume-Analyser
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

---

# Project Structure

```text
AI-Resume-Analyser/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/
```

---

# Example Output

The application provides:

* Resume Match Score
* Matched Requirements Table
* Weak Areas Table
* Suggested Resume Improvements

---

# Future Improvements

* ATS compatibility analysis
* Resume section-wise scoring
* Downloadable PDF reports
* Skill visualization dashboard
* Multi-role analysis support

