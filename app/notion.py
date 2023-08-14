# notion.py

import requests
import json
from app.models.user import User
from app.models.prompt import Prompt
from app.models.response import Response
from app import db

def save_to_notion(response, user_id):
    print("Saving to Notion...")
    return "Saved to Notion!"


