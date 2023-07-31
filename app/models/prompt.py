from app import db
from flask_security import UserMixin, RoleMixin, login_required, current_user
from flask_security import check_password_hash, generate_password_hash, login_required

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    responses = db.relationship('Response', backref='prompt', lazy=True)

    def to_dict(self):
        prompt_dict = {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "user_id": self.user_id,
        }
        return prompt_dict

    @classmethod
    def from_dict(cls, request_body):
        return cls(
            title=request_body["title"],
            category=request_body["category"],
            user_id=request_body["user_id"],
        )
    
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)

        db.session.commit()

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500), nullable=False)
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'), nullable=False)


    def to_dict(self):
        response_dict = {
            "id": self.id,
            "body": self.body,
            "prompt_id": self.prompt_id,

        }
        return response_dict

    @classmethod
    def from_dict(cls, request_body):
        return cls(
            body=request_body["body"],
            prompt_id=request_body["prompt_id"],
            
        )
    
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()


