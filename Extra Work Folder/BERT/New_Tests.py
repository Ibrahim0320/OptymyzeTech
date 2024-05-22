import os
import sqlite3
import pdfplumber
import re



def create_database():
    database_path = 'cv_database.db'
    print("Creating or opening the database at:", database_path)
    conn = sqlite3.connect(database_path)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS cv_data (
                        id INTEGER PRIMARY KEY,
                        Candidate_Info TEXT,
                        Professional_Background TEXT,
                        Education_Skills TEXT,
                        Extracurriculars_Certificates TEXT
                    )''')
        conn.commit()
        print("Database and table creation successful.")
    except Exception as e:
        print("Failed to create table:", e)
    finally:
        conn.close()

def insert_cv_data(parsed_sections):
    print("Inserting data into database...")
    conn = sqlite3.connect('cv_database.db')
    try:
        with conn:
            c = conn.cursor()
            c.execute('''INSERT OR IGNORE INTO cv_data (
                            Candidate_Info,
                            Professional_Background,
                            Education_Skills,
                            Extracurriculars_Certificates
                        ) VALUES (?, ?, ?, ?)''',
                        (parsed_sections.get('Candidate Info', ''),
                         parsed_sections.get('Professional Background', ''),
                         parsed_sections.get('Education & Skills', ''),
                         parsed_sections.get('Extracurriculars & Certificates', '')))
            if c.rowcount == 0:
                print("No data inserted. Possible duplicate or issue with the data.")
            else:
                print("Data inserted successfully.")
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
    return text

def parse_resume_sections(text):
    print("Parsing sections in the resume...")
    # Define the sections dictionary with default empty strings
    sections = {
        "Candidate Info": "",
        "Professional Background": "",
        "Education & Skills": "",
        "Extracurriculars & Certificates": ""
    }
    # Patterns to identify different sections more clearly
    section_patterns = {
        "Professional Background": r"Work Experience|Professional Experience|Projects",
        "Education & Skills": r"Education|Skills",
        "Extracurriculars & Certificates": r"Extracurricular Courses|Certificates|Activities"
    }
    current_section = None
    content_lines = text.split("\n")

    # First, extract candidate info such as name, email, phone number, and links
    candidate_info_extracted = False
    for line in content_lines:
        if not candidate_info_extracted:
            name_match = re.search(r"[A-Za-z]+ [A-Za-z]+", line)  # Simple regex for names
            email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", line)
            phone_match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", line)
            link_match = re.search(r"(LinkedIn|GitHub):\s*(\S+)", line)
            if name_match or email_match or phone_match or link_match:
                sections["Candidate Info"] += " ".join(filter(None, [name_match.group(0) if name_match else "",
                                                                    email_match.group(0) if email_match else "",
                                                                    phone_match.group(0) if phone_match else "",
                                                                    f"{link_match.group(1)}: {link_match.group(2)}" if link_match else ""]))
                candidate_info_extracted = True  # Only run this once to capture the first instance

    # Process other sections
    for line in content_lines:
        found_section = None
        for section, pattern in section_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                current_section = section  # Set current section upon finding a match
                break
        if current_section:
            sections[current_section] += line + "\n"  # Add line to the current section

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
            if cv_text.strip():
                parsed_sections = parse_resume_sections(cv_text)
                print("Parsed Sections:", parsed_sections)
                insert_cv_data(parsed_sections)
            else:
                print(f"Skipping file due to empty text content: {filename}")
    print("All files processed.")

def main():
    print("Starting CV processing script...")
    create_database()
    cv_folder_path = "Test"  # Ensure this directory exists and contains PDFs
    if os.path.isdir(cv_folder_path):
        process_cv_files(cv_folder_path)
    else:
        print("Invalid CV folder path")

main()









