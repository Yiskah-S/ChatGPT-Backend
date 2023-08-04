# api_key.py

from app import db

class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_type = db.Column(db.String(120), nullable=False)
    api_key = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        api_key_dict = {
            "id": self.id,
            "api_type": self.api_type,
            "api_key": self.api_key,
            "user_id": self.user_id,
        }
        return api_key_dict

