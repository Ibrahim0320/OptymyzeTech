# Connecting to GPT and moving the top files into the final assessment stage

import os
import requests
import json
import time
import csv
import pdfplumber
from docx import Document

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
        prompt += "\nRank the CVs based on their suitability for the job described above. More CVs will follow.Make sure to give me a final ranking containing every single CV that i have submitted to you."

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

def main(api_key, job_description, folder_path):
    top_cvs = retrieve_candidate_texts(folder_path)
    if not top_cvs:
        print("No CVs available for analysis.")
        return
    response = analyze_cvs_with_gpt4(api_key, job_description, top_cvs)
    if response:
        print("GPT-4 Analysis Result:")
        print(response)
        save_response_to_text(response)
        save_response_to_csv(response)



# Configuration
api_key = ""

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

folder_path = 'All Candidate CVs/Top_CVs'

main(api_key, job_description, folder_path)


