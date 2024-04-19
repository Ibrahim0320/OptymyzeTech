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
    candidate_features= [row[1:] for row in data]  # Extract skills and experience
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
            processed_feature = ' '.join(feature)  # Join all elements of the tuple
            processed_candidate_features.append(preprocess_text(processed_feature))
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
Senior Quality Assurance Engineer We are on the hunt for an exceptional Senior QA Engineer to join and elevate our team. 
This role is perfect for someone who is not just looking for a job but an opportunity to make a significant impact. 
Key Responsibilities: Develop, enhance, and maintain both front-end and back-end automated testing frameworks using
cutting-edge tools and technologies, alongside conducting manual testing when necessary.Take charge of our CI/CD 
processes, crafting a comprehensive test strategy, and embedding quality standards within automated pipelines.
Define, track, and optimize quality and performance metrics for our applications to ensure they meet our high standards.
Lead by example, reviewing test procedures and mentoring team members on best practices in automated testing.
Serve as the linchpin for quality control, ensuring application changes meet our rigorous standards for excellence.
Requirements: Proven track record as a Quality Assurance Engineer, boasting a deep understanding of automated testing 
frameworks for both front-end (e.g., Playwright) and back-end (e.g., xUnit) development. Experience with AWS DevOps, 
cloud services, and an ability to seamlessly integrate test cases into comprehensive suites for automation.Familiarity 
with test design, methodologies, and tools, with ISTQB or similar certifications being a huge plus. A strong team player 
with outstanding analytical abilities, you pride yourself on being independent, solution-focused, and proactive.
Excellent communication skills in English, both verbal and written, are essential. What We Offer: Competitive salaries 
that stand above market standards.Annual bonuses reflecting both personal and company performance.A generous learning 
and development budget to support your professional growth. 25 days of paid leave annually to ensure work-life balance.
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

