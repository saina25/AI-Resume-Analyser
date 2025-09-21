# 📄 AI Resume Analyzer

A simple yet powerful Streamlit application designed to help you tailor your resume to a specific job description. This tool calculates a match score, highlights matching keywords, and identifies important keywords you might be missing.

## 📂 Project Structure

```
.
├── app.py                  # Main Streamlit application script
├── requirements.txt        # Python dependencies
├── demo_resumes/           # Folder with sample resumes for testing
│   ├── Software_Engineer_Resume.pdf
│   ├── Project_Manager_Resume.pdf
│   └── Data_Analyst_Resume.pdf
└── README.md
```

## ✨ Features

  - **PDF Resume Upload**: Easily upload your resume in `.pdf` format.
  - **Job Description Input**: Paste any job description into a text area.
  - **Instant Match Score**: Get a percentage score showing how well your resume matches the job description.
  - **Keyword Analysis**:
      - See which keywords from the job description are present in your resume.
      - Identify crucial keywords that are missing from your resume.
  - **Actionable Feedback**: Receive a simple success or warning message based on your score.

-----

## 🚀 How It Works

The application follows a simple workflow:

1.  **Text Extraction**: The text is extracted from the uploaded PDF resume using the `PyPDF2` library.
2.  **Text Cleaning**: Both the resume text and the job description are cleaned by converting them to lowercase and removing extra whitespace. This ensures the comparison is accurate.
3.  **Scoring Algorithm**: The core logic compares the set of unique words in your resume against the set of unique words in the job description. The score is calculated as:
    $$\text{Score} = \left( \frac{\text{Number of Matched Keywords}}{\text{Total Number of Keywords in Job Description}} \right) \times 100$$
4.  **Keyword Identification**:
      - **Matched Keywords**: The intersection of words between your resume and the job description.
      - **Missing Keywords**: The words present in the job description but not in your resume.

-----

## 🛠️ Setup and Installation

To run this application on your local machine, please follow these steps.

### Prerequisites

  - Python 3.7+

### 1\. Clone the Repository

```bash
git clone https://github.com/saina25/AI-Resume-Analyser.git
cd AI-Resume-Analyser
```

### 2\. Install Dependencies

Install all the necessary packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 3\. Run the Application

Once the dependencies are installed, you can start the Streamlit server:

```bash
streamlit run app.py
```

Your web browser should automatically open with the application running.

-----

## 📝 How to Use

1.  **Run the app** using the command `streamlit run app.py`.
2.  **Upload Resume**: Click on the "Browse files" button to upload your resume.
      - *You can use one of the sample resumes located in the `/demo_resumes` folder to test the application.*
3.  **Paste Job Description**: Copy a job description you are interested in and paste it into the text area.
4.  **View Results**: The app will automatically calculate and display:
      - Your resume match score.
      - A list of matched keywords.
      - A list of missing keywords to consider adding to your resume.
