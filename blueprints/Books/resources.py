import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from sqlalchemy import desc
from .model import Books
from flask_jwt_extended import jwt_required

from . import *
from blueprints import db, app, internal_required

bp_books = Blueprint('books', __name__)

api = Api(bp_books)

class BookResource(Resource):

    def __init__(self):
        pass
    
    @jwt_required
    @internal_required
    def get(self, books_id=None):
        qry = Books.query.get(books_id)
        if qry is not None:
            return marshal(qry, Books.response_fields), 200, {'Content-Type':'application/json'}
        return {'status' : 'NOT_FOUND'}, 404

    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('books_title', location='json', required=True)
        parser.add_argument('books_isbn', location='json', required=True)
        parser.add_argument('writter', location='json', required=True,)
        args = parser.parse_args()
        
        book = Books(args['books_title'], args['books_isbn'], args['writter'])
        db.session.add(book)
        db.session.commit()

        app.logger.debug('DEBUG : %s', book)

        return marshal(book, Books.response_fields), 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    @internal_required
    def put(self, books_id):
        parser = reqparse.RequestParser()
        parser.add_argument('books_title', location='json', required=True)
        parser.add_argument('books_isbn', location='json', required=True)
        parser.add_argument('writter', location='json', required=True)
        args = parser.parse_args()
        
        qry = Books.query.get(books_id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404
        
        qry.books_title = args['books_title']
        qry.books_isbn = args['books_isbn']
        qry.writter = args['writter']
        db.session.commit()

        return marshal(qry, Books.response_fields), 200

    @jwt_required
    @internal_required
    def delete(self, books_id):
        qry = Books.query.get(books_id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200
        
    def patch(self):
        return "not yet implemented", 501
    
class Bookslist(Resource):
    def __init__(self):
        pass
    
    @jwt_required
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 25)
        parser.add_argument('books_title', location = 'args', help='invalid status')
        parser.add_argument('books_isbn', location = 'args', help='invalid status')
        args = parser.parse_args()

        offset = args['p']*args['rp'] - args['rp']

        qry = Books.query

        if args['books_title'] is not None:
            qry = qry.filter_by(status=args['books_title'])
        if args['books_isbn'] is not None:
            qry = qry.filter_by(status=args['books_isbn'])
            
        qry = qry.limit(args['rp']).offset(offset).all()
        list_temp = []
        for row in qry:
            list_temp.append(marshal(row, Books.response_fields))
        
        return list_temp, 200 

api.add_resource(BookResource, '', '/<books_id>')
api.add_resource(Bookslist, '', '/list')