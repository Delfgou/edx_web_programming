import os
from flask import Flask, render_template, request
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine
#from sqlalchemy.orm import scoped_session, sessionmaker
from classes import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vhltvfuekxyisp:4e8e3284506f4903c26843cbeca2e8bc2ed4693c95ddd2dd8f104550c5700e27@ec2-79-125-6-250.eu-west-1.compute.amazonaws.com:5432/d4j9oravts15j7"
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("postgres://vhltvfuekxyisp:4e8e3284506f4903c26843cbeca2e8bc2ed4693c95ddd2dd8f104550c5700e27@ec2-79-125-6-250.eu-west-1.compute.amazonaws.com:5432/d4j9oravts15j7")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#db = SQLAlchemy(app)
db.init_app(app)    


def main():
    db.create_all()
    
if __name__ == "__main__":
    with app.app_context():
        main()    
        
        
#class User(db.d4j9oravts15j7):
    #def __init__(self,username,email,password):
        #self.username = username
        #self.email = email
        #self.password = password        
        
#user1 = User("cyrill","c@b.ch","abc123")
#print(user1.username)



#@app.route("/")
#def index():
    #return "Hello, world!"

#print("ran")