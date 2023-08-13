# crawler.py

from goose3 import Goose
from goose3.network import NetworkError
import tiktoken

def extract_content(url):
	g = Goose()
	try:
		article = g.extract(url=url)
		content = article.cleaned_text
		if content:
			print("Page content retrieved:")
			# content = 'test'
			# print(content)
			
			# Tokenize the content using tiktoken
			enc = tiktoken.get_encoding("cl100k_base")
			tokens = enc.encode(content)
			print(f"Number of tokens in the content: {len(tokens)}")
		else:
			print("Failed to retrieve content.")
		return content
	except NetworkError as e:
		print(f"Network error when fetching URL {url}: {e}")
		return None

target_website = 'https://en.wikipedia.org/wiki/2005_Azores_subtropical_storm'    
# target_website = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
# target_website = 'https://www.addicted2decorating.com/diy-wainscoting-part-3-adding-a-tile-accent.html'
# target_website = 'https://arstechnica.com/gadgets/2023/08/zoom-updates-terms-of-service-to-clarify-that-it-wont-use-your-calls-to-train-ai/'
# content = extract_content(target_website)




