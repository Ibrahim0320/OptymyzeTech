# Working out a function to open all cvs in a folder using an iterative method

import os
from Working_build import *
from Cv_info_storage import *



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

test_folder= "/Users/muhammadibrahim/Desktop/Test"


