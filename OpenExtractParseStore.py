# Working out a function to open all cvs in a folder using an iterative method

import os
from Working_build import *
from Cv_info_storage import *
import re


# Function to iterate through CV files in a folder
def iterate_over_cv_folder_extract_and_parse_and_store(folder_path):
    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):  # Assuming CVs are in PDF format
            cv_path = os.path.join(folder_path, filename)
            # Extract text from the CV
            cv_text = extract_text(cv_path)
            # Parse CV sections 
            parsed_sections = parse_resume_sections(cv_text)
            # Insert parsed CV sections into the SQLite database
            insert_cv_data(parsed_sections)

test_folder= "Test"


def extract_text_from_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        text = file.read()
    return text

def extract_candidate_names(cv_text):
    # Define a regular expression pattern to match candidate names
    name_pattern = re.compile(r'^\s*([A-Z][a-z]+(?: [A-Z][a-z]+)*)', re.MULTILINE)
    # Extract candidate names from the text
    candidate_names = name_pattern.findall(cv_text)
    return candidate_names

# Modify the function to use extract_candidate_names
def iterate_over_cv_folder_extract_and_parse_and_store_new(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            cv_path = os.path.join(folder_path, filename)
            cv_text = extract_text_from_file(cv_path)
            candidate_names = extract_candidate_names(cv_text)
            print("Candidate Names:", candidate_names)

# Call the function to process CVs in the folder
cv_folder_path = "Test"
if os.path.isdir(cv_folder_path):
    iterate_over_cv_folder_extract_and_parse_and_store_new(cv_folder_path)
else:
    print("Error: Invalid CV folder path!")
