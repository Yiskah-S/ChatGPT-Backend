from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_security import generate_password_hash
from app.models.user import User, db
from app.models.prompt import Prompt

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
	data = request.json
	username = data.get('username')
	email = data.get('email')
	password = data.get('password')

	if not username or not email or not password:
		return jsonify({"error": "Incomplete user data."}), 400

	user = User.query.filter_by(email=email).first()
	if user:
		return jsonify({"error": "User with this email already exists."}), 409

	password_hash = generate_password_hash(password)
	new_user = User(username=username, email=email, password=password_hash)
	db.session.add(new_user)
	db.session.commit()

	return jsonify(new_user.to_dict()), 201

@user_bp.route('/users', methods=['GET'])  # Define a separate GET route for /users
def get_users():
	users = User.query.all()
	users_data = [user.to_dict() for user in users]
	return jsonify(users_data), 200

@user_bp.route('/users/login', methods=['POST'])
def login():
	data = request.get_json()
	user = User.query.filter_by(email=data['email']).first()
	if user and user.verify_password(data['password']):
		login_user(user)
		return jsonify(user.to_dict()), 200
	else:
		return jsonify({"error": "Invalid username/password"}), 401
	
@user_bp.route('/users/logout', methods=['POST'])
def logout():
	logout_user()
	return jsonify({"message": "Logged out"}), 200

@user_bp.route('/users/me', methods=['GET'])
@login_required
def get_user():
    return jsonify(current_user.to_dict()), 200

@user_bp.route('/users/me', methods=['PATCH'])
@login_required
def update_user():
    data = request.get_json()
    current_user.username = data['username']
    current_user.email = data['email']
    db.session.commit()
    return jsonify(current_user.to_dict()), 200

@user_bp.route('/users/me', methods=['DELETE'])
@login_required
def delete_user():
    db.session.delete(current_user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

@user_bp.route('/users/me/prompts', methods=['GET'])
@login_required
def get_user_prompts():
    prompts = current_user.prompts
    prompts_data = [prompt.to_dict() for prompt in prompts]
    return jsonify(prompts_data), 200

@user_bp.route('/users/me/prompts', methods=['POST'])
@login_required
def create_user_prompt():
    data = request.get_json()
    data['user_id'] = current_user.get_id()
    prompt = Prompt.from_dict(data)
    db.session.add(prompt)
    db.session.commit()
    return jsonify(prompt.to_dict()), 201

@user_bp.route('/users/me/prompts/<prompt_id>', methods=['GET'])
@login_required
def get_user_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(prompt.to_dict()), 200

@user_bp.route('/users/me/prompts/<prompt_id>', methods=['PATCH'])
@login_required
def update_user_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json()
    prompt.title = data['title']
    prompt.description = data['description']
    db.session.commit()
    return jsonify(prompt.to_dict()), 200

@user_bp.route('/users/me/prompts/<prompt_id>', methods=['DELETE'])
@login_required
def delete_user_prompt(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    db.session.delete(prompt)
    db.session.commit()
    return jsonify({"message": "Prompt deleted"}), 200

@user_bp.route('/users/me/prompts/<prompt_id>/responses', methods=['GET'])
@login_required
def get_user_prompt_responses(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    responses = prompt.responses
    responses_data = [response.to_dict() for response in responses]
    return jsonify(responses_data), 200

@user_bp.route('/users/me/prompts/<prompt_id>/responses', methods=['POST'])
@login_required
def create_user_prompt_response(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json()
    data['prompt_id'] = prompt_id
    response = Response.from_dict(data)
    db.session.add(response)
    db.session.commit()
    return jsonify(response.to_dict()), 201

@user_bp.route('/users/me/prompts/<prompt_id>/responses/<response_id>', methods=['GET'])    
@login_required
def get_user_prompt_response(prompt_id, response_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    response = Response.query.get_or_404(response_id)
    return jsonify(response.to_dict()), 200

@user_bp.route('/users/me/prompts/<prompt_id>/responses/<response_id>', methods=['PATCH'])  
@login_required
def update_user_prompt_response(prompt_id, response_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.get_id():
        return jsonify({"error": "Unauthorized"}), 403
    response = Response.query.get_or_404(response_id)
    data = request.get_json()
    response.body = data['body']
    db.session.commit()
    return jsonify(response.to_dict()), 200

@user_bp.route('/users/me/prompts/<prompt_id>/responses/<response_id>', methods=['DELETE']) 
@login_required
def delete_user_prompt_response(prompt_id, response_id):
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


