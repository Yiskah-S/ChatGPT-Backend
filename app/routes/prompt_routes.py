from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.prompt import Prompt
from app.models.response import Response
from app import db

prompt_bp = Blueprint('prompt', __name__)

@login_required
@prompt_bp.route('/prompts', methods=['POST'])
def create_prompt():
    if not current_user.is_authenticated:
        return jsonify({"error": "You must be logged in to access this page"}), 401

    data = request.get_json()

    if "title" in data and not data["title"].strip():
        return jsonify({"error": "Title cannot be left blank"}), 400

    if "category" in data and not data["category"].strip():
        return jsonify({"error": "Category cannot be left blank"}), 400

    data['user_id'] = current_user.get_id()
    prompt = Prompt.from_dict(data)
    db.session.add(prompt)
    db.session.commit()
    return jsonify(prompt.to_dict()), 201

@login_required
@prompt_bp.route('/prompts', methods=['GET'])
def get_prompts():
    if not current_user.is_authenticated:
        return jsonify({"error": "You must be logged in to access this page"}), 401
    
    prompts = Prompt.query.filter_by(user_id=current_user.get_id()).all()
    prompts_data = [prompt.to_dict() for prompt in prompts]
    return jsonify(prompts_data), 200

@login_required
@prompt_bp.route('/prompts/<prompt_id>', methods=['GET'])
def get_prompt(prompt_id):
    if not current_user.is_authenticated:
        return jsonify({"error": "You must be logged in to access this page"}), 401
    
    prompt = Prompt.query.filter_by(id=prompt_id, user_id=current_user.get_id()).first()
    
    if not prompt:
        return jsonify({"error": "Prompt not found"}), 404

    return jsonify(prompt.to_dict()), 200


@login_required
@prompt_bp.route('/prompts/<prompt_id>', methods=['PATCH'])
def update_prompt(prompt_id):
    if not current_user.is_authenticated:
        return jsonify({"error": "You must be logged in to access this page"}), 401
    
    prompt = Prompt.query.filter_by(id=prompt_id, user_id=current_user.get_id()).first()
    
    if not prompt:
        return jsonify({"error": "Prompt not found"}), 404

    data = request.get_json()

    # Check if 'title' and 'category' are provided and not blank
    if "title" in data and not data["title"].strip():
        return jsonify({"error": "Title cannot be left blank"}), 400

    if "category" in data and not data["category"].strip():
        return jsonify({"error": "Category cannot be left blank"}), 400

    prompt.update(data)
    db.session.commit()
    return jsonify(prompt.to_dict()), 200

@login_required
@prompt_bp.route('/prompts/<prompt_id>', methods=['DELETE'])
def delete_prompt(prompt_id):
    if not current_user.is_authenticated:
        return jsonify({"error": "You must be logged in to access this page"}), 401
    
    prompt = Prompt.query.filter_by(id=prompt_id, user_id=current_user.get_id()).first()
    
    if not prompt:
        return jsonify({"error": "Prompt not found"}), 404
    
    db.session.delete(prompt)
    db.session.commit()
    return jsonify({"message": "Prompt deleted"}), 200