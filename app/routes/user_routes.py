# user_routes.py 

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from app.models.user import User, db

user_bp = Blueprint('user', __name__, url_prefix='/users/')

# Create a new user
@user_bp.route('/', methods=['POST'])
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
@user_bp.route('/', methods=['GET'])
def get_users():
	users = User.query.all()
	users_data = [user.to_dict() for user in users]
	return jsonify(users_data), 200

# User login
@user_bp.route('/login/', methods=['POST'])
def login():
	data = request.get_json()
	email = data.get('email')
	password = data.get('password')
	user = User.query.filter_by(email=email).first()
	
	if user and user.verify_password(password):
		login_user(user)
		return jsonify(user.to_dict()), 200
	else:
		return jsonify({"error": "User not found or password is incorrect"}), 404

# User logout
@login_required
@user_bp.route('/logout/', methods=['POST'])
def logout():
	logout_user()
	return jsonify({"message": "Logged out"}), 200

# Get the current logged in user
@login_required
@user_bp.route('/me/', methods=['GET'])
def get_user():
	return jsonify(current_user.to_dict()), 200

# Update the current logged in user
@login_required
@user_bp.route('/me/', methods=['PATCH'])
def update_user():
	data = request.get_json()
	username = data.get('username')
	email = data.get('email')
	
	if username:
		user_with_username = User.query.filter_by(username=username).first()
		if user_with_username and user_with_username.id != current_user.id:
			return jsonify({"error": "User with this username already exists."}), 409
		current_user.username = username
	
	if email:
		user_with_email = User.query.filter_by(email=email).first()
		if user_with_email and user_with_email.id != current_user.id:
			return jsonify({"error": "User with this email already exists."}), 409
		current_user.email = email
	
	db.session.commit()
	return jsonify(current_user.to_dict()), 200

# Delete the current logged in user
@login_required
@user_bp.route('/me/', methods=['DELETE'])
def delete_user():
	db.session.delete(current_user)
	db.session.commit()
	return jsonify({"message": "User deleted"}), 200

@login_required
@user_bp.route('/protected_resource/')
def protected_resource():
	return jsonify({'message': 'This is a protected resource!', 'current_user_id': current_user.get_id()}), 200
