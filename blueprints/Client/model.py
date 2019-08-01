from blueprints import db
from flask_restful import fields

class Clients(db.Model):
    __tablename__ = "client"
    client_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    sex = db.Column(db.String(30), nullable = False)
    access_key = db.Column(db.String(30), nullable = False)
    access_secret = db.Column(db.String(30), nullable = False)
    status_access = db.Column(db.Boolean, nullable = False)

    
    response_fields = {
            'client_id' : fields.Integer,
            'name' : fields.String,
            'sex' : fields.String,
            'access_key' : fields.String,
            'access_secret' : fields.String,
            'status_access' : fields.Boolean,
        }

    jwt_response_field = {
            'client_id' : fields.Integer,
            'name' : fields.String,
            'sex' : fields.String,
            'access_key' : fields.String,
            'status_access' : fields.Boolean,
        }

    def __init__(self, name, sex, access_key, access_secret, status_access):
        self.name = name
        self.sex = sex
        self.access_key = access_key
        self.access_secret = access_secret
        self.status_access = status_access  

    def __repr__(self):
        return '<Client %r>' % self.client_id