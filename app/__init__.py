# __init__.py

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
from flask_login import LoginManager
from werkzeug.exceptions import Unauthorized
from flask_session import Session
import os
from datetime import timedelta

# Initialize Flask extensions
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()

# Load environment variables
load_dotenv()


def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    if not app.config["SQLALCHEMY_DATABASE_URI"]:
        raise RuntimeError("SQLALCHEMY_DATABASE_URI is not set")

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    # Configure Flask extensions
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['CORS_HEADERS'] = 'Content-Type'

    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
    
    # Additional session configuration
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    Session(app) # Initialize Flask-Session with app

    # Get CORS_ORIGIN from the .env file
    cors_origin = os.environ.get("CORS_ORIGIN")
    print("CORS_ORIGIN:", cors_origin)

    # Configure CORS using the loaded value
    CORS(app, resources={r"/*": {"origins": cors_origin}})

    # Import models
    from .models.user import User
    from .models.prompt import Prompt
    from .models.response import Response
    from .models.api_key import APIKey

    # Initialize SQLAlchemy and Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"error": "You must be logged in to access this page"}), 401

    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    # Import routes and register blueprints
    from .routes.user_routes import user_bp
    app.register_blueprint(user_bp)
    from .routes.prompt_routes import prompt_bp
    app.register_blueprint(prompt_bp)
    from .routes.api_key_routes import api_key_bp
    app.register_blueprint(api_key_bp)
    from .routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp)
    from .routes.response_routes import response_bp
    app.register_blueprint(response_bp)

    # Debug statement
    print("Routes registered successfully!")
    print(app.url_map)
    # print("Current user:", User.query.get(1))
    # print("Current user id:", User.query.get(1).get_id())
    # print("Current user is authenticated:", User.query.get(1).is_authenticated)

    return app
