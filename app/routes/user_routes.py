from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app.models.user import User, db
from app.models.prompt import Prompt

user_bp = Blueprint('user', __name__)

# Create a new user
@user_bp.route('/users', methods=['POST'])
def create_user():
	data = request.json
	username = data.get('username')
	email = data.get('email')
	password = data.get('password')
	
	if not username or not email or not password:
		return jsonify({"error": "Incomplete user data."}), 400
	
	user_with_email = User.query.filter_by(email=email).first()
	if user_with_email:
		return jsonify({"error": "User with this email already exists."}), 409
	
	user_with_username = User.query.filter_by(username=username).first()
	if user_with_username:
		return jsonify({"error": "User with this username already exists."}), 409
	
	password_hash = generate_password_hash(password)
	new_user = User(username=username, email=email, password=password_hash)
	db.session.add(new_user)
	db.session.commit()
	return jsonify(new_user.to_dict()), 201


# Get all users
@user_bp.route('/users', methods=['GET'])
def get_users():
	users = User.query.all()
	users_data = [user.to_dict() for user in users]
	return jsonify(users_data), 200

# User login
@user_bp.route('/users/login', methods=['POST'])
def login():
	data = request.get_json()
	email = data.get('email')
	password = data.get('password')
	user = User.query.filter_by(email=email).first()
	
	if user and user.verify_password(password):
		login_user(user)
		return jsonify(user.to_dict()), 200
	else:
		return jsonify({"error": "Invalid username/password"}), 401

# User logout
@user_bp.route('/users/logout', methods=['POST'])
def logout():
	logout_user()
	return jsonify({"message": "Logged out"}), 200

# Get the current logged in user
@user_bp.route('/users/me', methods=['GET'])
@login_required
def get_user():
    return jsonify(current_user.to_dict()), 200

# Update the current logged in user
@user_bp.route('/users/me', methods=['PATCH'])
@login_required
def update_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    
    if username:
        current_user.username = username
    if email:
        current_user.email = email
        
    db.session.commit()
    return jsonify(current_user.to_dict()), 200

# Delete the current logged in user
@user_bp.route('/users/me', methods=['DELETE'])
@login_required
def delete_user():
    db.session.delete(current_user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

