# This file will take in the names of specific candidates and will then open the CV folder to find, select, and
# upload the relevant CV pdf files onto GPT4 in order to find out how GPT4 ranks these potential candidates

import os
import requests
import PyPDF2

# Constants
OPENAI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"  # OpenAI GPT-4 API endpoint
OPENAI_API_KEY = "sk-proj-mKY2RwX6ugxJ2gwfqFA2T3BlbkFJlpWrV5O8iww5V2w4iFaI"  # Securely handle your API key
FOLDER_PATH = "Test"
NAMES = ["Hamza bin Saleem", "Muhammad Usman", "Umer Ehsan"]  # Names you're looking for

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:  # Only add if text was found
                text.append(page_text)
        return '\n'.join(text)

def find_cv_files(names, folder_path):
    """Finds CV files matching given names."""
    cv_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            for name in names:
                if name.lower() in file.lower() and file.endswith(".pdf"):
                    cv_files.append(os.path.join(root, file))
    return cv_files

def analyze_with_gpt4(text):
    """Sends extracted text to GPT-4 and gets analysis."""
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "system", "content": "Analyze the following CV:"},
                     {"role": "user", "content": text}]
    }
    response = requests.post(OPENAI_API_ENDPOINT, headers=headers, json=data)
    return response.json()

def main():
    cv_files = find_cv_files(NAMES, FOLDER_PATH)
    if cv_files:
        for file_path in cv_files:
            text = extract_text_from_pdf(file_path)
            result = analyze_with_gpt4(text)
            print(result)  # Printing each candidate's analysis results
    else:
        print("No CVs found for the given names.")

if __name__ == "__main__":
    main()
