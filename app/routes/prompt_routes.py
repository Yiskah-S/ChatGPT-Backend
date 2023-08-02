from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.prompt import Prompt
from app.models.response import Response
from app import db

prompt_bp = Blueprint('prompt', __name__)

@login_required
@prompt_bp.route('/prompts', methods=['POST'])
def create_prompt():
    data = request.get_json()
    data['user_id'] = current_user.get_id()
    prompt = Prompt.from_dict(data)
    db.session.add(prompt)
    db.session.commit()
    return jsonify(prompt.to_dict()), 201

@login_required
@prompt_bp.route('/prompts/<prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(prompt.to_dict()), 200

@login_required
@prompt_bp.route('/prompts/<prompt_id>', methods=['PATCH'])
def update_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json()
    prompt.update(data)
    return jsonify(prompt.to_dict()), 200

@login_required
@prompt_bp.route('/prompts/<prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(prompt)
    db.session.commit()
    return jsonify({"message": "Prompt deleted"}), 200

@login_required
@prompt_bp.route('/prompts', methods=['GET'])
def get_prompts():
    prompts = Prompt.query.all()
    prompts_data = [prompt.to_dict() for prompt in prompts]
    return jsonify(prompts_data), 200

