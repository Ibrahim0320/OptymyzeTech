# Here BERT is integrated into the CV-to-req matching

import numpy as np
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

# Ensure you have the necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def retrieve_candidate_data():
    conn = sqlite3.connect('BERT int/cv_database.db')
    c = conn.cursor()
    c.execute('SELECT Candidate_Info, Professional_Background, Education_Skills, Extracurriculars_Certificates FROM cv_data')
    data = c.fetchall()
    conn.close()
    candidate_ids = [row[0] for row in data]
    candidate_features = [row[1:] for row in data]
    return candidate_ids, candidate_features


def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = ''.join([char for char in text if char not in string.punctuation])
    # Tokenize text
    words = text.split()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    # Join words to reform the sentence
    return ' '.join(words)

def load_model_and_tokenizer(model_name='bert-base-cased'):
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)
    return tokenizer, model


def encode_text_bert(tokenizer, model, text):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding=True)
    outputs = model(**inputs)
    # Return the mean of the last hidden state to represent the document
    return outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

def calculate_similarity_tfidf(job_description, candidate_features):
    vectorizer = TfidfVectorizer()
    job_vector = vectorizer.fit_transform([job_description])
    candidate_vectors = vectorizer.transform(candidate_features)
    return cosine_similarity(job_vector, candidate_vectors).flatten()

def calculate_similarity_bert(tokenizer, model, job_description, candidate_features):
    job_embed = encode_text_bert(tokenizer, model, job_description)
    candidate_embeddings = np.array([encode_text_bert(tokenizer, model, feature) for feature in candidate_features])
    similarities = cosine_similarity([job_embed], candidate_embeddings).flatten()
    return similarities

# Main execution
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






def main(job_description):
    # Load model and tokenizer for BERT
    tokenizer, model = load_model_and_tokenizer()

    # Retrieve and preprocess candidate data
    candidate_ids, candidate_features = retrieve_candidate_data()
    processed_features = [preprocess_text(' '.join(feature)) for feature in candidate_features]

    # Compute TF-IDF scores
    tfidf_scores = calculate_similarity_tfidf(job_description, processed_features)

    # Compute BERT scores
    bert_scores = calculate_similarity_bert(tokenizer, model, job_description, processed_features)

    # Combine scores using a weighted average
    weight_for_bert = 0.7 # Adjust as needed
    weight_for_tfidf = 0.3  # Adjust as needed
    final_scores = weight_for_bert * bert_scores + weight_for_tfidf * tfidf_scores

    # Rank candidates
    ranked_candidates = sorted(zip(candidate_ids, final_scores), key=lambda x: x[1], reverse=True)

    # Print the top candidates
    for candidate_id, score in ranked_candidates[:10]:  # Adjust the slice as needed
        print(f"Candidate ID: {candidate_id}, Combined Similarity Score: {score}")

# Example job description

main(job_description)


