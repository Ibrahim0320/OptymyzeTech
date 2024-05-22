# Combining OCR and NER on Spacy to extract entities from CVs to make a summarisable database

from pdf2image import convert_from_path
import pytesseract
import spacy
import os
import spacy
import spacy_transformers
import pickle
import pandas as pd


train_data = pickle.load(open('/Users/muhammadibrahim/Downloads/train_data.pkl', 'rb'))


# Load your custom spaCy model
nlp = spacy.load('nlp_GIT_model2')
# Load a pre-trained generic model
nlp = spacy.load('en_core_web_sm')


doc = nlp(train_data[0][0])
for ent in doc.ents:
    print(f'{ent.label_.upper():{30}}- {ent.text}')


'''
def convert_pdf_to_text(pdf_path):
    images = convert_from_path(pdf_path)
    full_text = []
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text.append(text)
    return "\n".join(full_text)


def extract_entities_from_pdf(pdf_path, nlp):
    # Convert PDF to text
    text = convert_pdf_to_text(pdf_path)
    
    # Process text with spaCy
    doc = nlp(text)
    
    # Extract and print entities
    for ent in doc.ents:
        print(ent.text, ent.label_)



def process_folder(folder_path, nlp):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {filename}")
            extract_entities_from_pdf(file_path, nlp)

# Example usage
folder_path = 'Test1'
process_folder(folder_path, nlp)
'''