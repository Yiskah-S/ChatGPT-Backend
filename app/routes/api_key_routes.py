# api_ey_routes.py 

from flask_login import current_user, login_required
from flask import Blueprint, jsonify, request
from app import db
from app.models.api_key import APIKey
from app.models.user import User

api_key_bp = Blueprint('api_key', __name__, url_prefix='/api-keys')

# @login_required
# def load_user_from_request(request):
#     token = request.headers.get("Authorization")
#     if token:
#         try:
#             user = User.query.get(int(user_id))
#             return user
#         except Exception as e:
#             print("Error loading user from request:", str(e))
#     return None

@login_required
@api_key_bp.route('/api-keys/<int:user_id>', methods=['POST'])
def create_api_key(user_id):
    data = request.get_json()
    print("Received data:", data)
    print(f"Current user id: {current_user.get_id()}")

    api_keys = data.get('apiKeys')  # Assuming the front end sends 'apiKeys' as the key

    if not api_keys:
        return jsonify({"error": "No API keys provided."}), 400

    # Assuming each item in the 'api_keys' list has 'api_type' and 'api_key' keys
    for api_key in api_keys:
        api_type = api_key.get('api_type')
        api_key_value = api_key.get('api_key')

        if not api_type or not api_key_value:
            return jsonify({"error": "Incomplete API key data."}), 400

        data['user_id'] = user_id
        new_api_key = APIKey(api_type=api_type, api_key=api_key_value, user_id=user_id)
        db.session.add(new_api_key)

    db.session.commit()

    return jsonify({"message": "API keys added successfully."}), 201

# Route to get all API keys for the current user
@login_required
@api_key_bp.route('/api-keys/<int:user_id>/keys', methods=['GET'])
def get_api_keys(user_id):
    # data = request.get_json()
    # print("Received data:", data)
    # print(f"Current user id: {current_user.get_id()}")

    api_keys = APIKey.query.filter_by(user_id=user_id).all()
    api_keys_data = [api_key.to_dict() for api_key in api_keys]
    return jsonify(api_keys_data), 200

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


