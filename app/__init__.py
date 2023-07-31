from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_security import check_password_hash, generate_password_hash, login_required

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .models.user import User
    from .models.prompt import Prompt



    from .routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    from .routes.prompt_routes import prompt_bp
    app.register_blueprint(prompt_bp)



    login_manager.init_app(app)
    

    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    
    return app
