# Implementation of Gpt-4 embeddings

import os
import pdfplumber
from docx import Document
import openai
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json
import numpy as np
import time


def read_text_from_file(file_path):
    text = ""
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + '\n'
    return text

def read_cvs(folder_path):
    cvs = {}
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_path.endswith('.pdf') or file_path.endswith('.docx'):
            cvs[file_name] = read_text_from_file(file_path)
    return cvs






def get_embeddings(texts, model="text-embedding-ada-002", retries=5, retry_delay=20):
    api_key = ''
    if not api_key:
        print("API key not found. Please set the OPENAI_API_KEY environment variable.")
        return None

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    url = "https://api.openai.com/v1/embeddings"

    responses = []
    for text in texts:
        payload = json.dumps({
            "input": text,
            "model": model
        })

        for attempt in range(retries):
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                embedding = np.array(response.json()['data'][0]['embedding'])
                responses.append(embedding)
                break
            elif response.status_code == 429:
                print(f"Rate limit exceeded, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)  # Respect the Retry-After header if provided by the API
            else:
                print(f"Error {response.status_code}: {response.text}")
                responses.append(None)
                break
    
    return responses




def calculate_similarity(job_embed, cv_embeddings):
    return cosine_similarity([job_embed], cv_embeddings)


def main(folder_path, job_description):
    # Read CVs
    cvs = read_cvs(folder_path)
    
    # Generate embeddings for the job description and CVs
    texts = [job_description] + list(cvs.values())
    embeddings = get_embeddings(texts)
    
    if any(embed is None for embed in embeddings):
        print("Failed to retrieve one or more embeddings.")
        return
    
    # Job description embedding is the first one, rest are CVs
    job_embed = embeddings[0]
    cv_embeddings = embeddings[1:]
    
    # Calculate similarities
    similarities = calculate_similarity(job_embed, cv_embeddings)
    
    # Print results
    for (cv_name, score) in zip(cvs.keys(), similarities[0]):
        print(f"CV: {cv_name}, Similarity Score: {score}")



# Example usage
folder_path = 'Test'

job_description= '''
Senior Quality Assurance Engineer We are on the hunt for an exceptional Senior QA Engineer to join and elevate our team. 
This role is perfect for someone who is not just looking for a job but an opportunity to make a significant impact. 
Key Responsibilities: Develop, enhance, and maintain both front-end and back-end automated testing frameworks using
cutting-edge tools and technologies, alongside conducting manual testing when necessary.Take charge of our CI/CD 
processes, crafting a comprehensive test strategy, and embedding quality standards within automated pipelines.
Define, track, and optimize quality and performance metrics for our applications to ensure they meet our high standards.
Lead by example, reviewing test procedures and mentoring team members on best practices in automated testing.
Serve as the linchpin for quality control, ensuring application changes meet our rigorous standards for excellence.
Requirements: Proven track record as a Quality Assurance Engineer, boasting a deep understanding of automated testing 
frameworks for both front-end (e.g., Playwright) and back-end (e.g., xUnit) development. Experience with AWS DevOps, 
cloud services, and an ability to seamlessly integrate test cases into comprehensive suites for automation.Familiarity 
with test design, methodologies, and tools, with ISTQB or similar certifications being a huge plus. A strong team player 
with outstanding analytical abilities, you pride yourself on being independent, solution-focused, and proactive.
Excellent communication skills in English, both verbal and written, are essential. What We Offer: Competitive salaries 
that stand above market standards.Annual bonuses reflecting both personal and company performance.A generous learning 
and development budget to support your professional growth. 25 days of paid leave annually to ensure work-life balance.
'''

main(folder_path, job_description)
