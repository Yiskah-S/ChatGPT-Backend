# api_key_routes.py 

from flask_login import current_user, login_required
from flask import Blueprint, jsonify, request
from app import db
from app.models.api_key import APIKey
from app.models.user import User

api_key_bp = Blueprint('api_key', __name__, url_prefix='/api-keys/<int:user_id>')

@login_required
@api_key_bp.route('/', methods=['POST'])
def create_api_key(user_id):
    data = request.get_json()
    print("Received data:", data)
    print(f"Current user id: {current_user.get_id()}")

    if user_id != current_user.id:
        return jsonify({"error": "Unauthorized to post these API keys."}), 403

    api_keys = data.get('apiKeys')  # Assuming the front end sends 'apiKeys' as the key

    if not api_keys:
        return jsonify({"error": "No API keys provided."}), 400

    # Assuming each item in the 'api_keys' list has 'api_type' and 'api_key' keys
    for api_key in api_keys:
        api_type = api_key.get('api_type')
        api_key_value = api_key.get('api_key')
        user_id = current_user.get_id()

        if not api_type or not api_key_value:
            return jsonify({"error": "Incomplete API key data."}), 400

        new_api_key = APIKey(api_type=api_type, api_key=api_key_value, user_id=user_id)
        db.session.add(new_api_key)

    db.session.commit()

    return jsonify({"message": "API keys added successfully."}), 201

@login_required
@api_key_bp.route('/', methods=['GET'])
def get_api_keys(user_id):
	if user_id != current_user.id:
		return jsonify({"error": "Unauthorized to access these API keys."}), 403

	api_keys = APIKey.query.filter_by(user_id=user_id).all()

	if not api_keys:
		return jsonify({"error": "No API keys found for this user."}), 404

	api_keys_data = [api_key.to_dict() for api_key in api_keys]
	return jsonify(api_keys_data), 200


@login_required
@api_key_bp.route('/', methods=['PATCH'])
def update_api_keys(user_id):
    data = request.get_json()
    api_keys_data = data.get('apiKeys')  # Assuming the front end sends 'apiKeys' as the key

    if not api_keys_data:
        return jsonify({"error": "No API keys provided."}), 400

    for api_key_data in api_keys_data:
        api_type = api_key_data.get('api_type')
        api_key_value = api_key_data.get('api_key')

        if not api_type or api_key_value is None:  # allow for empty string as value
            return jsonify({"error": "Incomplete API key data."}), 400

        api_key = APIKey.query.filter_by(user_id=user_id, api_type=api_type).first()
        if not api_key:
            return jsonify({"error": f"API key of type {api_type} not found."}), 404

        if api_key.user_id != current_user.id:
            return jsonify({"error": "Unauthorized to update this API key."}), 403

        api_key.api_key = api_key_value

    db.session.commit()

    return jsonify({"message": "API keys updated successfully."}), 200
