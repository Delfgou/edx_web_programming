import os
from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vhltvfuekxyisp:4e8e3284506f4903c26843cbeca2e8bc2ed4693c95ddd2dd8f104550c5700e27@ec2-79-125-6-250.eu-west-1.compute.amazonaws.com:5432/d4j9oravts15j7"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    #user.register(username,email,password)
    user = User(username = username, email = email, password = password)
    db.session.add(user)
    db.session.commit()
    return render_template('success.html')
    
       




if __name__ == "__main__":
    with app.app_context():
        main()     
