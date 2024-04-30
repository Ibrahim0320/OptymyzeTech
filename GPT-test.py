# Testing different stuff on the gpt API
import os
import requests

def query_gpt4(prompt):
    api_key = os.getenv()
    if not api_key:
        print("API key not found. Please set the OPENAI_API_KEY environment variable.")
        return None

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
    "model": "gpt-3.5-turbo",  # Replace "gpt-4" with an available model like "text-davinci-003"
    "prompt": prompt,
    "max_tokens": 150,
    "temperature": 0.7
    }

    try:
        print("Sending request to OpenAI...")
        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        print("Request successful, processing response...")
        json_response = response.json()
        print("JSON Response:", json_response)
        return json_response['choices'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f'HTTP Request failed: {e}')
        if hasattr(e, 'response'):
            print("Status Code:", e.response.status_code)
            print("Error Response:", e.response.text)
        return None

# Example usage
prompt = "Translate the following English text to French: 'Hello, how are you?'"
response = query_gpt4(prompt)
print("Response from GPT-4:", response if response else "No response received.")



