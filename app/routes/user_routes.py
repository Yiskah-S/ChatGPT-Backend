from flask import Blueprint, jsonify, request
from app.models.user import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User.from_dict(data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
