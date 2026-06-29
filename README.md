# AI Resume Screening & Candidate Ranking System

An automated screening application that matches candidate resumes (PDF/TXT) against a job description using Natural Language Processing (NLP), TF-IDF feature extraction, and Cosine Similarity scoring.

## 🚀 Live Demo Links
* **Frontend Dashboard:** [Paste your Streamlit Cloud Link Here]
* **Backend API:** [Paste your Render API Link Here]

## 📂 Project Structure
* `app_backend.py`: FastAPI server handling PDF text extraction, TF-IDF vectorization, and scoring math.
* `app_frontend.py`: Streamlit user interface allowing job description input and multi-file resume uploads.
* `Capstone_Notebook.ipynb`: Jupyter notebook containing initial data exploration and pipeline prototyping.

## 🛠️ Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/deepanshumudgal22-droid/AI-Resume-Screener]
   cd AI-Resume-Screener

2.**Install the dependencies:**
 
 pip install -r requirements.txt

3.**Run the Backend API:**
 
  uvicorn app_backend:app --reload

4.**Run the Frontend UI (Open a new terminal):**
  
  streamlit run app_frontend.py 
