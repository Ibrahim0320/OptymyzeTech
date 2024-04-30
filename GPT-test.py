# Testing different stuff on the gpt API

import openai
import os

# Set the API key for OpenAI
openai.api_key = 'api-key'

try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Who won the world series in 2020?"}]
    )
    print(response)
except Exception as e:
    print(f"An error occurred: {e}")




