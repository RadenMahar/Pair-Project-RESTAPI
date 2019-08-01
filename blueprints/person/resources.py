from flask import Blueprint
from flask_restful import Resource, Api, reqparse

from . import *

# 'person' adalah nama blueprint nya
bp_person = Blueprint('person', __name__)
# person didaftarin di Api
api = Api(bp_person)

class PersonResource(Resource):
    person = Person()

    
    def get(self):
        return self.person.__dict__, 200, {'Content-Type': 'application/json'}
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', required=True)
        parser.add_argument('sex', location='json', required=True)
        args = parser.parse_args()

        self.person.name = args['name']
        self.person.age = args['age']
        self.person.sex = args['sex']

        return self.person.__dict__, 200, {'Content-Type': 'application/json'}
    
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('age', location='json', required=True)
        parser.add_argument('sex', location='json', required=True)
        args = parser.parse_args()

        if int(args['age']) >= 40:
            self.person.age = 20
        self.person.sex = args['sex']

        return self.person.__dict__, 200, {'Content-Type': 'application/json'}
        

    def delete(self):
        return "Deleted", 200
    
    def patch(self):
        return "Not yet implement", 501
    
api.add_resource(PersonResource, '')