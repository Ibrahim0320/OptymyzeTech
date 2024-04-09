# Attempting to match the CVs to the job description

import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def retrieve_job_description():
    job_description = """
    This is a sample job description.
    We are looking for candidates with the following skills and qualifications:
    - Strong communication skills
    - Proficiency in Python programming
    - Experience with machine learning algorithms
    - Bachelor's degree in Computer Science or related field
    """
    return job_description

def retrieve_candidate_data():
    conn = sqlite3.connect('/Users/muhammadibrahim/Desktop/Github/Optymyze/cv_database.db')
    c= conn.cursor()
    c.execute('SELECT id, work_experience, skills FROM cv_data')  # Adjust feature names accordingly
    data = c.fetchall()
    conn.close()

    candidate_ids = [row[0] for row in data]
    candidate_features= [(row[1], row[2]) for row in data]  # Extract skills and experience
    return candidate_ids, candidate_features

candidate_ids, candidate_features = retrieve_candidate_data()

# Print the retrieved candidate data
print("Candidate IDs:")
print(candidate_ids)
print("\nCandidate Features:")
for feature in candidate_features:
    print(feature)

