# Connecting to GPT and moving the top files into the final assessment stage

import openai

def analyze_cvs_with_gpt4(api_key, job_description, cvs):
    # Set up the OpenAI API key
    openai.api_key = api_key

    # Prepare the prompt for GPT-4
    prompt = f"Job Description: {job_description}\n\n"
    prompt += "CVs:\n"
    for idx, (filename, text) in enumerate(cvs, start=1):
        prompt += f"\n{idx}. Filename: {filename}, CV Content: {text}\n"
    prompt += "\nRank the CVs based on their suitability for the job described above."

    # Connect to GPT-4 and get the analysis
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",  # Replace with the GPT-4 engine ID once available
            prompt=prompt,
            max_tokens=1024,
            temperature=0.5
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
api_key = 'your-openai-api-key'
job_description = 'Senior Quality Assurance Engineer... (job description here)'
top_cvs = [('cv1.pdf', 'Content of CV 1...'), ('cv2.pdf', 'Content of CV 2...')]  # Assume these are the top CVs

result = analyze_cvs_with_gpt4(api_key, job_description, top_cvs)
print("GPT-4 Analysis Result:")
print(result)
