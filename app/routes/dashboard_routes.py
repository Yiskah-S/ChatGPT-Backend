# dashboard_routes.py 

from flask import Blueprint, jsonify, request, session
from flask_login import login_required, current_user
from app import db
from app.models.api_key import APIKey
from app.models.user import User
from app.models.prompt import Prompt
from app.crawler import extract_content
from app.chatgpt import generate_response
from app.notion import save_to_notion
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
    print("Got the response!")

    # Save the response in the database
    response_obj = Response(target_website=target_website, prompt_id=prompt_id, prompt_text=prompt_text, response_text=response_text, user_id=user_id)
    db.session.add(response_obj)
    db.session.commit()

    return jsonify(message='Success', response_id=response_obj.id), 200

@login_required
@dashboard_bp.route('/save/', methods=['POST'])
def save_results(user_id):
    response_id = request.json.get('response_id')
    print("Response ID:", response_id)
    output_format = request.json.get('outputFormat')
    print("Output format:", output_format)

    if not response_id or not output_format:
        return jsonify({"error": "Response ID and output format are required"}), 440

    # Retrieve the response from the database
    response_to_save = Response.query.get(response_id)

    if response_to_save and response_to_save.user_id == user_id:
        try:
            save_to_notion(response_to_save.response_text, user_id)
            print("Did it!")
            return jsonify({"message": "Saved successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify(message='No response to save or unauthorized access'), 400
