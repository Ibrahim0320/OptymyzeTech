# Using Document AI to parse CVs

import os
from google.cloud import documentai_v1 as documentai
import re
import sqlite3
from google.oauth2 import service_account

import os
from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account

def get_client():
    credentials_path = 'beaming-mode-423311-q4-5e258468bd22.json'
    if not os.path.exists(credentials_path):
        print("Credentials file not found.")
        return None
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = documentai.DocumentProcessorServiceClient(credentials=credentials)
    return client


def get_files_from_folder(folder_path):
    files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            files.append(os.path.join(folder_path, filename))
    return files

def parse_cv(file_path, client, processor_id):
    name = f'projects/beaming-mode-423311-q4/locations/eu/processors/821b61a87ee4f1a3'
    with open(file_path, "rb") as f:
        content = f.read()
    document = {"content": content, "mime_type": "application/pdf"}
    request = {"name": name, "raw_document": document}
    result = client.process_document(request=request)
    return extract_information(result.document)

def extract_information(document):
    text_content = ' '.join([layout.text for page in document.pages for layout in page.paragraphs])
    return {
        "Name": extract_name(text_content),
        "Email": extract_email(text_content),
        "Phone": extract_phone(text_content),
        "Work Experience": extract_work_experience(text_content),
        "Projects": extract_projects(text_content),
        "Education": extract_education(text_content),
        "Skills": extract_skills(text_content),
        "Summary": text_content[:200]
    }


def extract_email(text):
    # Basic email regex pattern
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_phone(text):
    # Basic phone number regex pattern
    match = re.search(r'\+?\d[\d -]{8,12}\d', text)
    return match.group(0) if match else None

def extract_name(text):
    # Simplistic Name extraction assuming the first capitalized words might be the name
    match = re.findall(r'^([A-Z][a-z]*\s[A-Z][a-z]*)', text)
    return match[0] if match else None

def extract_work_experience(text):
    # Regex to extract work experience, assuming it starts with a header like "Experience" or "Work Experience"
    match = re.search(r'(Experience|Work Experience)[\s\S]*?(Education|Projects|Skills|Summary)', text, re.IGNORECASE)
    return match.group(0) if match else None

def extract_projects(text):
    # Regex to extract projects, assuming it starts with a header like "Projects"
    match = re.search(r'(Projects)[\s\S]*?(Experience|Education|Skills|Summary)', text, re.IGNORECASE)
    return match.group(0) if match else None

def extract_education(text):
    # Regex to extract education details
    match = re.search(r'(Education)[\s\S]*?(Experience|Projects|Skills|Summary)', text, re.IGNORECASE)
    return match.group(0) if match else None

def extract_skills(text):
    # Regex to find skills section
    match = re.search(r'(Skills)[\s\S]*?(Experience|Projects|Education|Summary)', text, re.IGNORECASE)
    return match.group(0) if match else None


# Add similar extraction functions for email, phone, work experience, projects, education, skills



def create_db():
    conn = sqlite3.connect('candidates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS candidates (
        Name TEXT, Email TEXT, Phone TEXT, WorkExperience TEXT,
        Projects TEXT, Education TEXT, Skills TEXT, Summary TEXT)''')
    conn.commit()
    conn.close()

def insert_candidate(candidate):
    conn = sqlite3.connect('candidates.db')
    c = conn.cursor()
    c.execute('''INSERT INTO candidates (Name, Email, Phone, WorkExperience, Projects, Education, Skills, Summary)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (candidate['Name'], candidate['Email'], candidate['Phone'],
               candidate['Work Experience'], candidate['Projects'], candidate['Education'],
               candidate['Skills'], candidate['Summary']))
    conn.commit()
    conn.close()

def main():
    folder_path = 'Test'
    files = get_files_from_folder(folder_path)
    client = get_client()
    processor_id = '821b61a87ee4f1a3'  # Update this

    create_db()

    for file_path in files:
        try:
            candidate_info = parse_cv(file_path, client, processor_id)
            insert_candidate(candidate_info)
            print(f"Processed {file_path} and stored information in database.")
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")



main()



