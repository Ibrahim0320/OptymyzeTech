import os
from Working_build import *
import sqlite3

# Function to create a SQLite database and table

def create_database():
    conn = sqlite3.connect('cv_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cv_data (
                    id INTEGER PRIMARY KEY,
                    work_experience TEXT,
                    education TEXT,
                    skills TEXT,
                    qualifications TEXT,
                    languages TEXT,
                    extracurricular_courses TEXT,
                    relevant_projects TEXT
                )''')
    conn.commit()
    conn.close()

# Call the function to create the database and the table
create_database()

# Function to insert parsed CV sections into the database
def insert_cv_data(parsed_sections):


    try:
        conn = sqlite3.connect('cv_database.db')
        c = conn.cursor()
        c.execute('''INSERT INTO cv_data (
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
        conn.commit()
        conn.close()
        print("Data inserted successfully.")  # Print success message
    except sqlite3.Error as e:
        print("Error inserting data:", e)  # Print error message if an exception occurs


# Function to iterate through CV files in a folder
def iterate_over_cv_folder_extract_and_parse_and_store(folder_path):
    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):  # Assuming CVs are in PDF format
            cv_path = os.path.join(folder_path, filename)
            # Extract text from the CV
            cv_text = extract_text(cv_path)
            # Parse CV sections 
            parsed_sections = parse_resume_sections(cv_text)
            # Insert parsed CV sections into the SQLite database
            insert_cv_data(parsed_sections)

# Call the function to create the database
'create_database()'


# Specify the folder containing CVs
cv_folder_path = "Test"

# Verify the path exists
if os.path.isdir(cv_folder_path):
    # Process CVs in the folder
    iterate_over_cv_folder_extract_and_parse_and_store(cv_folder_path)
else:
    print("Error: Invalid CV folder path!")
