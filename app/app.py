# username = 'yiskah.scientia@gmail.com'
# password = 'ywf7ZBY_jhu.rjw*pac'

# import requests
# from bs4 import BeautifulSoup
# from transformers import GPT2Tokenizer

# # Set up the tokenizer
# tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# # Set up the OpenAI API endpoint and authentication headers
# openai_url = 'https://api.openai.com/v1/chat/completions'
# # openai_auth = {'Authorization': "import json

# # Set up the HTML parser
# def parse_html(file_path):
#     with open(file_path, 'r') as file:
#         soup = BeautifulSoup(file, 'html.parser')

#                 # Remove unwanted text
#         unwanted_text = [
#             "Branches",
#             "NEXT:",
#             "Problem Set: Git",
#             "Ada C19 Zoisite Class",
#             "JA",
#             "Jessica Anderson",
#             "My Account",
#             "yiskah.scientia@gmail.com",
#             "Sign Out",
#             "CurriculumResources",
#             "Branches In GitBranchesUsing BranchesProblem Set: GitActivity: Merge CarnivalUsing Branches",
#             "save",
#             "© 2013 - 2023 Galvanize, Inc.",
#             "Privacy Policy",
#             "Terms of Use",
#             "Galvanize",
#             "info@galvanize.com",
#             "Reset InputCHECK"
#         ]
        
#         for text in unwanted_text:
#             for element in soup(text=text):
#                 element.extract()

#         text = soup.get_text()
#         return text.strip()

# # Split the text into segments of max length 2048
# def split_text(text, max_len=3000):
#     return [text[i:i+max_len] for i in range(0, len(text), max_len)]

# # Generate a summary for each segment of text
# def generate_summary(text_segment):
#     # print("Text to be summarized:")
#     # print(text_segment)
#     # print("\n")

#     # Structure the payload for chat-based models
#     payload = {
#         'model': 'gpt-3.5-turbo',
#         'messages': [
#             {
#                 'role': 'system',
#                 'content': 'You are a helpful assistant that summarizes text.'
#             },
#             {
#                 'role': 'user',
#                 'content': f'Summarize the following text: {text_segment}'
#             }
#         ],
#         'max_tokens': 3000,  # Adjust max_tokens according to your needs
#         'temperature': 0.5,
#     }

#     response = requests.post(openai_url, headers=openai_auth, json=payload)
#     # print(response.status_code)  # Add this line to print the status code
#     # print(response.json())  # Add this line to print the response content

#     if 'choices' not in response.json():
#         print("Error: 'choices' not found in response")
#         return ""

#     summary = response.json()['choices'][0]['message']['content'].strip()
#     return summary

# # Generate a summary for each HTML file
# def summarize_file(file_path):
#     text = parse_html(file_path)
#     print("Text to be summarized:")
#     print(text)
#     print("\n")

#     segments = split_text(text)
#     summaries = [generate_summary(segment) for segment in segments]
#     summary = ' '.join(summaries)
#     return summary

# # Example usage
# file_path = "/Users/jessica/Ada/UsingBranches.html"
# summary = summarize_file(file_path)
# print("Final summary:")
# print(summary)
