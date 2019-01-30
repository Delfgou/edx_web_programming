from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model): #or db.database_name ?
    __tablename__="users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)