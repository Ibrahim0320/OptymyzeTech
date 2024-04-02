from pyresparser import ResumeParser
from docx import Document
import os 
from pdf2docx import Converter

cv = "/Users/muhammadibrahim/Downloads/Blue Neutral Simple Minimalist Professional Web Developer Resume.pdf"
'''
try:
    try:
        doc = Document()
        with open(cv, 'r') as file:
         doc.add_paragraph(file.read())
        doc.save('text.docx')
        data= ResumeParser('text.docx').get_extracted_data()
        print(data)
    except:
        data= ResumeParser('text.docx').get_extracted_data()
        print(data)
except Exception as e:
    print(f"An error occurred: {e}")
'''
'''
from pyresparser import ResumeParser
from docx import Document
from pdf2docx import Converter

file_path = "/Users/muhammadibrahim/Downloads/Blue Neutral Simple Minimalist Professional Web Developer Resume.pdf"

try:
    if file_path.endswith('.pdf'):
        # Convert PDF to DOCX and then parse
        try:
            # Convert PDF to DOCX
            docx_file_path = 'converted_resume.docx'
            cv = Converter(file_path)
            cv.convert(docx_file_path, start=0, end=None)
            cv.close()

            # Parse the converted DOCX file
            data = ResumeParser(docx_file_path).get_extracted_data()
            print(data)
        except Exception as e:
            print(f"Error converting PDF to DOCX: {e}")
    else:
        # Parse the DOCX file directly
        data = ResumeParser(file_path).get_extracted_data()
        print(data)

except Exception as e:
    print(f"An error occurred: {e}")
'''

from pdfminer.high_level import extract_text
text= extract_text(cv)
print(text)
