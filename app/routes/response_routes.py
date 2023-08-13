# response_routes.py 

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.prompt import Prompt
from app.models.response import Response
from app import db

response_bp = Blueprint('response', __name__, url_prefix='/response/<int:user_id>/')

@login_required
@response_bp.route('/', methods=['GET'])
def get_responses(user_id):
    responses = Response.query.filter_by(user_id=user_id).all()
    print("Responses:", responses)
    if not responses:
        return jsonify({"error": "Prompt not found."}), 404
    
    responses_data = [response.to_dict() for response in responses]
    return jsonify(responses_data), 200