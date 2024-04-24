import os
import sqlite3
import pdfplumber
import re
import logging

# Setup basic configuration for logging
logging.basicConfig(filename='cv_parsing.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

def create_database():
    database_path = 'cv_database.db'
    print("Creating or opening the database at:", database_path)
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS cv_data (
                        id INTEGER PRIMARY KEY,
                        Candidate_Info TEXT,
                        Work_Experience TEXT,
                        Education TEXT,
                        Skills TEXT,
                        Languages TEXT,
                        Extracurricular_Courses_and_Certificates TEXT,
                        Relevant_Projects TEXT
                    )''')
        conn.commit()
        print("Database and table creation successful.")
    except Exception as e:
        print("Failed to create table:", e)
    finally:
        conn.close()

def insert_cv_data(parsed_sections):
    conn = sqlite3.connect('cv_database.db')
    try:
        with conn:
            c = conn.cursor()
            c.execute('''INSERT OR IGNORE INTO cv_data (
                            Candidate_Info,
                            Work_Experience,
                            Education,
                            Skills,
                            Languages,
                            Extracurricular_Courses_and_Certificates,
                            Relevant_Projects
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (parsed_sections.get('Candidate Info', ''),
                         parsed_sections.get('Work Experience', ''),
                         parsed_sections.get('Education', ''),
                         parsed_sections.get('Skills', ''),
                         parsed_sections.get('Languages', ''),
                         parsed_sections.get('Extracurricular Courses and Certificates', ''),
                         parsed_sections.get('Relevant Projects', '')))
            if c.rowcount == 0:  # No rows inserted
                print("No data inserted. Possible duplicate or issue with the data.")
    except sqlite3.Error as e:
        print("Error inserting data:", e)
    finally:
        conn.close()


def extract_text_from_pdf(pdf_path):
    print(f"Extracting text from: {pdf_path}")
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    if text:
        print("Text extraction successful.")
    else:
        print("No text extracted.")
    return text

def parse_resume_sections(text):
    print("Parsing sections in the resume...")
    section_patterns = {
        "Candidate Info": r"Candidate Info|Personal Details",
        "Work Experience": r"Work Experience|Professional Experience",
        "Education": r"Education",
        "Skills": r"Skills",
        "Languages": r"Languages",
        "Extracurricular Courses and Certificates": r"Extracurricular Courses|Certificates",
        "Relevant Projects": r"Projects"
    }
    sections = {}
    current_section = None
    start_idx = 0
    content_lines = text.split("\n")

    for i, line in enumerate(content_lines):
        found = False
        for section, pattern in section_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                if current_section:
                    sections[current_section] = "\n".join(content_lines[start_idx:i])
                current_section = section
                start_idx = i + 1
                found = True
                break
        if not found and current_section:
            sections[current_section] = "\n".join(content_lines[start_idx:])
    print("Parsing completed.")
    return sections

def process_cv_files(folder_path):
    files = os.listdir(folder_path)
    print(f"Total files to process: {len(files)}")
    for filename in files:
        if filename.endswith('.pdf'):
            print(f"Processing file: {filename}")
            cv_path = os.path.join(folder_path, filename)
            cv_text = extract_text_from_pdf(cv_path)
            if cv_text.strip():  # Check if text is not just whitespace
                parsed_sections = parse_resume_sections(cv_text)
                print("Parsed Sections:", parsed_sections)  # Debug print to check data before insertion
                insert_cv_data(parsed_sections)
            else:
                print(f"Skipping file due to empty text content: {filename}")
    print("All files processed.")




# Test run
print("Starting CV processing script...")
create_database()
path= '/Users/muhammadibrahim/Desktop/Github/Optymyze/Test'
process_cv_files(path)








