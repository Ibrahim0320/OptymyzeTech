# Creating a SQL database based on the NER extractions

import os
import sqlite3
import spacy
from pdf2image import convert_from_path
import pytesseract
from NER_OCR_Test import process_folder

# Load your custom spaCy model
nlp = spacy.load('Improved_ner_model')  # Ensure this path is correct

def convert_pdf_to_text(pdf_path):
    images = convert_from_path(pdf_path)
    full_text = []
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text.append(text)
    return "\n".join(full_text)

def extract_entities_from_pdf(pdf_path, nlp):
    # Convert PDF to text
    text = convert_pdf_to_text(pdf_path)
    
    # Process text with spaCy
    doc = nlp(text)
    
    # Extract entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def process_folder(folder_path, nlp):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {filename}")
            entities = extract_entities_from_pdf(file_path, nlp)
            if entities:
                documents.append(entities)
    return documents

# Function to create and populate the SQLite database
def create_and_populate_db(documents):
    # Connect to SQLite database
    conn = sqlite3.connect('cv_data.db')
    c = conn.cursor()
    
    # Create table
    c.execute('''
    CREATE TABLE IF NOT EXISTS Candidates (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        linkedin TEXT,
        github TEXT,
        work_experience TEXT,
        education TEXT
    )
    ''')

    for entities in documents:
        # Initialize fields
        name = email = linkedin = github = ""
        work_experience = []
        education = []

        # Extract and assign entities to respective fields
        for ent in entities:
            if ent[1] == 'PERSON' and not name:
                name = ent[0]
            elif ent[1] == 'EMAIL' and not email:
                email = ent[0]
            elif ent[1] == 'ORG' and 'linkedin' in ent[0].lower() and not linkedin:
                linkedin = ent[0]
            elif ent[1] == 'ORG' and 'github' in ent[0].lower() and not github:
                github = ent[0]
            elif ent[1] == 'ORG' and ('Tech Consulting' in ent[0] or 'Finnish Defence Forces' in ent[0] or 'Boston Consulting Group' in ent[0] or 'GenAl Consulting' in ent[0]):
                work_experience.append(ent[0])
            elif ent[1] == 'ORG' and ('University' in ent[0] or 'Gothenburg' in ent[0]):
                education.append(ent[0])

        # Convert lists to strings
        work_experience_str = '; '.join(work_experience)
        education_str = '; '.join(education)
        
        # Insert data into the table
        c.execute('''
        INSERT INTO Candidates (name, email, linkedin, github, work_experience, education)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, linkedin, github, work_experience_str, education_str))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

# Main script execution
folder_path = 'Test1'
documents = process_folder(folder_path, nlp)

if documents:
    create_and_populate_db(documents)
else:
    print("No documents were processed.")
