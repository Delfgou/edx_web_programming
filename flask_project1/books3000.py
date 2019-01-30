import os
from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/register")
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    #user.register(username,email,password)
    user = User(username = username, email = email, password = password)
    db.session.add(user)
    db.session.commit()
    return render_template('success.html')
    
    #passenger = Passenger(name=name, flight_id=flight_id)
        #db.session.add(passenger)
        #db.session.commit()
        #return render_template("success.html")    
#def main():
    #db.create_all()
    
    #user1 = User(username = "xaver",email = "x@f.ch",password = "123")
    #db.session.add(user1)
    #db.session.commit()


    
    



#if __name__ == "__main__":
    #with app.app_context():
        #main()     
