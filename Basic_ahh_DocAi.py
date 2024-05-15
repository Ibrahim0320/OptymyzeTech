# Building it form the very basics again just to see process and approach

from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account

def get_client():
    credentials = service_account.Credentials.from_service_account_file('beaming-mode-423311-q4-5e258468bd22.json')
    client = documentai.DocumentProcessorServiceClient(credentials=credentials)
    return client

client = get_client()



def process_document(file_path, client, processor_id):
    name = f'projects/your-project-id/locations/eu/processors/{processor_id}'

    # Read the file into memory
    with open(file_path, "rb") as f:
        content = f.read()

    # Configure the request with the content of the file
    request = {
        "name": name,
        "raw_document": {
            "content": content,
            "mime_type": "application/pdf"
        }
    }

    # Process the document
    result = client.process_document(request=request)

    # Print out the document text
    document = result.document
    print("Found text content:")
    for page in document.pages:
        for paragraph in page.paragraphs:
            # Access text using the text anchor's start and end index
            for segment in paragraph.layout.text_anchor.text_segments:
                start_index = segment.start_index
                end_index = segment.end_index if segment.end_index != -1 else len(document.text)
                paragraph_text = document.text[start_index:end_index]
                print(paragraph_text)


def main():
    processor_id = '9e0288e87d2654f5'
    file_path = 'Test1/Blue Neutral Simple Minimalist Professional Web Developer Resume.pdf'
    client = get_client()
    process_document(file_path, client, processor_id)

if __name__ == "__main__":
    main()
