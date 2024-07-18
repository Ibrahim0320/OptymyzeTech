# Setting up the backend with flask

# app.py

import os
import shutil
import time
import requests
import pdfplumber
from docx import Document
from flask import Flask, request, jsonify, send_from_directory, render_template
from transformers import BertTokenizer, BertModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import zipfile
import openai

app = Flask(__name__, static_url_path='/static', static_folder='frontend/static', template_folder='frontend/templates')

# Set up OpenAI API key
openai.api_key = ""

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
model = BertModel.from_pretrained('bert-base-cased')

def read_text_from_file(file_path):
    text = ""
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        text = ' '.join(para.text for para in doc.paragraphs)
    return text

def retrieve_candidate_texts(folder_path):
    texts = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_path.endswith('.pdf') or file_path.endswith('.docx'):
            text = read_text_from_file(file_path)
            texts.append((file_name, text))
    return texts

def preprocess_text(text):
    text = text.lower()
    text = ''.join(char for char in text if char not in string.punctuation)
    words = text.split()
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    return ' '.join(lemmatizer.lemmatize(word) for word in words if word not in stop_words)

def encode_text_bert(texts):
    inputs = tokenizer(texts, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

def calculate_similarity_tfidf(job_description, candidate_features):
    vectorizer = TfidfVectorizer()
    all_texts = [job_description] + candidate_features
    vectors = vectorizer.fit_transform(all_texts)
    return cosine_similarity(vectors[0:1], vectors[1:]).flatten()

def calculate_similarity_bert(job_embed, candidate_embeddings):
    return cosine_similarity([job_embed], candidate_embeddings).flatten()

def create_zip_folder(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))

import re

def generate_chatgpt_report(job_description, cvs, batch_size=3, max_retries=10):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai.api_key}'
    }
    
    all_results = []
    
    for i in range(0, len(cvs), batch_size):
        batch = cvs[i:i + batch_size]
        prompt = f"Job Description: {job_description}\n\nCVs:\n"
        for idx, (filename, text) in enumerate(batch, start=1):
            prompt += f"{idx}. Filename: {filename}, CV Content: {text}\n"
        prompt += "\nEvaluate these CVs based on the job description and provide a detailed report for each."

        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are an AI assistant tasked with evaluating CVs based on a job description."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2500,
            "temperature": 0.5
        }

        for attempt in range(max_retries):
            try:
                response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
                response.raise_for_status()
                report_content = response.json()['choices'][0]['message']['content'].strip()
                formatted_report = split_and_format_report(report_content)
                all_results.append(formatted_report)
                break
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:
                    retry_after = response.headers.get('Retry-After')
                    if retry_after is None:
                        retry_after = 2 ** attempt
                    else:
                        retry_after = int(retry_after)
                    print(f"Rate limit exceeded. Retrying in {retry_after} seconds...")
                    time.sleep(retry_after)
                else:
                    print(f"An error occurred with OpenAI API: {e}")
                    break
        else:
            print("Max retries exceeded. Could not complete the request.")
            return "Error: Unable to generate ChatGPT report due to rate limiting."
    
    return "\n".join(all_results)

def split_and_format_report(report_content):
    pattern = r'(\d+\.\s[A-Za-z]+[^\n]*)'
    split_content = re.split(pattern, report_content)
    
    formatted_report = ''
    for i in range(1, len(split_content), 2):
        candidate_info = split_content[i]
        candidate_report = split_content[i+1].strip()
        paragraphs = split_text_into_paragraphs(candidate_report, max_length=300)
        formatted_paragraphs = ''.join([f'<p>{para}</p>' for para in paragraphs])
        formatted_report += f'<div class="candidate-report"><h3>{candidate_info}</h3>{formatted_paragraphs}</div>'
    
    return formatted_report

def split_text_into_paragraphs(text, max_length=300):
    words = text.split()
    paragraphs = []
    current_paragraph = []

    for word in words:
        current_paragraph.append(word)
        if len(' '.join(current_paragraph)) >= max_length:
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []

    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))
    
    return paragraphs

def main(job_description, folder_path):
    try:
        print("Main function started")  # Debug statement
        candidates = retrieve_candidate_texts(folder_path)
        if not candidates:
            print("No CVs found")  # Debug statement
            return None, "No CVs found in the folder."

        processed_features = [preprocess_text(text) for _, text in candidates]
        print(f"Processed features: {processed_features}")  # Debug statement

        processed_texts = [preprocess_text(job_description)] + processed_features
        embeddings = encode_text_bert(processed_texts)
        print(f"Embeddings: {embeddings}")  # Debug statement

        job_embed = embeddings[0]
        candidate_embeddings = embeddings[1:]

        tfidf_scores = calculate_similarity_tfidf(job_description, processed_features)
        print(f"TF-IDF scores: {tfidf_scores}")  # Debug statement

        bert_scores = calculate_similarity_bert(job_embed, candidate_embeddings)
        print(f"BERT scores: {bert_scores}")  # Debug statement

        weight_for_bert = 0.7
        weight_for_tfidf = 0.3
        final_scores = weight_for_bert * bert_scores + weight_for_tfidf * tfidf_scores
        print(f"Final scores: {final_scores}")  # Debug statement

        ranked_candidates = sorted(zip([name for name, _ in candidates], final_scores), key=lambda x: x[1], reverse=True)
        print(f"Ranked candidates: {ranked_candidates}")  # Debug statement

        highest_score = ranked_candidates[0][1]

        score_threshold = highest_score - (0.10 * highest_score)

        relevant_cvs = [candidate for candidate in ranked_candidates if candidate[1] >= score_threshold]

        if not relevant_cvs:
            print("No CVs within the top 10% score range")  # Debug statement
            return None, "No CVs within the top 10% score range."

        top_cv_folder = os.path.join(folder_path, "Top_CVs")
        if not os.path.exists(top_cv_folder):
            os.makedirs(top_cv_folder)

        for file_name, _ in relevant_cvs:
            src_path = os.path.join(folder_path, file_name)
            dest_path = os.path.join(top_cv_folder, file_name)
            shutil.copy2(src_path, dest_path)

        formatted_ranked_candidates = [
            (name, f"{score*100:.2f}%") for name, score in ranked_candidates
        ]

        relevant_texts = [(name, read_text_from_file(os.path.join(folder_path, name))) for name, _ in relevant_cvs]
        chatgpt_report = generate_chatgpt_report(job_description, relevant_texts)

        return (relevant_cvs, formatted_ranked_candidates, chatgpt_report), None
    except Exception as e:
        print(f"Exception in main function: {str(e)}")  # Debug statement
        return None, str(e)

@app.route('/')
def serve_frontend():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    job_description = request.form['job_description']
    uploaded_files = request.files.getlist('files')
    
    cv_folder = 'temp_cvs'
    if not os.path.exists(cv_folder):
        os.makedirs(cv_folder)
    for uploaded_file in uploaded_files:
        uploaded_file.save(os.path.join(cv_folder, uploaded_file.filename))

    result, error = main(job_description, cv_folder)

    if error:
        return jsonify({"error": error}), 500

    relevant_cvs, ranked_candidates, chatgpt_report = result

    zip_name = 'top_cvs.zip'
    create_zip_folder(os.path.join(cv_folder, "Top_CVs"), zip_name)

    shutil.rmtree(cv_folder)

    return jsonify({
        "result": ranked_candidates,
        "chatgpt_report": chatgpt_report,
        "zip_name": zip_name
    })

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(directory=os.getcwd(), path=filename)

if __name__ == "__main__":
    app.run(debug=True)
