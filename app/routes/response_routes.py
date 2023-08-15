# response_routes.py 

from flask import Blueprint, jsonify
from flask_login import login_required
from app.models.response import Response

response_bp = Blueprint('response', __name__, url_prefix='/response/<int:user_id>/')

# Get all responses for a user
@login_required
@response_bp.route('/', methods=['GET'])
def get_responses(user_id):
	responses = Response.query.filter_by(user_id=user_id).all()
	if not responses:
		return jsonify({"error": "Prompt not found."}), 404

	responses_data = [response.to_dict() for response in responses]
	return jsonify(responses_data), 200
