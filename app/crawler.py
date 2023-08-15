# crawler.py

from goose3 import Goose
from goose3.network import NetworkError
import tiktoken

def extract_content(url):
	# Initialize Goose
	g = Goose()
	try:
		# Extract the article content
		article = g.extract(url=url)
		content = article.cleaned_text
		if content:
			# Tokenize the content using tiktoken
			enc = tiktoken.get_encoding("cl100k_base")
			tokens = enc.encode(content)
			return content, len(tokens)
		else:
			return None, 0
	except NetworkError as e:
		# Handle network errors
		return None, 0

# Example usage
target_website = 'https://en.wikipedia.org/wiki/2005_Azores_subtropical_storm'    
content, token_count = extract_content(target_website)



