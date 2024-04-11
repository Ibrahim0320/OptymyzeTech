# Attempting to match the CVs to the job description

import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


def retrieve_candidate_data():
    conn = sqlite3.connect('/Users/muhammadibrahim/Desktop/Github/Optymyze/cv_database.db')
    c= conn.cursor()
    c.execute('SELECT candidate_info, work_experience, skills, education, extracurricular_courses_and_certificates, relevant_projects FROM cv_data')  # Adjust feature names accordingly
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




# Test Run
job_description= '''
We are hiring a Data Scientist to join our team. 
The ideal candidate should have strong analytical skills and a passion for data-driven decision making. 
Responsibilities include analyzing large datasets, developing machine learning models, 
and providing actionable insights to drive business growth. 
Requirements include a Bachelor's degree in Computer Science, Statistics, or a related field, 
proficiency in Python and SQL, and experience with data visualization tools like Tableau or Power BI. 
If you're a data enthusiast looking for an exciting opportunity, apply now!
'''

# Preprocess job description
job_description = preprocess_text(job_description)
# Retrieve candidate features from the database
candidate_ids, candidate_features = retrieve_candidate_data()
# Calculate similarity between job description and candidate features
similarity_scores = calculate_similarity(job_description, [f[1] for f in candidate_features])
# Rank candidates based on similarity scores
ranked_candidates = candidate_ranking(candidate_ids, similarity_scores)

# Print the ranked candidates
# Print the ranked candidates
for candidate_info, score in ranked_candidates:
    # Extract the name from the candidate_info
    candidate_name = candidate_info.split('\n')[0]
    print(f"Candidate Name: {candidate_name}, Similarity Score: {score}")

