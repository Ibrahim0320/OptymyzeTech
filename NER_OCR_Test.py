# Combining OCR and NER on Spacy to extract entities from CVs to make a summarisable database

from pdf2image import convert_from_path
import pytesseract

def convert_pdf_to_text(pdf_path):
    images = convert_from_path(pdf_path)
    full_text = []
    for image in images:
        text = pytesseract.image_to_string(image)
        full_text.append(text)
    return "\n".join(full_text)

