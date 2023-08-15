# notion.py

import requests
import json
from app.models.user import User
from app.models.prompt import Prompt
from app.models.response import Response
from app.models.api_key import APIKey
from app import db

def save_response_to_notion(response_to_save, response_id, prompt_text, user_id):

    notion_api_key_record = APIKey.query.filter_by(user_id=user_id, api_type='notionKey').first()
    notion_api_key = notion_api_key_record.api_key if notion_api_key_record else None
    print("Notion API Key:", notion_api_key)

    notion_db_id_record = APIKey.query.filter_by(user_id=user_id, api_type='notionDbId').first()
    notion_db_id = notion_db_id_record.api_key if notion_db_id_record else None
    print("Notion Database Key:", notion_db_id)

    # Set up the headers for the request
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    
    target_website = response_to_save.target_website
    prompt_text = response_to_save.prompt_text

    properties_dict = {
        "Response ID": {
            "number": [{"text": {"content": str(response_id)}}]
        },
        "Target Website": {
            "title": [{"text": {"content": target_website}}]
        },
        "Prompt": {
            "rich_text": [{"text": {"content": prompt_text}}]
        },
        "Response": {
            "rich_text": [{"text": {"content": response_to_save.response_text}}]
        }
    }

    # Set up the body with the properties you want to include
    body = {
        "parent": {"database_id": notion_db_id},
        "properties": properties_dict,
    }

    # Send the request to create the new page
    response = requests.post(
        "https://api.notion.com/v1/pages",
        headers=headers,
        data=json.dumps(body),
    )

    if response.status_code == 200:
        print("Saved to Notion!")
        return "Saved to Notion!"
    else:
        print("Error saving to Notion:", response.text)
        return "Error saving to Notion:", response.text