from flask import Blueprint, jsonify, request
from app.models.prompt import Prompt, db
from flask_login import current_user
from flask_login import login_required, current_user, login_user, logout_user
from flask_security import generate_password_hash
from app.models.user import User, db

prompt_bp = Blueprint('prompt', __name__)

@prompt_bp.route('/prompts', methods=['POST'])
@login_required
def create_prompt():
    data = request.get_json()
    data['user_id'] = current_user.get_id()  # Set user_id to the id of the currently logged-in user
    prompt = Prompt.from_dict(data)
    db.session.add(prompt)
    db.session.commit()
    return jsonify(prompt.to_dict()), 201

@prompt_bp.route('/prompts/<prompt_id>', methods=['GET'])
@login_required
def get_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(prompt.to_dict()), 200

@prompt_bp.route('/prompts/<prompt_id>', methods=['PATCH'])
@login_required
def update_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json()
    prompt.title = data['title']
    db.session.commit()
    return jsonify(prompt.to_dict()), 200

@prompt_bp.route('/prompts/<prompt_id>', methods=['DELETE'])
@login_required
def delete_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(prompt)
    db.session.commit()
    return jsonify({"message": "Prompt deleted"}), 200

@prompt_bp.route('/prompts', methods=['GET'])
@login_required
def get_prompts():
    prompts = Prompt.query.all()
    prompts_data = [prompt.to_dict() for prompt in prompts]
    return jsonify(prompts_data), 200

@prompt_bp.route('/prompts/<prompt_id>/responses', methods=['GET'])
@login_required
def get_prompt_responses(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    responses = prompt.responses
    responses_data = [response.to_dict() for response in responses]
    return jsonify(responses_data), 200

@prompt_bp.route('/prompts/<prompt_id>/responses', methods=['POST'])
@login_required
def create_prompt_response(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json()
    data['prompt_id'] = prompt_id
    response = Response.from_dict(data)
    db.session.add(response)
    db.session.commit()
    return jsonify(response.to_dict()), 201

@prompt_bp.route('/prompts/<prompt_id>/responses/<response_id>', methods=['GET'])
@login_required
def get_prompt_response(prompt_id, response_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    response = Response.query.get_or_404(response_id)
    return jsonify(response.to_dict()), 200

@prompt_bp.route('/prompts/<prompt_id>/responses/<response_id>', methods=['PATCH'])
@login_required
def update_prompt_response(prompt_id, response_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    response = Response.query.get_or_404(response_id)
    data = request.get_json()
    response.body = data['body']
    db.session.commit()
    return jsonify(response.to_dict()), 200

@prompt_bp.route('/prompts/<prompt_id>/responses/<response_id>', methods=['DELETE'])
@login_required
def delete_prompt_response(prompt_id, response_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    response = Response.query.get_or_404(response_id)
    db.session.delete(response)
    db.session.commit()
    return jsonify({"message": "Response deleted"}), 200

@prompt_bp.route('/prompts/<prompt_id>/responses/<response_id>/comments', methods=['GET'])
@login_required
def get_prompt_response_comments(prompt_id, response_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    response = Response.query.get_or_404(response_id)
    comments = response.comments
    comments_data = [comment.to_dict() for comment in comments]
    return jsonify(comments_data), 200

@prompt_bp.route('/prompts/<prompt_id>/responses/<response_id>/comments', methods=['POST'])
@login_required
def create_prompt_response_comment(prompt_id, response_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    response = Response.query.get_or_404(response_id)
    data = request.get_json()
    data['response_id'] = response_id
    comment = Comment.from_dict(data)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

@prompt_bp.route('/prompts/<prompt_id>/responses/<response_id>/comments/<comment_id>', methods=['GET'])
@login_required
def get_prompt_response_comment(prompt_id, response_id, comment_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    response = Response.query.get_or_404(response_id)
    comment = Comment.query.get_or_404(comment_id)
    return jsonify(comment.to_dict()), 200

