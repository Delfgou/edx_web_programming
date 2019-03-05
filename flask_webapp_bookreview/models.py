from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model): #or db.database_name ?
    __tablename__="users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    salt = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    
class Book(db.Model):
    __tablename__="books"
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String)
    title = db.Column(db.String)
    author = db.Column(db.String)
    year = db.Column(db.String)
    average_rating = db.Column(db.Integer)
    number_of_ratings = db.Column(db.Integer)

class Review(db.Model):
    __tablename__="reviews"
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)
    username = db.Column(db.String)