username = 'yiskah.scientia@gmail.com'
password = 'ywf7ZBY_jhu.rjw*pac'

# import scrapy
# from scrapy.crawler import CrawlerProcess

# # Login information
# # username = 
# # password = 

# # Login URL
# login_url = 'https://auth.galvanize.com/sign_in'

# # Target URL
# target_url = 'https://learn-2.galvanize.com/cohorts/3646/blocks/1032/content_files/fundamentals/fundamentals-vocabulary.md'

# # class GalvanizeSpider(scrapy.Spider):
#     # name = 'galvanize_spider'

#     # def start_requests(self):
#     #     # Start by logging in to Galvanize
#     #     yield scrapy.FormRequest(
#     #         url=login_url,
#     #         formdata={'username': username, 'password': password},
#     #         callback=self.parse
#     #     )

#     # def parse(self, response):
#     #     # Check if login was successful
#     #     if 'Invalid' in response.text:
#     #         self.log('Login failed')
#     #     else:
#     #         # If login was successful, navigate to the target URL and extract the content
#     #         yield scrapy.Request(target_url, callback=self.parse_content)

#     # def parse_content(self, response):
#     #     # Extract the text content from the page
#     #     text_content = response.css('body').get()

#     #     # Extract the image content from the page
#     #     image_urls = response.css('img::attr(src)').getall()

#     #     # Print the text content and image URLs
#     #     print(text_content)
#     #     print(image_urls)

# class GalvanizeSpider(scrapy.Spider):
#     name = "galvanize"
#     start_urls = [
#         'https://learn-2.galvanize.com/cohorts/3646/blocks/1032/content_files/fundamentals/fundamentals-vocabulary.md'
#     ]

#     def parse(self, response):
#         for selector in response.css('p, img'):
#             # Extract text from <p> tags
#             if selector.css('p'):
#                 yield {
#                     'text': selector.css('p::text').get()
#                 }
#             # Extract image URLs from <img> tags
#             elif selector.css('img'):
#                 yield {
#                     'image_url': selector.css('img::attr(src)').get()
#                 }


# # Run the spider
# process = CrawlerProcess()
# process.crawl(GalvanizeSpider)
# process.start()

# import scrapy
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# import os

# # Login information
# # username = 
# # password = 

# # Login URL
# login_url = 'https://auth.galvanize.com/sign_in'

# # Target URL
# target_url = 'https://learn-2.galvanize.com/cohorts/3646/blocks/1032/content_files/fundamentals/fundamentals-vocabulary.md'


# class GalvanizeSpider(scrapy.Spider):
#     name = "galvanize"
#     start_urls = [
#         target_url,
#     ]

#     def parse(self, response):
#         items = []
#         for selector in response.css('p, img'):
#             # Extract text from <p> tags
#             if selector.css('p'):
#                 items.append({
#                     'text': selector.css('p::text').get()
#                 })
#             # Extract image URLs from <img> tags
#             elif selector.css('img'):
#                 items.append({
#                     'image_url': selector.css('img::attr(src)').get()
#                 })
#         return items


# # Run the spider
# process = CrawlerProcess(get_project_settings())
# result = process.crawl(GalvanizeSpider)
# result.addCallback(lambda items: print(f"Scraped {len(items)} items."))
# process.start()

# # Save scraped data to an HTML file
# items = result.result
# html_output = "<html><body>"
# for item in items:
#     if 'text' in item:
#         html_output += f"<p>{item['text']}</p>"
#     elif 'image_url' in item:
#         html_output += f"<img src='{item['image_url']}'></img>"
# html_output += "</body></html>"
# print(item)

# with open("output.html", "w") as f:
#     f.write(html_output)
#     print("Scraped data saved to output.html.")


import requests
from bs4 import BeautifulSoup

# Set the URL
url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'

# Make the request and get the HTML content
response = requests.get(url)
html_content = response.content

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the first <p> tag and print its content
first_paragraph = soup.find('p')
print(first_paragraph.text)


# import os
# import openai

# openai.api_key = "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"

# response = openai.Completion.create(model="text-davinci-003", prompt="First say this is a test and then tell me a joke about Ada", temperature=0, max_tokens=2048)
# if 'choices' in response and len(response['choices']) > 0 and 'text' in response['choices'][0]:
#     print(response['choices'][0]['text'])
# else:
#     print('No text generated.')

# import openai

# # Set up your API key as shown above

# # Read in the MHTML file
# with open("/Users/jessica/Ada/FundamentalsVocabulary.html", "r") as file:
#     mhtml_content = file.read()

# # Send a prompt to the API using the MHTML content as the context
# prompt = "What is the main topic of this article?\n\n" + mhtml_content
# response = openai.Completion.create(
#     engine="davinci",
#     prompt=prompt,
#     temperature=0.5,
#     max_tokens=100,
#     n=1,
#     stop=None,
#     timeout=30,
# )

# # Print the generated text
# print(response.choices[0].text)


import requests
from bs4 import BeautifulSoup
from transformers import GPT2Tokenizer

# Set up the tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Set up the OpenAI API endpoint and authentication headers
openai_url = 'https://api.openai.com/v1/chat/completions'
openai_auth = {'Authorization': "import json
from datetime import datetime, timedelta
import os
import pytz
import re
import html

file_path = 'json/messages.json'
output_folder_path = 'Chat-Log'

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def add_time_component(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    eastern_tz = pytz.timezone('America/New_York')
    date_with_time = eastern_tz.localize(datetime.combine(date_obj, datetime.min.time()))
    return date_with_time.isoformat()

def get_date_range(start_date_str, end_date_str):
    start_date_iso = add_time_component(start_date_str)
    end_date_iso = add_time_component(end_date_str)
    start_date = datetime.fromisoformat(start_date_iso)
    end_date = datetime.fromisoformat(end_date_iso)
    return start_date.date(), end_date.date()

def generate_date_list(start_date, end_date):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
    return dates

def format_date_time(arrival_time):
    try:
        arrival_datetime_utc = datetime.fromisoformat(arrival_time[:-1]).replace(tzinfo=pytz.utc)
        eastern_tz = pytz.timezone('America/New_York')
        arrival_datetime_ny = arrival_datetime_utc.astimezone(eastern_tz)
        formatted_datetime = arrival_datetime_ny.strftime('%H:%M:%S')
        return formatted_datetime
    except ValueError:
        return arrival_time

def save_messages_to_file(messages_to_print, file_path, formatted_date_str):
    if not messages_to_print:
        return

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"[{formatted_date_str}]\n\n")
        for message_info in messages_to_print:
            formatted_datetime, sender, formatted_reply_content = message_info
            file.write(f'{formatted_datetime} - {sender}:\n')
            file.write(f'{formatted_reply_content}\n\n')

def decode_html_entities(text):
    return html.unescape(text)

def extract_and_format_quote(message_content):
    start_tag = "<quote"
    end_tag = "</quote>"
    quote_start = message_content.find(start_tag)
    if quote_start == -1:
        return None, message_content
    quote_end = message_content.find(end_tag, quote_start)
    if quote_end == -1:
        return None, message_content

    author_match = re.search(r'authorname="([^"]+)"', message_content)
    quote_text_match = re.search(r'</legacyquote>(.*?)$', message_content, re.DOTALL)

    author = author_match.group(1)

    quoted_text = quote_text_match.group()
    quoted_text = quoted_text.replace('<<< </legacyquote></quote>', 'Reply: \n')
    quoted_text = quoted_text.replace('</legacyquote>', f'"{author}: ')
    quoted_text = quoted_text.replace('<legacyquote>', '"')

    if not quoted_text:
        return None

    quote_reply = f'Quote: \n {quoted_text}'


    return quote_reply, quoted_text  # Return both quote_reply and quoted_text

def format_edited_message(content):
    print(f"content: {content}")
    edited = re.sub(r'<e_m[^>]*>.*?</e_m>', '', content)

    return f"~Edited~ \n {edited}"

def extract_call_duration(properties_json):
    try:
        properties = json.loads(properties_json)
        start_time = datetime.fromisoformat(properties['startTime'][:-1])
        end_time = datetime.fromisoformat(properties['endTime'][:-1])
        duration = end_time - start_time
        return duration
    except (json.JSONDecodeError, KeyError, ValueError):
        return None

def format_call_logs(content):
    started_match = re.search(r'<partlist type="started".*?<name>(.*?)<\/name>', content, re.DOTALL)
    ended_match = re.search(r'<partlist type="ended".*?<name>(.*?)<\/name>.*?<duration>(.*?)<\/duration>', content, re.DOTALL)

    if started_match:
        caller = started_match.group(1)
        return f"~{caller} started a call~"
    elif ended_match:
        caller = ended_match.group(1)
        duration_str = ended_match.group(2)
        duration = timedelta(seconds=float(duration_str))
        duration_formatted = str(duration).split('.')[0]  # Remove microseconds part
        return f"~Call ended~ \n Call duration: {duration_formatted}"
    else:
        return None

import os

def extract_and_format_image_links(content):
    uri_objects = re.findall(r'<URIObject[^>]*?uri="(.*?)"[^>]*>', content)
    if not uri_objects:
        return None

    formatted_image_links = []
    for uri_object in uri_objects:
        file_name = os.path.basename(uri_object)
        image_link = f'Image: media/{file_name}'
        formatted_image_links.append(image_link)

    return '\n'.join(formatted_image_links)



def print_messages_by_date(json_data, dates, output_folder_path):
    conversations = json_data.get('conversations', [])

    for date in dates:
        year_folder_path = os.path.join(output_folder_path, str(date.year))
        month_folder_path = os.path.join(year_folder_path, date.strftime('%B_%Y'))

        messages_to_print = []
        for conversation in conversations:
            messages = conversation.get('MessageList', [])
            for message in messages:
                original_arrival_time = message.get('originalarrivaltime')
                if original_arrival_time:
                    try:
                        arrival_datetime = datetime.fromisoformat(original_arrival_time[:-1])
                    except ValueError:
                        continue

                    message_date = arrival_datetime.date()
                    if message_date == date:
                        formatted_datetime = format_date_time(message["originalarrivaltime"])
                        sender = decode_html_entities(message.get("from", ""))
                        content = decode_html_entities(message.get("content", ""))
                        
                        if content.strip():  # Check if content is not empty after stripping leading/trailing whitespace
                            if "<partlist" in content:
                                formatted_call_log = format_call_logs(content)
                                if formatted_call_log:
                                    messages_to_print.append((formatted_datetime, sender, formatted_call_log))
                            elif "Call Logs for Call" in content:
                                break
                            elif "<URIObject" in content:
                                formatted_reply_content = extract_and_format_image_links(content)
                                if formatted_reply_content:
                                    messages_to_print.append((formatted_datetime, sender, formatted_reply_content))
                            elif "</e_m>" in content:
                                formatted_edit_content = format_edited_message(content)
                                if formatted_edit_content:
                                    messages_to_print.append((formatted_datetime, sender, formatted_edit_content))
                            else:
                                quote_reply, quoted_text = extract_and_format_quote(content)
                                if quote_reply:
                                    messages_to_print.append((formatted_datetime, sender, quote_reply))
                                else:
                                    messages_to_print.append((formatted_datetime, sender, content))


        # Sort messages by originalarrivaltime in chronological order
        messages_to_print.sort(key=lambda x: datetime.strptime(x[0], '%H:%M:%S'))

        # Save messages to the output file if there are any messages to print
        if messages_to_print:
            create_folder_if_not_exists(year_folder_path)
            create_folder_if_not_exists(month_folder_path)

            day_file_path = os.path.join(month_folder_path, date.strftime('%m_%d.md'))
            formatted_date_str = date.strftime('%A %B %d, %Y')
            save_messages_to_file(messages_to_print, day_file_path, formatted_date_str)


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def main():
    json_data = load_json_data(file_path)

    start_date_str = '2023-06-12'
    end_date_str = '2023-06-13'
    start_date, end_date = get_date_range(start_date_str, end_date_str)
    dates_to_print = generate_date_list(start_date, end_date)

    print_messages_by_date(json_data, dates_to_print, output_folder_path)

if __name__ == "__main__":
    main()
"}

# Set up the HTML parser
def parse_html(file_path):
    with open(file_path, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

                # Remove unwanted text
        unwanted_text = [
            "Branches",
            "NEXT:",
            "Problem Set: Git",
            "Ada C19 Zoisite Class",
            "JA",
            "Jessica Anderson",
            "My Account",
            "yiskah.scientia@gmail.com",
            "Sign Out",
            "CurriculumResources",
            "Branches In GitBranchesUsing BranchesProblem Set: GitActivity: Merge CarnivalUsing Branches",
            "save",
            "© 2013 - 2023 Galvanize, Inc.",
            "Privacy Policy",
            "Terms of Use",
            "Galvanize",
            "info@galvanize.com",
            "Reset InputCHECK"
        ]
        
        for text in unwanted_text:
            for element in soup(text=text):
                element.extract()

        text = soup.get_text()
        return text.strip()

# Split the text into segments of max length 2048
def split_text(text, max_len=3000):
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]

# Generate a summary for each segment of text
def generate_summary(text_segment):
    # print("Text to be summarized:")
    # print(text_segment)
    # print("\n")

    # Structure the payload for chat-based models
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'system',
                'content': 'You are a helpful assistant that summarizes text.'
            },
            {
                'role': 'user',
                'content': f'Summarize the following text: {text_segment}'
            }
        ],
        'max_tokens': 3000,  # Adjust max_tokens according to your needs
        'temperature': 0.5,
    }

    response = requests.post(openai_url, headers=openai_auth, json=payload)
    # print(response.status_code)  # Add this line to print the status code
    # print(response.json())  # Add this line to print the response content

    if 'choices' not in response.json():
        print("Error: 'choices' not found in response")
        return ""

    summary = response.json()['choices'][0]['message']['content'].strip()
    return summary

# Generate a summary for each HTML file
def summarize_file(file_path):
    text = parse_html(file_path)
    print("Text to be summarized:")
    print(text)
    print("\n")

    segments = split_text(text)
    summaries = [generate_summary(segment) for segment in segments]
    summary = ' '.join(summaries)
    return summary

# Example usage
file_path = "/Users/jessica/Ada/UsingBranches.html"
summary = summarize_file(file_path)
print("Final summary:")
print(summary)
