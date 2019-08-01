from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from ..Client.model import Clients

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResource(Resource):
    def __init__(self):
        pass

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='args', required=True)
        parser.add_argument('client_secret', location='args', required=True)
        args = parser.parse_args()

        clientQry = Clients.query.filter_by(client_key=args['client_key']).filter_by(client_secret=args['client_secret']).first()
        client = marshal(clientQry, Clients.jwt_response_field)

        if clientQry is not None:
            token = create_access_token(identity=client)
        else:
            return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401

        return {'token': token,"client":client}, 200
    
    
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        return claims, 200
        

class RefreshTokenResource(Resource):

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity = current_user)
        return {'token': token}, 200


api.add_resource(CreateTokenResource, '')
api.add_resource(RefreshTokenResource, '/refresh')
