import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Clients
from flask_jwt_extended import jwt_required

from . import *
from blueprints import db, app, internal_required

bp_client = Blueprint('client', __name__)

api = Api(bp_client)

class ClientResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    @internal_required
    def get(self, client_id=None):
        qry = Clients.query.get(client_id)
        if qry is not None:
            return marshal(qry, Clients.response_fields), 200, {'Content-Type':'application/json'}
        return {'status' : 'NOT_FOUND'}, 404

    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', location='json', required=True, type = inputs.boolean)
        args = parser.parse_args()
        
        client = Clients(args['client_key'], args['client_secret'], args['status'])
        db.session.add(client)
        db.session.commit()

        app.logger.debug('DEBUG : %s', client)

        return marshal(client, Clients.response_fields), 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    @internal_required
    def put(self, client_id):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        parser.add_argument('status', location='json', required=True, type = inputs.boolean)
        args = parser.parse_args()
        
        qry = Clients.query.get(client_id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        qry.client_key = args['client_key']
        qry.client_secret = args['client_secret']
        qry.status = args['status']
        db.session.commit()

        return marshal(qry, Clients.response_fields), 200

    @jwt_required
    @internal_required
    def delete(self, client_id):
        qry = Clients.query.get(client_id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200
        
    def patch(self):
        return "not yet implemented", 501
    
class Clientlist(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)
        parser.add_argument('status', location = 'args', help='invalid status', type = inputs.boolean, choices = (True, False))
        parser.add_argument('orderby', location = 'args', help='invalid status', choices = ('client_id', 'client_secret'))
        parser.add_argument('sort', location = 'args', help='invalid status', choices = ('desc', 'asc'))
        args = parser.parse_args()

        offset = args['p']*args['rp'] - args['rp']

        qry = Clients.query

        if args['status'] is not None:
            qry = qry.filter_by(status=args['status'])
        
        if args['orderby'] is not None:
            if args['orderby'] == 'client_id':
                if args['sort'] is not None and args['sort'] == 'desc':
                    qry = qry.order_by(desc(Clients.client_id))
                else:
                    qry = qry.order_by(Clients.client_id)

            elif args['orderby'] == 'client_secret':
                if args['sort'] is not None and args['sort'] == 'desc':
                    qry = qry.order_by(desc(Clients.client_secret))
                else:
                    qry = qry.order_by(Clients.client_secret)               

        
        qry = qry.limit(args['rp']).offset(offset).all()
        list_temp = []
        for row in qry:
            list_temp.append(marshal(row, Clients.response_fields))
        
        return list_temp, 200 

api.add_resource(ClientResource, '', '/<client_id>')
api.add_resource(Clientlist, '', '/list')