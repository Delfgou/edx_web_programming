import os
from flask import Flask, render_template, request
from models import *
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vhltvfuekxyisp:4e8e3284506f4903c26843cbeca2e8bc2ed4693c95ddd2dd8f104550c5700e27@ec2-79-125-6-250.eu-west-1.compute.amazonaws.com:5432/d4j9oravts15j7"
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("postgres://vhltvfuekxyisp:4e8e3284506f4903c26843cbeca2e8bc2ed4693c95ddd2dd8f104550c5700e27@ec2-79-125-6-250.eu-west-1.compute.amazonaws.com:5432/d4j9oravts15j7")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)    


def main():
    db.create_all()


if __name__ == "__main__":
    with app.app_context():
        main()  
        
import csv
engine = create_engine(("postgres://vhltvfuekxyisp:4e8e3284506f4903c26843cbeca2e8bc2ed4693c95ddd2dd8f104550c5700e27@ec2-79-125-6-250.eu-west-1.compute.amazonaws.com:5432/d4j9oravts15j7")) # database engine object from SQLAlchemy that manages connections to the database" # DATABASE_URL is an environment variable that indicates where the database lives
db = scoped_session(sessionmaker(bind=engine))        
b = open("books.csv")
reader = csv.reader(b)
for isbn, title, author, year in reader: # loop gives each column a name
    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",{"isbn": isbn, "title": title, "author": author, "year": year}) # substitute values from CSV line into SQL command, as per this dict
db.commit() # transactions are assumed, so close the transaction finished