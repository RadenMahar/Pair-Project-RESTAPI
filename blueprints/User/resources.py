import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Users
from flask_jwt_extended import jwt_required

from . import *
import random
from blueprints import db, app, internal_required

bp_user = Blueprint('user', __name__)

api = Api(bp_user)

class UserResource(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    @internal_required
    def get(self, user_id=None):
        qry = Users.query.get(user_id)
        if qry is not None:
            return marshal(qry, Users.response_fields), 200, {'Content-Type':'application/json'}
        return {'status' : 'NOT_FOUND'}, 404

    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', location='json', required=True)
        parser.add_argument('user_age', location='json', required=True, type = int)
        parser.add_argument('user_sex', location='json', required=True)
        parser.add_argument('client_id', location='json', required=True, type = int)
        args = parser.parse_args()
        
        user = Users(args['user_name'], args['user_age'], args['user_sex'], args['client_id'])
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    @internal_required
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('user_name', location='json', required=True)
        parser.add_argument('user_age', location='json', required=True, type = int)
        parser.add_argument('user_sex', location='json', required=True)
        parser.add_argument('client_id', location='json', required=True, type = int)
        args = parser.parse_args()
        
        qry = Users.query.get(user_id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        qry.user_name = args['user_name']
        qry.user_age = args['user_age']
        qry.user_sex = args['user_sex']
        qry.client_id = args['client_id']
        db.session.commit()

        return marshal(qry, Users.response_fields), 200

    @jwt_required
    @internal_required
    def delete(self, user_id):
        qry = Users.query.get(user_id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200
        
    def patch(self):
        return "not yet implemented", 501
    
class Userlist(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)
        parser.add_argument('title', location = 'args', help='invalid status')
        parser.add_argument('isbn', location = 'args', help='invalid status')
        args = parser.parse_args()

        offset = args['p']*args['rp'] - args['rp']

        qry = Users.query

        list_temp = []
        for row in qry:
            list_temp.append(marshal(row, Users.response_fields))
        
        return list_temp, 200 

api.add_resource(UserResource, '', '/<user_id>')
api.add_resource(Userlist, '', '/list')