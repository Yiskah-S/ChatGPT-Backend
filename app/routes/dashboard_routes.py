# dashboard_routes.py 

from flask import send_file
from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models.response import Response
from app.models.prompt import Prompt
from app.notion import save_response_to_notion
from app.crawler import extract_content
from app.chatgpt import generate_response
from flask import make_response
from app import db


dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard/<int:user_id>/')

# Run the web crawler and generate a response
@login_required
@dashboard_bp.route('/', methods=['POST'])
def run_crawler(user_id):
	data = request.get_json()
	prompt_id = data.get('prompt_id')
	target_website = data.get('targetWebsite')

	prompt_obj = Prompt.query.filter_by(user_id=user_id, id=prompt_id).first()
	if prompt_obj:
		prompt_text = prompt_obj.prompt

	content = extract_content(target_website)
	response_text = generate_response(user_id, prompt_text, content)
	response_obj = Response(target_website=target_website, prompt_id=prompt_id, prompt_text=prompt_text, response_text=response_text, user_id=user_id)
	db.session.add(response_obj)
	db.session.commit()
	response_id = response_obj.id

	return jsonify(message='Success', response_id=response_id, response_text=response_text), 200

# Save the response to Notion
@login_required
@dashboard_bp.route('/save_notion/', methods=['POST'])
def save_to_notion(user_id):
	response_id = request.json.get('response_id')
	save_response_to_notion(response_id, user_id)
	return jsonify({"message": "Saved successfully"}), 200

# Save the response to a text file
@login_required
@dashboard_bp.route('/save_txt/', methods=['POST'])
def save_results_txt(user_id):
	response_id = request.json.get('response_id')
	response_to_save = Response.query.get(response_id)
	
	if response_to_save and response_to_save.user_id == user_id:
		response = make_response(response_to_save.response_text)
		response.headers['Content-Type'] = 'text/plain'
		response.headers['Content-Disposition'] = 'attachment; filename=response.txt'
		return response
	else:
		return jsonify(message='No response to save or unauthorized access'), 400

# Save the response to a markdown file
@login_required
@dashboard_bp.route('/save_md/', methods=['POST'])
def save_results_md(user_id):
	response_id = request.json.get('response_id')
	response_to_save = Response.query.get(response_id)
	
	if response_to_save and response_to_save.user_id == user_id:
		response = make_response(response_to_save.response_text)
		response.headers['Content-Type'] = 'text/markdown'
		response.headers['Content-Disposition'] = 'attachment; filename=response.md'
		return response
	else:
		return jsonify(message='No response to save or unauthorized access'), 400