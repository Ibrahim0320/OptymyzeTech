# Testing different stuff on the gpt API

import openai
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Who won the world series in 2020?"}]
    )
    print(response)
except openai.Error as e:
    print(f"OpenAI API error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
