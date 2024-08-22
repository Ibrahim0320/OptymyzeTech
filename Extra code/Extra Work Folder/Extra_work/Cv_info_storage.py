# A database of sorts which will contain stored info from the extracted cvs

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

# Function to insert parsed CV sections into the database
def insert_cv_data(parsed_sections):
    conn = sqlite3.connect('cv_database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO cv_data (
                    work_experience,
                    education,
                    skills,
                    qualifications,
                    languages,
                    extracurricular_courses,
                    relevant_projects
                ) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (parsed_sections.get('work experience', ''),
                 parsed_sections.get('education', ''),
                 parsed_sections.get('skills', ''),
                 parsed_sections.get('qualifications', ''),
                 parsed_sections.get('languages', ''),
                 parsed_sections.get('extracurricular courses and certificates', ''),
                 parsed_sections.get('relevant projects', '')))
    conn.commit()
    conn.close()

# Call the function to create the database
create_database()

# Insert parsed CV sections into the database
insert_cv_data(parsed_sections)
