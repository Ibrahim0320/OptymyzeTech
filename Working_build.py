# This file will contain all the code that eventually works from all the different test sections
# This can hopefully become the final project

from pdfminer.high_level import extract_text



cv= "/Users/muhammadibrahim/Desktop/Blue Neutral Simple Minimalist Professional Web Developer Resume.pdf"
cv2= "/Users/muhammadibrahim/Desktop/Applications/Muhammad Ibrahim CV.pdf"

text_from_cv= extract_text(cv)



from fuzzywuzzy import process

def parse_resume_sections(text):
    # Define section keywords
    section_keywords = [
        "work experience", 
        "education", 
        "skills", 
        "qualifications"
        "languages", 
        "extracurricular courses and certificates", 
        "relevant projects"
    ]

    # Initialize variables to store parsed sections
    sections = {}
    current_section = None
    current_content = []


    # Extract candidate's name and contact information
    candidate_info = text.split('\n\n')[0]  
    # Assuming the candidate's name and contact information are in the first paragraph
    # Add candidate's name and contact information to the sections dictionary
    sections['candidate_info'] = candidate_info


    # Iterate through each line of the text
    for line in text.split("\n"):
        # Check if the line contains a section keyword
        match = process.extractOne(line.lower(), section_keywords)
        if match is not None and match[1] >= 90:  # Consider a match if similarity is >= 90
            # If a new section is encountered, store the content of the previous section
            if current_section is not None:
                sections[current_section] = "\n".join(current_content)
            # Update the current section
            current_section = match[0]  # Use the matched keyword
            current_content = []
        # If the line does not contain a section keyword, append it to the current section's content
        else:
            if current_section is not None:
                current_content.append(line)

    # Store the content of the last section
    if current_section is not None:
        sections[current_section] = "\n".join(current_content)

    return sections

# Example usage:

parsed_sections = parse_resume_sections(text_from_cv)

def print_section(parsed_sections, section_name):
    if section_name.lower() in parsed_sections:
        print(parsed_sections[section_name.lower()])
    else:
        print(f"{section_name.capitalize()} section not found.")

# Example usage:
#print_section(parsed_sections, 'language')

# Print the parsed sections
#for section, content in parsed_sections.items():
#    print(f"{section}:\n{content}\n")
