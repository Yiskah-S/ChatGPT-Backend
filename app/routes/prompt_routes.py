import logging
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user, login_user, logout_user
from app import db
from app.models.prompt import Prompt

logging.basicConfig(level=logging.DEBUG)

prompt_bp = Blueprint('prompt', __name__, url_prefix='/prompts/<int:user_id>/')

@login_required
@prompt_bp.route('/', methods=['POST'])
def create_prompt(user_id):
    logging.debug(f"Current user id: {current_user.get_id()}")
    logging.debug(f"User id from URL: {user_id}")
    logging.debug(f"Request body: {request.get_json()}")
    # print(f"Current user id: {current_user.get_id()}")
    # print(f"User id from URL: {user_id}")
    # print(f"Request body: {request.get_json()}")

    data = request.get_json()
    new_prompt = Prompt.from_dict(data, user_id=user_id)
    db.session.add(new_prompt)
    db.session.commit()
    return jsonify(new_prompt.to_dict()), 201

@login_required
@prompt_bp.route('/', methods=['GET'])
def get_prompts(user_id):
    prompts = Prompt.query.filter_by(user_id=user_id).all()

    if not prompts:
        return jsonify({"error": "No prompts found for this user."}), 404

    prompts_data = [prompt.to_dict() for prompt in prompts]
    return jsonify(prompts_data), 200

@login_required
@prompt_bp.route('/<int:prompt_id>', methods=['PUT'])
def update_prompt(user_id, prompt_id):
    data = request.get_json()
    logging.debug("Received data: " + str(data))
    # print("Received data:", data)
    prompt = Prompt.query.filter_by(user_id=user_id, id=prompt_id).first()

    if not prompt:
        return jsonify({"error": "Prompt not found."}), 404

    prompt.update_from_dict(data)
    db.session.commit()

    return jsonify(prompt.to_dict()), 200

@login_required
@prompt_bp.route('/<int:prompt_id>', methods=['DELETE'])
def delete_prompt(user_id, prompt_id):
    prompt = Prompt.query.get(prompt_id)
    if not prompt:
        return jsonify({"error": "Prompt not found."}), 404
    db.session.delete(prompt)
    db.session.commit()
    return jsonify({"message": "Prompt successfully deleted."}), 200
