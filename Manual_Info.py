

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity







def retrieve_candidate_data(csv_file):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file, delimiter= ',')
    
    # Extract relevant columns from the DataFrame
    candidate_ids = data['candidate_info']
    candidate_features = data[['work experience', 'education', 'skills', 'extracurrcicular', 'projects']].values.tolist()
    
    return candidate_ids, candidate_features




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
    processed_candidate_features = [preprocess_text(feature[0] + ' ' + feature[1]) for feature in candidate_features]

    if not processed_candidate_features:
        return np.array([])

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

job_description= preprocess_text(job_description)
# Path to your CSV file
csv_file_path = 'Manual test.csv'

# Retrieve candidate features from the CSV file
candidate_ids, candidate_features = retrieve_candidate_data(csv_file_path)

# Calculate similarity between job description and candidate features
similarity_scores = calculate_similarity(job_description, candidate_features)

# Rank candidates based on similarity scores
ranked_candidates = candidate_ranking(candidate_ids, similarity_scores)

# Print the ranked candidates
for candidate_id, score in ranked_candidates:
    print(f"Candidate ID: {candidate_id}, Similarity Score: {score}")



