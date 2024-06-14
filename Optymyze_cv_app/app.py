# Setting up the backend with flask


import os
import shutil
import time
import requests
import csv
import pdfplumber
from docx import Document
from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from PyPDF2 import PdfReader
import openai
import zipfile

app = Flask(__name__, static_url_path='', static_folder='frontend', template_folder='templates')

# Set up OpenAI API key (Make sure to keep this secret)
openai.api_key = "your_openai_api_key"

# Load pre-trained BERT model and tokenizer
model_name = "bert-base-cased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to get BERT score
def get_bert_score(job_description, candidate_text):
    inputs = tokenizer(job_description, candidate_text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    scores = outputs.logits
    return scores.softmax(dim=1).detach().numpy()[0][1]  # Assuming binary classification, we take the positive class score

def read_text_from_file(file_path):
    text = ""
    try:
        if file_path.endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                pages = [page.extract_text() for page in pdf.pages if page.extract_text()]
                text = ' '.join(pages)
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            text = ' '.join(para.text for para in doc.paragraphs if para.text)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return text

def retrieve_candidate_texts(folder_path):
    texts = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_path.endswith('.pdf') or file_path.endswith('.docx'):
            text = read_text_from_file(file_path)
            if text:
                texts.append((file_name, text))
            else:
                print(f"No text extracted from {file_name}.")
    return texts

def analyze_cvs_with_gpt4(api_key, job_description, cvs, batch_size=3, max_retries=5):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    all_results = []
    for i in range(0, len(cvs), batch_size):
        batch = cvs[i:i + batch_size]
        prompt = f"Job Description: {job_description}\n\nCVs:\n"
        for idx, (filename, text) in enumerate(batch, start=1):
            prompt += f"{idx}. Filename: {filename}, CV Content: {text}\n"
        prompt += "\nRank the CVs based on their suitability for the job described above. More CVs will follow. Make sure to give me a final ranking containing every single CV that I have submitted to you."

        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are an AI assistant tasked with evaluating CVs based on a job description."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2500,
            "temperature": 0.5
        }

        retries = 0
        while retries < max_retries:
            try:
                response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
                response.raise_for_status()
                all_results.append(response.json()['choices'][0]['message']['content'].strip())
                break
            except requests.exceptions.RequestException as e:
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 2 ** retries))
                    print(f"Rate limit exceeded. Retrying in {retry_after} seconds...")
                    time.sleep(retry_after)
                    retries += 1
                else:
                    print(f"An error occurred with OpenAI API: {e}")
                    return None
        else:
            print("Max retries exceeded. Could not complete the request.")
            return None
    return "\n\n".join(all_results)

def save_response_to_text(response, filename='gpt4_response.txt'):
    with open(filename, 'w') as file:
        file.write(response)
    print(f"Response saved to {filename}")

def save_response_to_csv(response, filename='gpt4_response.csv'):
    lines = response.split("\n")
    data = []
    for line in lines:
        if line.strip():  # Skip empty lines
            parts = line.split(". ", 1)
            if len(parts) == 2:
                index, content = parts
                data.append([index.strip(), content.strip()])
    
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Rank', 'Content'])
        writer.writerows(data)
    print(f"Response saved to {filename}")

def create_zip_folder(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))

# Function to evaluate candidates
def evaluate_candidates(job_description, cv_folder):
    scores = {}
    for cv_filename in os.listdir(cv_folder):
        if cv_filename.endswith('.pdf'):
            cv_path = os.path.join(cv_folder, cv_filename)
            candidate_text = extract_text_from_pdf(cv_path)
            bert_score = get_bert_score(job_description, candidate_text)
            if bert_score > 0.5:  # BERT threshold
                scores[cv_filename] = bert_score
    return scores

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

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
    
    # Evaluate candidates using BERT
    bert_scores = evaluate_candidates(job_description, cv_folder)
    
    # Prepare the CVs that passed BERT threshold for GPT-4 analysis
    top_cv_folder = 'temp_cvs_top'
    if not os.path.exists(top_cv_folder):
        os.makedirs(top_cv_folder)
    for cv_filename, score in bert_scores.items():
        if score > 0.5:  # Adjust this threshold as needed
            shutil.copy(os.path.join(cv_folder, cv_filename), os.path.join(top_cv_folder, cv_filename))

    # Perform GPT-4 analysis
    top_cvs = retrieve_candidate_texts(top_cv_folder)
    response = analyze_cvs_with_gpt4(openai.api_key, job_description, top_cvs)
    
    # Create a zip file of the top CVs
    zip_name = 'top_cvs.zip'
    create_zip_folder(top_cv_folder, zip_name)
    
    # Clean up temporary CV folders
    shutil.rmtree(cv_folder)
    shutil.rmtree(top_cv_folder)

    if response:
        save_response_to_text(response)
        save_response_to_csv(response)
        return render_template('results.html', result=response, zip_name=zip_name)
    else:
        return jsonify({"error": "Failed to analyze CVs with GPT-4"}), 500

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(os.getcwd(), filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
