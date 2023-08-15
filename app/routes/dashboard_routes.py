# dashboard_routes.py 

from flask import send_file
from flask import Blueprint, jsonify, request, session
from flask_login import login_required, current_user
from app import db
from app.models.api_key import APIKey
from app.models.user import User
from app.models.prompt import Prompt
from app.crawler import extract_content
from app.chatgpt import generate_response
from app.notion import save_response_to_notion
from app.models.response import Response


dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard/<int:user_id>/')

@login_required
@dashboard_bp.route('/', methods=['POST'])
def run_crawler(user_id):
    data = request.get_json()
    print("Request body:", data)
    prompt_id = data.get('prompt_id')
    print("prompt_id:", prompt_id)
    target_website = data.get('targetWebsite')
    print("Got the stuff I need from the request body!")

    prompt_obj = Prompt.query.filter_by(user_id=user_id, id=prompt_id).first()
    print("Prompt object:", prompt_obj)
    if prompt_obj:
        prompt_text = prompt_obj.prompt
        print("Prompt_text:", prompt_text)

    # Extract content
    content = extract_content(target_website)
    print("Got the content!")

    # Generate response
    response_text = generate_response(user_id, prompt_text, content)
    print("Response text:", response_text)
    print("Got the response!")

    # Save the response in the database
    response_obj = Response(target_website=target_website, prompt_id=prompt_id, prompt_text=prompt_text, response_text=response_text, user_id=user_id)
    db.session.add(response_obj)
    db.session.commit()
    response_id = response_obj.id
    print("Response ID:", response_id)

    # Return both the response ID and the response text
    print(jsonify(message='Success', response_id=response_id, response=response_text))
    return jsonify(message='Success', response_id=response_id, response_text=response_text), 200


@login_required
@dashboard_bp.route('/save_notion/', methods=['POST'])
def save_to_notion(user_id):
    response_id = request.json.get('response_id')
    prompt_text = request.json.get('prompt_text')
    print("Response ID:", response_id)

    # Retrieve the response from the database
    response_to_save = Response.query.get(response_id)
    print("Response to save:", response_to_save)

    result = save_response_to_notion(response_to_save, response_id, prompt_text, user_id)
    print("Result:", result)

    return jsonify({"message": "Saved successfully"}), 200


@login_required
@dashboard_bp.route('/save_txt/', methods=['POST'])
def save_results_txt(user_id):
	response_id = request.json.get('response_id')
	response_to_save = Response.query.get(response_id)
	
	if response_to_save and response_to_save.user_id == user_id:
		return response_to_save.response_text
	else:
		return jsonify(message='No response to save or unauthorized access'), 400


@login_required
@dashboard_bp.route('/save_md/', methods=['POST'])
def save_results_md(user_id):
	response_id = request.json.get('response_id')
	response_to_save = Response.query.get(response_id)

	if response_to_save and response_to_save.user_id == user_id:
		return response_to_save.response_text
	else:
		return jsonify(message='No response to save or unauthorized access'), 400