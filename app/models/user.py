from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        user_dict = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
        return user_dict

    @classmethod
    def from_dict(cls, request_body):
        return cls(
            username=request_body["username"],
            email=request_body["email"],
            password=request_body["password"],
        )
