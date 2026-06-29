from fastapi import FastAPI, Form, UploadFile, File
from typing import List
import re
import io
import numpy as np
import pandas as pd
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# 1. Cleaning Function
def simple_clean(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# 2. PDF Text Extraction Function
def extract_text_from_pdf(file_bytes):
    # Wrap the raw file bytes in an in-memory stream so PdfReader can read it
    pdf_stream = io.BytesIO(file_bytes)
    reader = PdfReader(pdf_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# 3. Core Ranking API Endpoint
@app.post("/rank")
async def rank_candidates(job_description: str = Form(...), files: List[UploadFile] = File(...)):
    # Clean job description
    cleaned_jd = simple_clean(job_description)
    
    file_names = []
    cleaned_resumes = []
    
    # Process each uploaded file dynamically based on its extension
    for file in files:
        contents = await file.read()
        
        if file.filename.endswith('.pdf'):
            raw_text = extract_text_from_pdf(contents)
        else:
            # Fallback for plain text (.txt) files
            raw_text = contents.decode("utf-8", errors="ignore")
            
        file_names.append(file.filename)
        cleaned_resumes.append(simple_clean(raw_text))
        
    # Combine data for TF-IDF Vectorization
    corpus = [cleaned_jd] + cleaned_resumes
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    # Calculate Cosine Similarity Scoring
    jd_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]
    similarity_scores = cosine_similarity(jd_vector, resume_vectors).flatten()
    
    # Candidate Ranking Algorithm
    rankings = []
    for i in range(len(file_names)):
        rankings.append({
            "filename": file_names[i],
            "score": round(float(similarity_scores[i]) * 100, 2)
        })
        
    # Sort rankings from highest score to lowest
    rankings.sort(key=lambda x: x["score"], reverse=True)
    
    return {"rankings": rankings}
