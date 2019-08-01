from blueprints import db
from flask_restful import fields

class Rents(db.Model):
    __tablename__ = "rent"
    rent_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), unique = True, nullable = False)
    books_id = db.Column(db.Integer, db.ForeignKey('books.books_id'), unique = True, nullable = False)
    
    def __init__(self, user_id, books_id):
        self.user_id = user_id
        self.books_id = books_id

    response_fields = {
            'user_id' : fields.Integer,
            'books_id' : fields.Integer,
        }

    def __repr__(self):
        return self.rent_id