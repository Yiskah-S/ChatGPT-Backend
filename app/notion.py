# notion.py

import requests
import json
from app.models.api_key import APIKey
from app import db
from app.models.response import Response
import logging

def save_response_to_notion(response_id, user_id):
    # Retrieve the response from the database
    response_to_save = Response.query.get(response_id)
    if response_to_save is None:
        return "Response not found"

    # Validation for required fields
    if not all([response_to_save.target_website, response_to_save.prompt_text, response_to_save.response_text]):
        return "Missing required fields in response"

    # Get Notion API Key and Database ID
    notion_api_key_record = APIKey.query.filter_by(user_id=user_id, api_type='notionKey').first()
    notion_db_id_record = APIKey.query.filter_by(user_id=user_id, api_type='notionDbId').first()

    if not notion_api_key_record or not notion_db_id_record:
        return "Notion API key or Database ID not found for user"

    notion_api_key = notion_api_key_record.api_key
    notion_db_id = notion_db_id_record.api_key

    # Set up the headers for the request
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    properties_dict = {
        "Response ID": {
            "number": response_id
        },
        "Target Website": {
            "title": [{"text": {"content": response_to_save.target_website}}]
        },
        "Prompt": {
            "rich_text": [{"text": {"content": response_to_save.prompt_text}}]
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
        logging.info("Saved to Notion!")
        return "Saved to Notion!"
    else:
        logging.error(f"Error saving to Notion: {response.text}")
        return f"Error saving to Notion: {response.text}"