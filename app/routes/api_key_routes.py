# api_ey_routes.py 

from flask_login import current_user, login_required
from flask import Blueprint, jsonify, request
from app import db
from app.models.api_key import APIKey

api_key_bp = Blueprint('api_key', __name__, url_prefix='/api-keys')

# Route to get all API keys for the current user
@login_required
@api_key_bp.route('/', methods=['GET'])
def get_api_keys():
    api_keys = APIKey.query.filter_by(user_id=current_user.id).all()
    api_keys_data = [api_key.to_dict() for api_key in api_keys]
    return jsonify(api_keys_data), 200

# Route to get an API key by its ID
@login_required
@api_key_bp.route('/<int:api_key_id>', methods=['GET'])
def get_api_key_by_id(api_key_id):
    api_key = APIKey.query.get(api_key_id)
    if not api_key:
        return jsonify({"error": "API key not found."}), 404
    if api_key.user_id != current_user.id:
        return jsonify({"error": "Unauthorized to access this API key."}), 403
    return jsonify(api_key.to_dict()), 200

# Route to update an API key by its ID
@login_required
@api_key_bp.route('/<int:api_key_id>', methods=['PATCH'])
def update_api_key(api_key_id):
    api_key = APIKey.query.get(api_key_id)
    if not api_key:
        return jsonify({"error": "API key not found."}), 404
    if api_key.user_id != current_user.id:
        return jsonify({"error": "Unauthorized to update this API key."}), 403

    data = request.get_json()
    if 'api_type' in data:
        api_key.api_type = data['api_type']
    if 'api_key' in data:
        api_key.api_key = data['api_key']

    db.session.commit()
    return jsonify(api_key.to_dict()), 200

@login_required
@api_key_bp.route('/', methods=['POST'])
def create_api_key():
    data = request.get_json()
    api_type = data.get('api_type')
    api_key = data.get('api_key')

    if not api_type or not api_key:
        return jsonify({"error": "Incomplete API key data."}), 400

    # You can add additional checks to validate the API type and key as needed

    new_api_key = APIKey(api_type=api_type, api_key=api_key, user_id=current_user.id)
    db.session.add(new_api_key)
    db.session.commit()

    return jsonify(new_api_key.to_dict()), 201
