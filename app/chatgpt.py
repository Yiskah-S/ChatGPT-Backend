#  chatgpt.py

# from dotenv import load_dotenv
# import openai
# from app.models.api_key import APIKey

# # Load the .env file
# load_dotenv()

# def generate_response(user_id, prompt_text, content):
# 	# Retrieve the ChatGPT API key for the given user
# 	chatgpt_api_key_record = APIKey.query.filter_by(user_id=user_id, api_type='chatgptKey').first()
# 	chatgpt_api_key = chatgpt_api_key_record.api_key if chatgpt_api_key_record else None

# 	# Use the retrieved ChatGPT API key for the OpenAI API
# 	if chatgpt_api_key:
# 		openai.api_key = chatgpt_api_key
# 	else:
# 		return "API key not found"

# 	response_text = execute_prompt(prompt_text, content)
# 	return response_text

# def execute_prompt(prompt_text, content):
# 	payload = {
# 		'model': 'gpt-3.5-turbo',
# 		'messages': [
# 			{
# 				'role': 'system',
# 				'content': 'You are a helpful assistant.'
# 			},
# 			{
# 				'role': 'user',
# 				'content': f'{prompt_text}: {content}'
# 			}
# 		],
# 		'max_tokens': 3000,
# 		'temperature': 0.5,
# 	}

# 	response = openai.ChatCompletion.create(**payload)

# 	if 'choices' not in response:
# 		return "Response not found"

# 	response_text = response['choices'][0]['message']['content'].strip()
# 	return response_text

from dotenv import load_dotenv
import openai
from app.models.api_key import APIKey
import tiktoken

# Load the .env file
load_dotenv()

def generate_response(user_id, prompt_text, content, content_token_count): 
	# Retrieve the ChatGPT API key for the given user
	chatgpt_api_key_record = APIKey.query.filter_by(user_id=user_id, api_type='chatgptKey').first()
	chatgpt_api_key = chatgpt_api_key_record.api_key if chatgpt_api_key_record else None

	# Use the retrieved ChatGPT API key for the OpenAI API
	if chatgpt_api_key:
		openai.api_key = chatgpt_api_key
	else:
		return "API key not found"

	response_text = execute_prompt(prompt_text, content, content_token_count) 
	return response_text

def execute_prompt(prompt_text, content, content_token_count): 
	# Tokenize the prompt_text using tiktoken
	enc = tiktoken.get_encoding("cl100k_base")
	prompt_tokens = enc.encode(prompt_text)
	print(f"Prompt tokens: {len(prompt_tokens)}")
	# Calculate the maximum tokens
	max_tokens = 4097 - content_token_count - len(prompt_tokens) - 100
	print(f"Max tokens: {max_tokens}")

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
		'max_tokens': max_tokens, # Use the calculated value here
		'temperature': 0.5,
	}

	response = openai.ChatCompletion.create(**payload)

	if 'choices' not in response:
		return "Response not found"

	response_text = response['choices'][0]['message']['content'].strip()
	return response_text
