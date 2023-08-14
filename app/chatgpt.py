#  chatgpt.py

import os
from dotenv import load_dotenv
import openai
from app.models.api_key import APIKey

# Load the .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
print("OpenAI API Key:", openai.api_key)

def generate_response(user_id, prompt_text, content):
    print("Generating response...")
    print("User ID:", user_id)
    print("Prompt:", prompt_text)
    print("Content:", content)

    chatgpt_api_key_record = APIKey.query.filter_by(user_id=user_id, api_type='chatgptKey').first()
    chatgpt_api_key = chatgpt_api_key_record.api_key if chatgpt_api_key_record else None
    print("ChatGPT API Key:", chatgpt_api_key)

    response_text = execute_prompt(prompt_text, content)
    print("Response:", response_text)
    
    return response_text


def execute_prompt(prompt_text, content):
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'system',
                'content': 'You are a helpful assistant.'
            },
            {
                'role': 'user',
                'content': f'{prompt_text}: {content}'
            }
        ],
        'max_tokens': 3000,
        'temperature': 0.5,
    }

    response = openai.ChatCompletion.create(**payload)

    if 'choices' not in response:
        print("Error: 'choices' not found in response")
        return "Response not found"

    response_text = response['choices'][0]['message']['content'].strip()
    return response_text

