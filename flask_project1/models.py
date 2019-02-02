from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model): #or db.database_name ?
    __tablename__="users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    
class Book(db.Model):
    __tablename__="books"
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String)
    title = db.Column(db.String)
    author = db.Column(db.String)
    year = db.Column(db.String)

class Review(db.Model):
    __tablename__="reviews"
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)