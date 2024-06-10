# Attempting to use OCR on pdfs
import os
import sqlite3
import pytesseract
from pdf2image import convert_from_path
import spacy

# Load Spacy model
nlp = spacy.load("en_core_web_sm")

def setup_database():
    with sqlite3.connect('InfoDatabase.db') as conn:
        c = conn.cursor()
        # Create a single table with columns for each type of information
        c.execute('''
            CREATE TABLE IF NOT EXISTS Candidates (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                work_experience TEXT,
                education TEXT,
                skills TEXT,
                extracurriculars TEXT
            )
        ''')

def insert_data(candidate_info):
    with sqlite3.connect('InfoDatabase.db') as conn:
        c = conn.cursor()
        # Insert all candidate information into the Candidates table
        c.execute('''
            INSERT INTO Candidates (name, email, work_experience, education, skills, extracurriculars) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            candidate_info['Name'],
            candidate_info['Email'],
            "\n".join(candidate_info['WorkExperience']),
            "\n".join(candidate_info['Education']),
            "\n".join(candidate_info['Skills']),
            "\n".join(candidate_info['Extracurriculars'])
        ))

def convert_pdf_to_text(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        full_text = ""
        for image in images:
            full_text += pytesseract.image_to_string(image) + "\n"
        return full_text
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return ""

def extract_info(text):
    doc = nlp(text)
    candidate_info = {
        'Name': '',
        'Email': '',
        'WorkExperience': [],
        'Education': [],
        'Skills': [],
        'Extracurriculars': []
    }

    section = None
    for sent in doc.sents:
        lower_text = sent.text.lower()
        if "experience" in lower_text or "work" in lower_text:
            section = 'WorkExperience'
        elif "education" in lower_text:
            section = 'Education'
        elif "skills" in lower_text:
            section = 'Skills'
        elif "extracurriculars" in lower_text:
            section = 'Extracurriculars'

        if section:
            candidate_info[section].append(sent.text)

    # Extract name and email using named entity recognition
    for ent in doc.ents:
        if ent.label_ == "EMAIL":
            candidate_info['Email'] = ent.text
        elif ent.label_ == "PERSON" and not candidate_info['Name']:
            candidate_info['Name'] = ent.text  # Assume first PERSON entity is the name

    return candidate_info


def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {filename}")
            text = convert_pdf_to_text(file_path)
            if text:
                info = extract_info(text)
                insert_data(info)
                print(f"Data inserted for {filename}")

# Example usage
setup_database()
folder_path = 'Test'
process_folder(folder_path)
