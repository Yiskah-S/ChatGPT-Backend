#  prompt_routes.py 

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.prompt import Prompt
from app import db

prompt_bp = Blueprint('prompt', __name__, url_prefix='/prompts/<int:user_id>/')

# Create a new prompt
@login_required
@prompt_bp.route('/', methods=['POST'])
def create_prompt(user_id):
	data = request.get_json()
	new_prompt = Prompt.from_dict(data, user_id=user_id)
	db.session.add(new_prompt)
	db.session.commit()
	return jsonify(new_prompt.to_dict()), 201

# Get all prompts for a user
@login_required
@prompt_bp.route('/', methods=['GET'])
def get_prompts(user_id):
    prompts = Prompt.query.filter_by(user_id=user_id).all()

    if not prompts:
        return jsonify({"error": "No prompts found for this user."}), 404

    prompts_data = [prompt.to_dict() for prompt in prompts]
    return jsonify(prompts_data), 200

# Get a single prompt
@login_required
@prompt_bp.route('/<int:prompt_id>/', methods=['GET'])
def get_prompt(user_id, prompt_id):
    prompt = Prompt.query.filter_by(user_id=user_id, id=prompt_id).first()
    if not prompt:
        return jsonify({"error": "Prompt not found."}), 404
    return jsonify(prompt.to_dict()), 200

# Update a single prompt
@login_required
@prompt_bp.route('/<int:prompt_id>/', methods=['PUT'])
def update_prompt(user_id, prompt_id):
    data = request.get_json()
    print("Received data:", data)
    prompt = Prompt.query.filter_by(user_id=user_id, id=prompt_id).first()

    if not prompt:
        return jsonify({"error": "Prompt not found."}), 404

    prompt.update_from_dict(data)
    db.session.commit()

    return jsonify(prompt.to_dict()), 200

# Delete a single prompt
@login_required
@prompt_bp.route('/<int:prompt_id>/', methods=['DELETE'])
def delete_prompt(user_id, prompt_id):
    prompt = Prompt.query.get(prompt_id)
    if not prompt:
        return jsonify({"error": "Prompt not found."}), 404
    db.session.delete(prompt)
    db.session.commit()
    return jsonify({"message": "Prompt successfully deleted."}), 200

# Get all categories for a user
@login_required
@prompt_bp.route('/categories/', methods=['GET'])
def get_prompt_categories(user_id):
    prompts = Prompt.query.filter_by(user_id=user_id).all()
    
    if not prompts:
        return jsonify({"error": "No prompts found for this user."}), 404
    
    categories = {prompt.category for prompt in prompts}
    return jsonify(list(categories)), 200

# Get all prompts for a user by category
@login_required
@prompt_bp.route('/categories/<string:category>/', methods=['GET'])
def get_prompts_by_category(user_id, category):
    prompts = Prompt.query.filter_by(user_id=user_id, category=category).all()
    
    if not prompts:
        return jsonify({"error": "No prompts found for this user."}), 404
    
    prompts_data = [prompt.to_dict() for prompt in prompts]
    return jsonify(prompts_data), 200