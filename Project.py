# A file that contains all my coding work on the project

import pdfplumber

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Example usage:
pdf_path = "/Users/muhammadibrahim/Desktop/Applications/Muhammad Ibrahim CV.pdf"
unrefined_cv_text = extract_text_from_pdf(pdf_path)


import re

def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    # Remove special characters and extra whitespaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    return text

# Example usage:
text_no_extra_characters = preprocess_text(unrefined_cv_text)




import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Example usage:
entities = extract_entities(text_no_extra_characters)



'''
# Example training data
X_train = [
    "Work Experience: Software Engineer at XYZ Inc. (Jan 2019 - Present) - Developed...",
    "Education: Bachelor of Science in Computer Science, University of ABC (2015 - 2019)...",
    "Skills: Proficient in Python, Java, and SQL. Experience with machine learning algorithms...",
    "Work Experience: Intern at ABC Corporation (May 2018 - Aug 2018) - Assisted...",
    # Additional training examples...
]

# Corresponding labels for each training example
y_train = [
    "work_experience",
    "education",
    "skills",
    "work_experience",
    # Additional labels corresponding to each training example...
]


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

def classify_sections(text):
    # Use TF-IDF vectorization to convert text data into numerical features
    vectorizer = TfidfVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)

    # Initialize a logistic regression classifier
    classifier = LogisticRegression()

    # Train the classifier on the training data
    classifier.fit(X_train_vectorized, y_train)

    # Predict the section label for the input text
    text_vectorized = vectorizer.transform([text])
    predicted_section = classifier.predict(text_vectorized)[0]

    return {predicted_section: text}



# Example usage:

sections = classify_sections(preprocessed_text)

'''

