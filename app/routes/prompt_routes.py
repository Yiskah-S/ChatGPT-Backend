from flask import Blueprint, jsonify, request
from app.models.prompt import Prompt, db

prompt_bp = Blueprint('prompt', __name__)

@prompt_bp.route('/prompts', methods=['POST'])
def create_prompt():
    data = request.get_json()
    prompt = Prompt.from_dict(data)
    db.session.add(prompt)
    db.session.commit()
    return jsonify(prompt.to_dict()), 201
