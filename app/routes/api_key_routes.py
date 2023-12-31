#  api_key_routes.py

from flask_login import login_required
from flask import Blueprint, jsonify
from app.models.api_key import APIKey
from flask import request
from app import db

api_key_bp = Blueprint('api_key', __name__, url_prefix='/api-keys/<int:user_id>/')

# Get all API keys for a user
@login_required
@api_key_bp.route('/', methods=['GET'])
def get_api_keys(user_id):
    api_keys = APIKey.query.filter_by(user_id=user_id).all()
    if not api_keys:
        return jsonify({"error": "No API keys found for this user."}), 404
    api_keys_data = [api_key.to_dict() for api_key in api_keys]
    return jsonify(api_keys_data), 200

# Create a new API key for a user
@login_required
@api_key_bp.route('/', methods=['PUT'])
def update_api_key(user_id):
    data = request.get_json()
    api_keys = data.get('apiKeys')

    if not api_keys:
        return jsonify({"error": "No API keys provided."}), 400

    for key_obj in api_keys:
        key = APIKey.query.filter_by(user_id=user_id, api_type=key_obj['api_type']).first()
        if key:
            key.api_key = key_obj['api_key']
        else:
            new_api_key = APIKey(api_type=key_obj['api_type'], api_key=key_obj['api_key'], user_id=user_id)
            db.session.add(new_api_key)
    db.session.commit()
    return jsonify({"message": "API keys updated successfully."}), 200

# Delete an API key for a user
@login_required
@api_key_bp.route('/', methods=['DELETE'])
def delete_api_key(user_id, api_key_id):
    api_key = APIKey.query.get(api_key_id)
    if not api_key:
        return jsonify({"error": "API key not found."}), 404
    db.session.delete(api_key)
    db.session.commit()
    return jsonify({"message": "API key successfully deleted."}), 200
