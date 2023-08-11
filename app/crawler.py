# # username = 'yiskah.scientia@gmail.com'
# # password = 'ywf7ZBY_jhu.rjw*pac'

# # import scrapy
# # from scrapy.crawler import CrawlerProcess

# # # Login information
# # # username = 
# # # password = 

# # # Login URL
# # login_url = 'https://auth.galvanize.com/sign_in'

# # # Target URL
# # target_url = 'https://learn-2.galvanize.com/cohorts/3646/blocks/1032/content_files/fundamentals/fundamentals-vocabulary.md'

# # # class GalvanizeSpider(scrapy.Spider):
# #     # name = 'galvanize_spider'

# #     # def start_requests(self):
# #     #     # Start by logging in to Galvanize
# #     #     yield scrapy.FormRequest(
# #     #         url=login_url,
# #     #         formdata={'username': username, 'password': password},
# #     #         callback=self.parse
# #     #     )

# #     # def parse(self, response):
# #     #     # Check if login was successful
# #     #     if 'Invalid' in response.text:
# #     #         self.log('Login failed')
# #     #     else:
# #     #         # If login was successful, navigate to the target URL and extract the content
# #     #         yield scrapy.Request(target_url, callback=self.parse_content)

# #     # def parse_content(self, response):
# #     #     # Extract the text content from the page
# #     #     text_content = response.css('body').get()

# #     #     # Extract the image content from the page
# #     #     image_urls = response.css('img::attr(src)').getall()

# #     #     # Print the text content and image URLs
# #     #     print(text_content)
# #     #     print(image_urls)

# # class GalvanizeSpider(scrapy.Spider):
# #     name = "galvanize"
# #     start_urls = [
# #         'https://learn-2.galvanize.com/cohorts/3646/blocks/1032/content_files/fundamentals/fundamentals-vocabulary.md'
# #     ]

# #     def parse(self, response):
# #         for selector in response.css('p, img'):
# #             # Extract text from <p> tags
# #             if selector.css('p'):
# #                 yield {
# #                     'text': selector.css('p::text').get()
# #                 }
# #             # Extract image URLs from <img> tags
# #             elif selector.css('img'):
# #                 yield {
# #                     'image_url': selector.css('img::attr(src)').get()
# #                 }


# # # Run the spider
# # process = CrawlerProcess()
# # process.crawl(GalvanizeSpider)
# # process.start()

# # import scrapy
# # from scrapy.crawler import CrawlerProcess
# # from scrapy.utils.project import get_project_settings
# # import os

# # # Login information
# # # username = 
# # # password = 

# # # Login URL
# # login_url = 'https://auth.galvanize.com/sign_in'

# # # Target URL
# # target_url = 'https://learn-2.galvanize.com/cohorts/3646/blocks/1032/content_files/fundamentals/fundamentals-vocabulary.md'


# # class GalvanizeSpider(scrapy.Spider):
# #     name = "galvanize"
# #     start_urls = [
# #         target_url,
# #     ]

# #     def parse(self, response):
# #         items = []
# #         for selector in response.css('p, img'):
# #             # Extract text from <p> tags
# #             if selector.css('p'):
# #                 items.append({
# #                     'text': selector.css('p::text').get()
# #                 })
# #             # Extract image URLs from <img> tags
# #             elif selector.css('img'):
# #                 items.append({
# #                     'image_url': selector.css('img::attr(src)').get()
# #                 })
# #         return items


# # # Run the spider
# # process = CrawlerProcess(get_project_settings())
# # result = process.crawl(GalvanizeSpider)
# # result.addCallback(lambda items: print(f"Scraped {len(items)} items."))
# # process.start()

# # # Save scraped data to an HTML file
# # items = result.result
# # html_output = "<html><body>"
# # for item in items:
# #     if 'text' in item:
# #         html_output += f"<p>{item['text']}</p>"
# #     elif 'image_url' in item:
# #         html_output += f"<img src='{item['image_url']}'></img>"
# # html_output += "</body></html>"
# # print(item)

# # with open("output.html", "w") as f:
# #     f.write(html_output)
# #     print("Scraped data saved to output.html.")


# import requests
# from bs4 import BeautifulSoup

# # Set the URL
# url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

# # Make the request and get the HTML content
# response = requests.get(url)
# html_content = response.content

# # Parse the HTML content with BeautifulSoup
# soup = BeautifulSoup(html_content, 'html.parser')

# # Find the first <p> tag and print its content
# first_paragraph = soup.find('p')
# print(first_paragraph.text)


# # import os
# # import openai

# # response = openai.Completion.create(model="text-davinci-003", prompt="First say this is a test and then tell me a joke about Ada", temperature=0, max_tokens=2048)
# # if 'choices' in response and len(response['choices']) > 0 and 'text' in response['choices'][0]:
# #     print(response['choices'][0]['text'])
# # else:
# #     print('No text generated.')

# # import openai

# # # Set up your API key as shown above

# # # Read in the MHTML file
# # with open("/Users/jessica/Ada/FundamentalsVocabulary.html", "r") as file:
# #     mhtml_content = file.read()

# # # Send a prompt to the API using the MHTML content as the context
# # prompt = "What is the main topic of this article?\n\n" + mhtml_content
# # response = openai.Completion.create(
# #     engine="davinci",
# #     prompt=prompt,
# #     temperature=0.5,
# #     max_tokens=100,
# #     n=1,
# #     stop=None,
# #     timeout=30,
# # )

# # # Print the generated text
# # print(response.choices[0].text)


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
#         unwanted_text = []
        
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
