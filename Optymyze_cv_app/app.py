# Setting up the backend with flask

import os
import shutil
import time
import requests
import pdfplumber
from docx import Document
from flask import Flask, request, jsonify, send_from_directory, render_template
from transformers import BertTokenizer, BertModel
import torch
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

# Function to read text from a file
def read_text_from_file(file_path):
    text = ""
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        text = ' '.join(para.text for para in doc.paragraphs)
    return text

# Function to retrieve candidate texts from a folder
def retrieve_candidate_texts(folder_path):
    texts = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_path.endswith('.pdf') or file_path.endswith('.docx'):
            text = read_text_from_file(file_path)
            texts.append((file_name, text))
    return texts

# Function to preprocess text
def preprocess_text(text):
    text = text.lower()
    text = ''.join(char for char in text if char not in string.punctuation)
    words = text.split()
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    return ' '.join(lemmatizer.lemmatize(word) for word in words if word not in stop_words)

# Function to encode text using BERT
def encode_text_bert(texts):
    inputs = tokenizer(texts, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# Function to calculate similarity using TF-IDF
def calculate_similarity_tfidf(job_description, candidate_features):
    vectorizer = TfidfVectorizer()
    all_texts = [job_description] + candidate_features
    vectors = vectorizer.fit_transform(all_texts)
    return cosine_similarity(vectors[0:1], vectors[1:]).flatten()

# Function to calculate similarity using BERT embeddings
def calculate_similarity_bert(job_embed, candidate_embeddings):
    return cosine_similarity([job_embed], candidate_embeddings).flatten()

# Function to create a zip file from a folder
def create_zip_folder(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), folder_path))

# Function to generate ChatGPT evaluation report with batch processing and retry logic
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
                all_results.append(response.json()['choices'][0]['message']['content'].strip())
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
    
    return "\n\n".join(all_results)

# Main function to process CVs and calculate scores
def main(job_description, folder_path):
    try:
        print("Main function started")  # Debug statement
        candidates = retrieve_candidate_texts(folder_path)
        if not candidates:
            print("No CVs found")  # Debug statement
            return None, "No CVs found in the folder."

        processed_features = [preprocess_text(text) for _, text in candidates]
        print(f"Processed features: {processed_features}")  # Debug statement

        # Preprocess and encode texts
        processed_texts = [preprocess_text(job_description)] + processed_features
        embeddings = encode_text_bert(processed_texts)
        print(f"Embeddings: {embeddings}")  # Debug statement

        job_embed = embeddings[0]
        candidate_embeddings = embeddings[1:]

        # Compute TF-IDF scores
        tfidf_scores = calculate_similarity_tfidf(job_description, processed_features)
        print(f"TF-IDF scores: {tfidf_scores}")  # Debug statement

        # Compute BERT scores
        bert_scores = calculate_similarity_bert(job_embed, candidate_embeddings)
        print(f"BERT scores: {bert_scores}")  # Debug statement

        # Combine scores using a weighted average
        weight_for_bert = 0.7
        weight_for_tfidf = 0.3
        final_scores = weight_for_bert * bert_scores + weight_for_tfidf * tfidf_scores
        print(f"Final scores: {final_scores}")  # Debug statement

        # Rank candidates
        ranked_candidates = sorted(zip([name for name, _ in candidates], final_scores), key=lambda x: x[1], reverse=True)
        print(f"Ranked candidates: {ranked_candidates}")  # Debug statement

        # Determine the top candidate's score
        highest_score = ranked_candidates[0][1]

        # Determine the score range for relevant candidates
        score_threshold = highest_score - (0.10 * highest_score)  # 10% below the highest score

        # Select candidates within the top 10% score range
        relevant_cvs = [candidate for candidate in ranked_candidates if candidate[1] >= score_threshold]

        if not relevant_cvs:
            print("No CVs within the top 10% score range")  # Debug statement
            return None, "No CVs within the top 10% score range."

        # Create a new folder for top candidates' CVs
        top_cv_folder = os.path.join(folder_path, "Top_CVs")
        if not os.path.exists(top_cv_folder):
            os.makedirs(top_cv_folder)

        # Copy relevant CV files to the new folder
        for file_name, _ in relevant_cvs:
            src_path = os.path.join(folder_path, file_name)
            dest_path = os.path.join(top_cv_folder, file_name)
            shutil.copy2(src_path, dest_path)  # copy2 preserves metadata

        # Generate ChatGPT report
        relevant_texts = [(name, read_text_from_file(os.path.join(folder_path, name))) for name, _ in relevant_cvs]
        chatgpt_report = generate_chatgpt_report(job_description, relevant_texts)

        # Save ChatGPT report as a text file in the same folder as the zip file
        chatgpt_report_file = "OptymyzeTech_AI_Candidate_Assessment.txt"
        with open(chatgpt_report_file, "w") as file:
            file.write(chatgpt_report)
        print(f"ChatGPT report saved to {chatgpt_report_file}")  # Debug statement

        return (relevant_cvs, ranked_candidates, chatgpt_report_file), None
    except Exception as e:
        print(f"Exception in main function: {str(e)}")  # Debug statement
        return None, str(e)

@app.route('/')
def serve_frontend():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    try:
        job_description = request.form['job_description']
        uploaded_files = request.files.getlist('files')
        
        print("Received job description:", job_description)
        print("Received files:", [file.filename for file in uploaded_files])

        # Save uploaded files to a temporary directory
        cv_folder = 'temp_cvs'
        if not os.path.exists(cv_folder):
            os.makedirs(cv_folder)
        for uploaded_file in uploaded_files:
            uploaded_file.save(os.path.join(cv_folder, uploaded_file.filename))
        
        # Process CVs using the new main function
        result, error = main(job_description, cv_folder)
        
        if error:
            print(f"Error processing CVs: {error}")
            return jsonify({"error": error}), 500

        relevant_cvs, ranked_candidates, chatgpt_report_file = result

        # Create a zip file of the top CVs
        zip_name = 'top_cvs.zip'
        create_zip_folder(os.path.join(cv_folder, "Top_CVs"), zip_name)
        
        # Clean up temporary CV folders
        shutil.rmtree(cv_folder)

        # Generate a readable result for display
        result_text = "\n".join([f"{i+1}. {name}: {score}" for i, (name, score) in enumerate(ranked_candidates)])
        
        if relevant_cvs:
            print("Response: ", result_text)
            print("Zip Name: ", zip_name)
            print("ChatGPT Report File: ", chatgpt_report_file)
            return render_template('results.html', result=result_text, zip_name=zip_name, chatgpt_report_file=chatgpt_report_file)
        else:
            return jsonify({"error": "Failed to process CVs"}), 500
    except Exception as e:
        print(f"Exception in evaluate function: {str(e)}")  # Debug statement
        return jsonify({"error": str(e)}), 500

@app.route('/results')
def results():
    zip_name = request.args.get('zip_name')
    result = request.args.get('result')
    chatgpt_report_file = request.args.get('chatgpt_report_file')
    return render_template('results.html', zip_name=zip_name, result=result, chatgpt_report_file=chatgpt_report_file)

@app.route('/download/<path:filename>')
def download_file(filename):
    print(f"Serving file {filename}")  # Debug statement
    return send_from_directory('', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
