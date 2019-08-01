from blueprints import db
from flask_restful import fields

class Users(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(30), unique = True, nullable = False)
    user_age = db.Column(db.Integer, nullable = False, default = 20)
    user_sex = db.Column(db.String(30), nullable = False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable = False)

    response_fields = {
            'user_id' : fields.Integer,
            'user_name' : fields.String,
            'user_age' : fields.Integer,
            'user_sex' : fields.String,
            'client_id' : fields.Integer,
        }
    
    def __init__(self, user_name, user_age, user_sex, client_id):
        self.user_name = user_name
        self.user_age = user_age
        self.user_sex = user_sex
        self.client_id = client_id

    def __repr__(self):
        return '<User %r>' % self.user_id