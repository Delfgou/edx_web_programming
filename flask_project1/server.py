import os
from flask import Flask, render_template, request
from models import *
import smtplib
import config
from sqlalchemy import or_

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vhltvfuekxyisp:4e8e3284506f4903c26843cbeca2e8bc2ed4693c95ddd2dd8f104550c5700e27@ec2-79-125-6-250.eu-west-1.compute.amazonaws.com:5432/d4j9oravts15j7"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    return render_template('index.html', message="Welcome!")

@app.route("/go_register", methods=["POST"])
def go_to_register():
    return render_template('register.html')

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")   
    email = request.form.get("email")
    if "@" not in email:
        return render_template("error.html", message = "Invalid email address")
    password = request.form.get("password")        
    user = User(username = username, email = email, password = password)
    Check_db = User.query.filter(or_(User.username == username, User.email == email)).first()
    if Check_db is None:        
        #send email to user after registration
        try:
            db.session.add(user) 
            EMAIL_TO = email
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(config.EMAIL_FROM,config.PASSWORD)
            subject = "Test. Welcome to books3000"
            msg = "Hello {}. Thank you for your registration. This email has been sent automatically after your registration.".format(username)
            message = 'Subject: {}\n\n{}'.format(subject,msg)
            server.sendmail(config.EMAIL_FROM,EMAIL_TO, message)
            server.quit()
            print("Success: Email sent!")   
            db.session.commit()
            return render_template('success.html')
        except:
            return render_template("error.html", message = "Invalid email address")
    else:
        return render_template('error.html', message = "Username or email has already been used")

@app.route("/sign_in", methods=["POST"])
def sign_in():
    input_user = request.form.get("username")
    input_password = request.form.get("password")  
    if " " in input_user or " " in input_password:
        return render_template('error.html', message = "You're trying to hack us!")    
    user = User.query.filter_by(username = input_user, password = input_password).first()
    
    if user is None:
        return render_template("error.html", message="You are not registered")    
    return render_template('welcome.html', message = input_user)

@app.route("/go_to_search", methods=["POST"])
def go_to_search():
    return render_template('welcome.html', message = "again")

@app.route("/sign_out", methods=["POST"])
def sign_out():
    return render_template('index.html', message="You are logged out")

@app.route("/search", methods=["POST"])
def search():
    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")
    year = request.form.get("year")     
    results_isbn = Book.query.filter(Book.isbn.ilike(f"%{isbn}%")).all()
    results_title = Book.query.filter(Book.title.ilike(f"%{title}%")).all()
    results_author = Book.query.filter(Book.author.ilike(f"%{author}%")).all()
    results_year = Book.query.filter(Book.year.ilike(f"%{year}%")).all()
    results = Book.query.filter(Book.isbn.ilike(f"%{isbn}%"),Book.title.ilike(f"%{title}%"),Book.author.ilike(f"%{author}%"),Book.year.ilike(f"%{year}%")).all()
    return render_template('search_results.html', results = results)    
    

@app.route("/<string:book>", methods =["post"])
def details(book):
    return f"Hello, {book}!"



if __name__ == "__main__":
    with app.app_context():
        main()     
