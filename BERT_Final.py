# Final version of BERT

import os
import pdfplumber
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import shutil

# Load BERT model and tokenizer once
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
model = BertModel.from_pretrained('bert-base-cased')

def read_text_from_file(file_path):
    text = ""
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        text = ' '.join(para.text for para in doc.paragraphs)
    return text

def retrieve_candidate_texts(folder_path):
    texts = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if file_path.endswith('.pdf') or file_path.endswith('.docx'):
            text = read_text_from_file(file_path)
            texts.append((file_name, text))
    return texts

def preprocess_text(text):
    text = text.lower()
    text = ''.join(char for char in text if char not in string.punctuation)
    words = text.split()
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    return ' '.join(lemmatizer.lemmatize(word) for word in words if word not in stop_words)

def encode_text_bert(texts):
    inputs = tokenizer(texts, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

def calculate_similarity_tfidf(job_description, candidate_features):
    vectorizer = TfidfVectorizer()
    all_texts = [job_description] + candidate_features
    vectors = vectorizer.fit_transform(all_texts)
    return cosine_similarity(vectors[0:1], vectors[1:]).flatten()

def calculate_similarity_bert(job_embed, candidate_embeddings):
    return cosine_similarity([job_embed], candidate_embeddings).flatten()





def main(job_description, folder_path):
    candidates = retrieve_candidate_texts(folder_path)
    processed_features = [preprocess_text(text) for _, text in candidates]

    # Preprocess and encode texts
    processed_texts = [preprocess_text(job_description)] + processed_features
    embeddings = encode_text_bert(processed_texts)

    job_embed = embeddings[0]
    candidate_embeddings = embeddings[1:]

    # Compute TF-IDF scores
    tfidf_scores = calculate_similarity_tfidf(job_description, processed_features)

    # Compute BERT scores
    bert_scores = calculate_similarity_bert(job_embed, candidate_embeddings)

    # Combine scores using a weighted average
    weight_for_bert = 0.7
    weight_for_tfidf = 0.3
    final_scores = weight_for_bert * bert_scores + weight_for_tfidf * tfidf_scores

    # Rank candidates
    ranked_candidates = sorted(zip([name for name, _ in candidates], final_scores), key=lambda x: x[1], reverse=True)

    # Determine the top candidate's score
    highest_score = ranked_candidates[0][1]

    # Determine the score range for relevant candidates
    score_threshold = highest_score - (0.10 * highest_score)  # 10% below the highest score

    # Select candidates within the top 10% score range
    relevant_cvs = [candidate for candidate in ranked_candidates if candidate[1] >= score_threshold]

    # Create a new folder for top candidates' CVs
    top_cv_folder = os.path.join(folder_path, "Top_CVs")
    if not os.path.exists(top_cv_folder):
        os.makedirs(top_cv_folder)

    # Copy relevant CV files to the new folder
    for file_name, _ in relevant_cvs:
        src_path = os.path.join(folder_path, file_name)
        dest_path = os.path.join(top_cv_folder, file_name)
        shutil.copy2(src_path, dest_path)  # copy2 preserves metadata

    # Display results
    print("\nTop 10% Score Range Relevant CVs:")
    for index, (file_name, score) in enumerate(relevant_cvs, start=1):
        print(f"{index}. {file_name}: Combined Similarity Score: {score}")

    print(f"Number of relevant CVs: {len(relevant_cvs)}")
    print(f"Relevant CVs are copied to: {top_cv_folder}")

    # Optionally return or further process relevant_cvs
    return relevant_cvs, ranked_candidates





# Specify the job description and the folder path containing CVs
folder_path = 'All Candidate CVs'
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

main(job_description, folder_path)
