from blueprints import db
from flask_restful import fields

class Locations(db.Model):
    __tablename__ = "location"
    Location_id = db.Column(db.Integer, primary_key = True)
    Location_ip = db.Column(db.String(30), nullable = False)
    Location_name = db.Column(db.String(30), nullable = False)
    Location_latitude = db.Column(db.String(30), nullable = True, default=20)
    Location_longitude = db.Column(db.String(30), nullable = True, default=20)
    
    response_fields = {
            'Location_id' : fields.Integer,
            'Location_ip' : fields.String,
            'Location_name' : fields.String,
            'Location_latitude' : fields.String,
            'Location_longitude' : fields.String,
        }

    jwt_response_field = {
        'client_id' : fields.Integer,
        'client_key' : fields.String,
        'status' : fields.Boolean,
    }
    
    def __init__(self, Location_ip, Location_name, Location_latitude, Location_longitude):
        self.Location_ip = Location_ip
        self.Location_name = Location_name
        self.Location_latitude = Location_latitude
        self.Location_longitude = Location_longitude

    def __repr__(self):
        return '<Location %r>' % self.Location_id