# prompt_routes.py

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user, login_user, logout_user
from app import db
from app.models.prompt import Prompt

prompt_bp = Blueprint('prompt', __name__, url_prefix='/prompts')

@login_required
@prompt_bp.route('/prompts', methods=['POST'])
def create_prompt():
	data = request.get_json()
	print("Received data:", data)
	print(f"Current user id: {current_user.get_id()}")

	# checking if required fields are present
	required_fields = ["title", "category", "prompt"]
	for field in required_fields:
		if field not in data or not data[field].strip():
			return jsonify({ "error": f"{field.capitalize()} cannot be left blank"}), 400

	# data['user_id'] = current_user.get_id()
	prompt = Prompt.from_dict(data)
	db.session.add(prompt)
	db.session.commit()
	return jsonify(prompt.to_dict()), 201

@login_required
@prompt_bp.route('/prompts', methods=['GET'])
def get_prompts():
	prompts = Prompt.query.filter_by(user_id=current_user.get_id()).all()
	prompts_data = [prompt.to_dict() for prompt in prompts]
	return jsonify(prompts_data), 200

@login_required
@prompt_bp.route('/prompts/<prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
	prompt = Prompt.query.filter_by(id=prompt_id, user_id=current_user.get_id()).first()

	if not prompt:
		return jsonify({"error": "Prompt not found"}), 404

	return jsonify(prompt.to_dict()), 200

@login_required
@prompt_bp.route('/prompts/<prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
	prompt = Prompt.query.filter_by(id=prompt_id, user_id=current_user.get_id()).first()

	if not prompt:
		return jsonify({"error": "Prompt not found"}), 404

	db.session.delete(prompt)
	db.session.commit()
	return jsonify({"message": "Prompt deleted"}), 200

@login_required
@prompt_bp.route('/<prompt_id>', methods=['PATCH'])
def update_prompt(prompt_id):
	prompt = Prompt.query.filter_by(id=prompt_id, user_id=current_user.get_id()).first()

	if not prompt:
		return jsonify({"error": "Prompt not found"}), 404

	data = request.get_json()

	# checking if required fields are provided and not blank
	required_fields = ["title", "category", "prompt"]
	for field in required_fields:
		if field in data and not data[field].strip():
			return jsonify({ "error": f"{field.capitalize()} cannot be left blank"}), 400

	prompt.update(data)
	db.session.commit()
	return jsonify(prompt.to_dict()), 200