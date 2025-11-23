import os
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text as extract_pdf_text
import docx

def extract_text(file_path):
    """Extracts text from PDF, DOCX, or TXT files."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == '.pdf':
            text = extract_pdf_text(file_path)
        elif ext == '.docx':
            doc = docx.Document(file_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return text

def clean_text(text):
    """Basic text cleaning."""
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.lower()

def rank_resumes(job_description, resume_files):
    """
    Ranks resumes based on similarity to job description.
    
    Args:
        job_description (str): The job description text.
        resume_files (list): List of paths to resume files.
        
    Returns:
        list: List of dicts containing 'filename', 'score', 'text_preview'.
    """
    documents = [job_description]
    filenames = ['Job Description']
    
    valid_resumes = []
    
    for file_path in resume_files:
        text = extract_text(file_path)
        if text.strip():
            cleaned = clean_text(text)
            documents.append(cleaned)
            filenames.append(os.path.basename(file_path))
            valid_resumes.append({'filename': os.path.basename(file_path), 'text': text})
            
    if len(documents) < 2:
        return []

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    
    # Calculate cosine similarity between Job Description (index 0) and all resumes
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    results = []
    for i, score in enumerate(cosine_sim):
        results.append({
            'filename': valid_resumes[i]['filename'],
            'score': round(score * 100, 2), # Convert to percentage
            'preview': valid_resumes[i]['text'][:200] + "..."
        })
        
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results
