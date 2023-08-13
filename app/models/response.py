# response.py 

from app import db

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_website = db.Column(db.String(1000), nullable=False) # URL of the target website
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'), nullable=False)          # The generated response text
    prompt_text = db.Column(db.String(5000), nullable=False)    # The prompt text used for generating the response
    response_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Foreign key to the User

    def to_dict(self):
        response_dict = {
            "id": self.id,
            "target_website": self.target_website,
            "prompt_id": self.prompt_id,
            "prompt_text": self.prompt_text,
            "response_text": self.response_text,
            "user_id": self.user_id,
        }
        return response_dict

    @classmethod
    def from_dict(cls, request_body, user_id):
        return cls(
            target_website=request_body["target_website"],
            prompt_id=request_body["prompt_id"],
            prompt_text=request_body["prompt_text"],
            response_text=request_body["response_text"],
            user_id=user_id,
        )
