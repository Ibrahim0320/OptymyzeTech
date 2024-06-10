# Setting up backend with Flask

import os
import shutil
from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from PyPDF2 import PdfFileReader
import openai

app = Flask(__name__)

# Set up OpenAI API key (Make sure to keep this secret)
openai.api_key = "your-api-key"

# Load pre-trained BERT model and tokenizer
model_name = "bert-base-cased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfFileReader(file)
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extract_text()
    return text

# Function to get BERT score
def get_bert_score(job_description, candidate_text):
    inputs = tokenizer(job_description, candidate_text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    scores = outputs.logits
    return scores.softmax(dim=1).detach().numpy()[0][1]  # Assuming binary classification, we take the positive class score

# Function to call OpenAI API and get the match score
def get_openai_score(job_description, candidate_text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Job Description: {job_description}\n\nCandidate Resume: {candidate_text}\n\nRate this candidate's fit for the job on a scale of 1 to 100.",
        max_tokens=10
    )
    return float(response.choices[0].text.strip())

# Function to evaluate candidates
def evaluate_candidates(job_description, cv_folder):
    scores = {}
    for cv_filename in os.listdir(cv_folder):
        if cv_filename.endswith('.pdf'):
            cv_path = os.path.join(cv_folder, cv_filename)
            candidate_text = extract_text_from_pdf(cv_path)
            bert_score = get_bert_score(job_description, candidate_text)
            if bert_score > 0.5:  # BERT threshold
                openai_score = get_openai_score(job_description, candidate_text)
                scores[cv_filename] = openai_score
    return scores

@app.route('/evaluate', methods=['POST'])
def evaluate():
    job_description = request.form['job_description']
    uploaded_files = request.files.getlist('files')
    
    # Save uploaded files to a temporary directory
    cv_folder = 'temp_cvs'
    if not os.path.exists(cv_folder):
        os.makedirs(cv_folder)
    for uploaded_file in uploaded_files:
        uploaded_file.save(os.path.join(cv_folder, uploaded_file.filename))
    
    # Evaluate candidates
    scores = evaluate_candidates(job_description, cv_folder)

    # Move top candidates to TOP Candidates folder
    top_candidates_folder = 'TOP_Candidates'
    if not os.path.exists(top_candidates_folder):
        os.makedirs(top_candidates_folder)

    for cv_filename, score in scores.items():
        if score >= 80:  # Threshold for top candidates
            shutil.move(os.path.join(cv_folder, cv_filename), os.path.join(top_candidates_folder, cv_filename))
    
    # Clean up temporary CV folder
    shutil.rmtree(cv_folder)

    return jsonify(scores)

if __name__ == "__main__":
    app.run(debug=True)


