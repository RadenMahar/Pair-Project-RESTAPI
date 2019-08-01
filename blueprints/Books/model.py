from blueprints import db
from flask_restful import fields

class Books(db.Model):
    __tablename__ = "books"
    books_id = db.Column(db.Integer, primary_key = True, unique = True)
    books_title = db.Column(db.String(30), unique = True, nullable = False)
    books_isbn = db.Column(db.String(30), nullable = False, unique = True)
    writter = db.Column(db.String(30), nullable = False, unique = True,)
    
    response_fields = {
            'books_id' : fields.Integer,
            'books_title' : fields.String,
            'books_isbn' : fields.String,
            'writter' : fields.String,
        }
    
    def __init__(self, books_title, books_isbn, writter):
        self.books_title = books_title
        self.books_isbn = books_isbn
        self.writter = writter

    def __repr__(self):
        return '<Books %r>' % self.books_id

