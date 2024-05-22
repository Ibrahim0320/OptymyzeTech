# Working on the cv scanner part of the project, attempting to get a clean output of the whole cv
# either in text form to be put later into a pipeline and section processer
# or in the respective sections from the get-go

pdf_path = "/Users/muhammadibrahim/Downloads/Blue Neutral Simple Minimalist Professional Web Developer Resume.pdf"

import pdfplumber

def extract_text_sections(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        cv_sections = []
        for page in pdf.pages:
            page_text = page.extract_text()
            # Define section headers to search for
            section_headers = ["Contact", "Skills", "Work Experience", "Educational Background", "Extracurricular Activities"]
            # Initialize variables to store section content
            current_section = None
            current_content = ""
            # Iterate through lines of text on the page
            for line in page_text.split("\n"):
                # Check if the line matches any of the section headers
                if any(header in line for header in section_headers):
                    # If a new section is detected, store the current content (if any)
                    if current_section is not None:
                        cv_sections.append((current_section, current_content.strip()))
                    # Set the current section to the detected header
                    current_section = line.strip()
                    # Reset the content for the new section
                    current_content = ""
                else:
                    # Append the line to the current section content
                    current_content += line + "\n"
            # Append the last section content after finishing the loop
            if current_section is not None:
                cv_sections.append((current_section, current_content.strip()))
    return cv_sections

# Example usage:
sections = extract_text_sections(pdf_path)
for header, content in sections:
    print(f"{header}:")
    print(content)
    print()
