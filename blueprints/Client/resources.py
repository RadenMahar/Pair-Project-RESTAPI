import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Clients
from flask_jwt_extended import jwt_required

from . import *
from blueprints import db, app

bp_client = Blueprint('client', __name__)

api = Api(bp_client)

class ClientResource(Resource):

    def __init__(self):
        pass

    def get(self, id=None):
        qry = Clients.query.get(id)
        if qry is not None:
            return marshal(qry, Clients.response_fields), 200, {'Content-Type':'application/json'}
        return {'status' : 'NOT_FOUND'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('sex', location='json', required=True)
        parser.add_argument('access_key', location='json', required=True)
        parser.add_argument('access_secret', location='json', required=True)
        parser.add_argument('status_access', location='json', required=False, type = inputs.boolean)
        args = parser.parse_args()
        
        client = Clients(args['name'], args['sex'], args['access_key'], args['access_secret'], args['status_access'])
        db.session.add(client)
        db.session.commit()

        app.logger.debug('DEBUG : %s', client)

        return marshal(client, Clients.response_fields), 200, {'Content-Type': 'application/json'}

    def delete(self, id):
        qry = Clients.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200
    
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('sex', location='json', required=True)
        parser.add_argument('access_key', location='json', required=True)
        parser.add_argument('access_secret', location='json', required=True)
        parser.add_argument('status_access', location='json', required=False, type = inputs.boolean)
        args = parser.parse_args()
        
        qry = Clients.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        qry.name = args['name']
        qry.sex = args['sex']
        qry.access_key = args['access_key']
        qry.access_secret = args['access_secret']
        qry.status_access = args['status_access']
        db.session.commit()

        return marshal(qry, Clients.response_fields), 200
        
    def patch(self):
        return "not yet implemented", 501
    
class Clientlist(Resource):
    def __init__(self):
        pass

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)
        parser.add_argument('status_access', location = 'args', help='invalid status', type = inputs.boolean, choices = (True, False))
        args = parser.parse_args()

        offset = args['p']*args['rp'] - args['rp']

        qry = Clients.query

        if args['status_access'] is not None:
            qry = qry.filter_by(status=args['status_access'])               
        
        qry = qry.limit(args['rp']).offset(offset).all()
        list_temp = []
        for row in qry:
            list_temp.append(marshal(row, Clients.response_fields))
        
        return list_temp, 200 
    
api.add_resource(ClientResource, '', '/<id>')
api.add_resource(Clientlist, '', '/list')