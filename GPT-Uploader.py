# This file will take in the names of specific candidates and will then open the CV folder to find, select, and
# upload the relevant CV pdf files onto GPT4 in order to find out how GPT4 ranks these potential candidates

import os
import PyPDF2
import openai

# CONSTANTS
OPENAI_API_KEY = 'sapi-key here'
FOLDER_PATH = "Test"
NAMES = ["Hamza bin Saleem", "Muhammad Usman", "Umer Ehsan"]

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




Assignment= '''
Here is a job description. Senior Quality Assurance Engineer We are on the hunt for an exceptional Senior QA Engineer to join and elevate our team.
This role is perfect for someone who is not just looking for a job but an opportunity to make a significant impact. 
Key Responsibilities: Develop, enhance, and maintain both front-end and back-end automated testing frameworks using 
cutting-edge tools and technologies, alongside conducting manual testing when necessary.Take charge of our CI/CD 
processes, crafting a comprehensive test strategy, and embedding quality standards within automated pipelines.
Define, track, and optimize quality and performance metrics for our applications to ensure they meet our high standards.
Lead by example, reviewing test procedures and mentoring team members on best practices in automated testing. 
Serve as the linchpin for quality control, ensuring application changes meet our rigorous standards for excellence.
Requirements: Proven track record as a Quality Assurance Engineer, boasting a deep understanding of automated testing
frameworks for both front-end (e.g., Playwright) and back-end (e.g., xUnit) development. 
Experience with AWS DevOps, cloud services, and an ability to seamlessly integrate test cases into comprehensive 
suites for automation.Familiarity with test design, methodologies, and tools, with ISTQB or similar certifications
being a huge plus. A strong team player with outstanding analytical abilities, you pride yourself on being 
independent, solution-focused, and proactive.Excellent communication skills in English, both verbal and written,
are essential. What We Offer: Competitive salaries that stand above market standards.Annual bonuses reflecting
both personal and company performance.A generous learning and development budget to support your professional
growth. 25 days of paid leave annually to ensure work-life balance.

I want you to take the following text from the potential candidates' CVs. Return to me a ranking 
of the most suitable candidates and why:
'''


def analyze_with_gpt4(text):
    """Analyzes CV text using OpenAI GPT-4."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": Assignment},
            {"role": "user", "content": text}
        ]
    )
    return response

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
