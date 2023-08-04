# response_routes.py 

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.prompt import Prompt
from app.models.response import Response
from app import db

prompt_bp = Blueprint('prompt', __name__)

@login_required
@prompt_bp.route('/prompts/<prompt_id>/responses', methods=['GET'])
def get_prompt_responses(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    responses = prompt.responses
    responses_data = [response.to_dict() for response in responses]
    return jsonify(responses_data), 200

@login_required
@prompt_bp.route('/prompts/<prompt_id>/responses', methods=['POST'])
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

@login_required
@prompt_bp.route('/prompts/<prompt_id>/responses/<response_id>', methods=['GET'])
def get_prompt_response(prompt_id, response_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    response = Response.query.get_or_404(response_id)
    return jsonify(response.to_dict()), 200

@login_required
@prompt_bp.route('/prompts/<prompt_id>/responses/<response_id>', methods=['PATCH'])
def update_prompt_response(prompt_id, response_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    response = Response.query.get_or_404(response_id)
    data = request.get_json()
    response.update(data)
    return jsonify(response.to_dict()), 200

@login_required
@prompt_bp.route('/prompts/<prompt_id>/responses/<response_id>', methods=['DELETE'])
def delete_prompt_response(prompt_id, response_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    response = Response.query.get_or_404(response_id)
    db.session.delete(response)
    db.session.commit()
    return jsonify({"message": "Response deleted"}), 200

@user_bp.route('/users/me/prompts/<prompt_id>/responses/<response_id>/comments', methods=['GET'])
@login_required
def get_user_prompt_response_comments(prompt_id, response_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    response = Response.query.get_or_404(response_id)
    comments = response.comments
    comments_data = [comment.to_dict() for comment in comments]
    return jsonify(comments_data), 200

# @login_required
# @prompt_bp.route('/prompts/<prompt_id>/responses/<response_id>/comments', methods=['GET'])
# def get_prompt_response_comments(prompt_id, response_id):
#     prompt = Prompt.query.get_or_404(prompt_id)
#     if prompt.user_id != current_user.get_id():
#         return jsonify({"error": "Unauthorized"}), 403
#     response = Response.query.get_or_404(response_id)
#     comments = response.comments
#     comments_data = [comment.to_dict() for comment in comments]
#     return jsonify(comments_data), 200

# @login_required
# @prompt_bp.route('/prompts/<prompt_id>/responses/<response_id>/comments', methods=['POST'])
# def create_prompt_response_comment(prompt_id, response_id):
#     prompt = Prompt.query.get_or_404(prompt_id)
#     if prompt.user_id != current_user.get_id():
#         return jsonify({"error": "Unauthorized"}), 403
#     response = Response.query.get_or_404(response_id)
#     data = request.get_json()
#     data['response_id'] = response_id
#     comment = Comment.from_dict(data)
#     db.session.add(comment)
#     db.session.commit()
#     return jsonify(comment.to_dict()), 201

# @login_required
# @prompt_bp.route('/prompts/<prompt_id>/responses/<response_id>/comments/<comment_id>', methods=['GET'])
# def get_prompt_response_comment(prompt_id, response_id, comment_id):
#     prompt = Prompt.query.get_or_404(prompt_id)
#     if prompt.user_id != current_user.get_id():
#         return jsonify({"error": "Unauthorized"}), 403
#     response = Response.query.get_or_404(response_id)
#     comment = Comment.query.get_or_404(comment_id)
#     return jsonify(comment.to_dict()), 200
