import os
from flask import Flask, render_template, request
from models import *
import smtplib
import config

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
    password = request.form.get("password")        
    user = User(username = username, email = email, password = password)
    db.session.add(user)
    #send email to user after registration
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

@app.route("/sign_out", methods=["POST"])
def sign_out():
    return render_template('index.html', message="You are logged out")

@app.route("/search", methods=["POST"])
def search():
    #isbn = request.form.get("isbn")
    #title = request.form.get("title")
    #author = request.form.get("author")
    #year = request.form.get("year")    
    #if isbn is None:
        #if title is None:
            #if author is None:
                #results = Book.query.filter_by(year = year).all()                                
            #else: 
                #results = Book.query.filter_by(author = author).all()                
        #else:
            #results = Book.query.filter_by(title = title).all()            
    #else:
        #results = Book.query.filter_by(isbn = isbn).all()
    #return render_template('search_results.html', results = results)
    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")
    year = request.form.get("year")    
    results_isbn = Book.query.filter_by(isbn = isbn).all()   
    results_title = Book.query.filter_by(title = title).all()        
    results_author = Book.query.filter_by(author = author).all()        
    results_year = Book.query.filter_by(year = year).all()        
    
                
    return render_template('search_results.html', results_isbn = results_isbn, results_title = results_title, results_author = results_author, results_year = results_year)    
    

       




if __name__ == "__main__":
    with app.app_context():
        main()     
