import os
from Working_build import *
import sqlite3
import re



# Function to create a SQLite database and table

def create_database():
    conn = sqlite3.connect('cv_database.db')
    c = conn.cursor()
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
    conn.close()

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
                    (parsed_sections.get('Candidate_Info', ''),
                     parsed_sections.get('Work Experience', ''),
                     parsed_sections.get('Education', ''),
                     parsed_sections.get('Skills', ''),
                     parsed_sections.get('Languages', ''),
                     parsed_sections.get('Extracurricular Courses and Certificates', ''),
                     parsed_sections.get('Relevant Projects', '')))
        conn.commit()
        conn.close()
        print("Data inserted successfully.")
    except sqlite3.Error as e:
        print("Error inserting data:", e)


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




# Specify the folder containing CVs
cv_folder_path = "Test"

# Verify the path exists
if os.path.isdir(cv_folder_path):
    # Process CVs in the folder
    iterate_over_cv_folder_extract_and_parse_and_store(cv_folder_path)
else:
    print("Error: Invalid CV folder path!")

import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def preprocess_job_description(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.replace("'", "")  # Remove apostrophes
    text = text.replace("-", " ")  # Replace hyphens with spaces
    text = ''.join([char for char in text if char.isalnum() or char.isspace()])  # Remove non-alphanumeric characters
    # Remove extra whitespaces
    text = ' '.join(text.split())
    return text



def retrieve_candidate_data():
    conn = sqlite3.connect('/Users/muhammadibrahim/Desktop/Github/Optymyze/cv_database.db')
    c= conn.cursor()
    c.execute('SELECT DISTINCT candidate_info, work_experience, skills, education, extracurricular_courses_and_certificates, relevant_projects FROM cv_data')  # Adjust feature names accordingly
    data = c.fetchall()
    conn.close()

    candidate_ids = [row[0] for row in data]
    candidate_features= [(row[1], row[2]) for row in data]  # Extract skills and experience
    return candidate_ids, candidate_features

candidate_ids, candidate_features = retrieve_candidate_data()

# Print the retrieved candidate data
#print("Candidate IDs:")
#print(candidate_ids)
#print("\nCandidate Features:")
#for feature in candidate_features:
#    print(feature)

def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.replace("'", "")  # Remove apostrophes
    text = text.replace("-", " ")  # Replace hyphens with spaces
    text = ''.join([char for char in text if char.isalnum() or char.isspace()])  # Remove non-alphanumeric characters
    # Remove extra whitespaces
    text = ' '.join(text.split())
    return text


def calculate_similarity(job_description, candidate_features):
    processed_job_description = preprocess_text(job_description)
    
    processed_candidate_features = []
    for feature in candidate_features:
        if isinstance(feature, tuple):  
            if len(feature) == 2:  
                processed_candidate_features.append(preprocess_text(feature[0] + ' ' + feature[1]))
            elif len(feature) == 1:  
                processed_candidate_features.append(preprocess_text(feature[0]))
        elif isinstance(feature, str):  
            processed_candidate_features.append(preprocess_text(feature))
    
    # Check if there are valid candidate features
    if not processed_candidate_features:
        return np.array([])  # Return an empty array
    
    vectorizer = TfidfVectorizer()
    job_vector = vectorizer.fit_transform([processed_job_description])
    candidate_vectors = vectorizer.transform(processed_candidate_features)
    
    similarities = cosine_similarity(job_vector, candidate_vectors)
    return similarities.flatten()


def candidate_ranking(candidate_ids, similarities):
    ranked_candidates = sorted(zip(candidate_ids, similarities), key=lambda x: x[1], reverse=True)
    return ranked_candidates

