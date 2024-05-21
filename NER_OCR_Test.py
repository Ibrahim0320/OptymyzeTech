# Combining OCR and NER on Spacy to extract entities from CVs to make a summarisable database

from pdf2image import convert_from_path
import pytesseract
import spacy
import os

# Load your custom spaCy model
nlp = spacy.load('NER_model_v2')
# Load a pre-trained generic model
nlp = spacy.load('en_core_web_sm')


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
