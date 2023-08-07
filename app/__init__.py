# __init__.py

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_cors import CORS
from flask_login import LoginManager
from werkzeug.exceptions import Unauthorized
import os

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

    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

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
    app.register_blueprint(prompt_bp, url_prefix='/prompt-library')
    from .routes.api_key_routes import api_key_bp  
    app.register_blueprint(api_key_bp, url_prefix='/api-keys')  # Register the blueprint for API keys

    print("Routes registered successfully!")

    return app
