import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs, fields
from sqlalchemy import desc
from .model import Rents
from ..Books.model import Books
from ..User.model import Users
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from . import *
import random
from blueprints import db, app

bp_rent = Blueprint('rent', __name__)

api = Api(bp_rent)

class RentResource(Resource):

    def __init__(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', location='json', required=True, type = int)
        parser.add_argument('books_id', location='json', required=True, type = int)
        args = parser.parse_args()
        
        Bookqry = Books.query.get(args['books_id'])
        Userqry = Users.query.get(args['user_id'])

        bookdict = marshal(Bookqry, Books.response_fields)
        userdict = marshal(Userqry, Users.response_fields)
        
        dict_post = {
            "user_id": args['user_id'],
            "books_id": args['books_id'],
            "user": userdict,
            "books":bookdict,
        }
        rent = Rents(args['user_id'], args['books_id'])


        db.session.add(rent)
        db.session.commit()
        

        app.logger.debug('DEBUG : %s', dict_post)

        return dict_post, 200, {'Content-Type': 'application/json'}

    def get(self, rent_id=None):
        rent = Rents.query.get(rent_id)

        rentdict = marshal(rent, Rents.response_fields)

        Bookqry = Books.query.get(rentdict['books_id'])
        Userqry = Users.query.get(rentdict['user_id'])

        clientjwt = get_jwt_claims()

        bookdict = marshal(Bookqry, Books.response_fields)
        userdict = marshal(Userqry, Users.response_fields)

        if userdict['client_id'] == clientjwt[client_id]:
            dict_get = {
                "user_id" : rentdict['user_id'],
                "books_id": rentdict['books_id'],
                "user": userdict,
                "books":bookdict,
            }
            return dict_get, 200

        else:
            return "Forbidden Status", 200

class Rentlist(Resource):
    def __init__(self):
        pass
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)
        parser.add_argument('user_id', location = 'args', help='invalid status', type = inputs.boolean, choices = (True, False))
        parser.add_argument('books_id', location = 'args', help='invalid status', choices = ('client_id', 'client_secret'))
        args = parser.parse_args()

        offset = args['p']*args['rp'] - args['rp']

        rent = Rents.query
        clientjwt = get_jwt_claims()

        if args['user_id'] is not None:
            rent = rent.filter_by(status=args['user_id'])
        
        if args['books_id'] is not None:
            rent = rent.filter_by(status=args['books_id'])
        
        rent = rent.limit(args['rp']).offset(offset).all()
        list_temp = []

        for row in rent:
            rentdict = marshal(row, Rents.response_fields)
            Bookqry = Books.query.get(rentdict['books_id'])
            Userqry = Users.query.get(rentdict['user_id'])

            bookdict = marshal(Bookqry, Books.response_fields)
            userdict = marshal(Userqry, Users.response_fields)

            if clientjwt['client_id'] == userdict['client_id']:
                dict_get = {
                    "user_id" : rentdict['user_id'],
                    "books_id": rentdict['books_id'],
                    "user": userdict,
                    "books":bookdict,
                }
                list_temp.append(dict_get)
        
        return list_temp, 200 


api.add_resource(RentResource, '', '/<rent_id>')
api.add_resource(Rentlist, '', '/list')