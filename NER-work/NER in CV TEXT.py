# Trying to mix the old CV Scanner and the new NER model, to correctly identify sentences and place themc orrectly

import os
import sqlite3
import spacy
from pdf2image import convert_from_path
import pytesseract
import traceback
from fuzzywuzzy import process

# Load the pretrained spaCy model and add the sentencizer component
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('sentencizer')

def convert_pdf_to_text(pdf_path):
    images = convert_from_path(pdf_path)
    full_text = []
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text.append(text)
    return "\n".join(full_text)

def extract_entities(text, nlp):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities, doc

def parse_resume_sections(text, nlp):
    try:
        sections = {
            'Name': '',
            'Email': '',
            'Work Experience': '',
            'Education': ''
        }

        entities, doc = extract_entities(text, nlp)

        # Debug: Print the extracted text and entities
        print(f"Extracted Text: {text}")
        print(f"Extracted Entities: {entities}")

        # Extract candidate's name and contact information
        for ent in entities:
            if ent[1] == 'PERSON' and not sections['Name']:
                sections['Name'] = ent[0]
            elif ent[1] == 'EMAIL' and not sections['Email']:
                sections['Email'] = ent[0]

        # Define keywords for sections
        work_experience_keywords = ['work experience', 'professional experience', 'employment history']
        education_keywords = ['education', 'academic background', 'qualifications']
        education_phrases = ['university of', 'bachelor of', 'bachelor in', 'master of', 'master in', 'phd in', 'phd of']

        current_section = None

        for sent in doc.sents:
            line = sent.text.strip().lower()
            if not line:
                continue

            if any(keyword in line for keyword in work_experience_keywords):
                current_section = 'Work Experience'
                continue
            elif any(keyword in line for keyword in education_keywords) or any(phrase in line for phrase in education_phrases):
                current_section = 'Education'
                continue

            if current_section == 'Work Experience':
                sections['Work Experience'] += sent.text.strip() + '\n'
            elif current_section == 'Education':
                sections['Education'] += sent.text.strip() + '\n'

        # Debug: Print parsed sections
        print(f"Parsed Sections: {sections}")

        return sections
    except Exception as e:
        print(f"Error parsing CV: {e}")
        print(traceback.format_exc())  # Print traceback for more detailed error information
        raise

def process_folder(folder_path, nlp):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {filename}")
            text = convert_pdf_to_text(file_path)
            parsed_sections = parse_resume_sections(text, nlp)
            documents.append(parsed_sections)
    return documents

def create_and_populate_db(documents):
    conn = sqlite3.connect('cv_data.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS Candidates (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        work_experience TEXT,
        education TEXT
    )
    ''')

    for doc in documents:
        name = doc.get('Name', "")
        email = doc.get('Email', "")
        work_experience = doc.get('Work Experience', "")
        education = doc.get('Education', "")

        name = str(name)
        email = str(email)
        work_experience = str(work_experience)
        education = str(education)

        print(f"Inserting Data: Name: {name}, Email: {email}, Work Experience: {work_experience}, Education: {education}")

        try:
            c.execute('''
            INSERT INTO Candidates (name, email, work_experience, education)
            VALUES (?, ?, ?, ?)
            ''', (name, email, work_experience, education))
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

    conn.commit()
    conn.close()

# Main script execution
folder_path = 'Test1'
documents = process_folder(folder_path, nlp)

if documents:
    create_and_populate_db(documents)
else:
    print("No documents were processed.")
