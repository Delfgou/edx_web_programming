import os
from flask import Flask, render_template, request, session, url_for, escape
from werkzeug.security import generate_password_hash, check_password_hash, gen_salt
from models import *
import config
from sqlalchemy import or_
from flask_session import Session
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import requests
from string import ascii_letters
from random import choice



app = Flask(__name__)
app.config.from_pyfile('config.py')
s = URLSafeTimedSerializer('\x00\xb7\x14Y\x19\xbc\xab*\xd7\x99\xe7-\xe1\xf1\xee\x1b\x800\xe4\xc9\xe9\x06\x142')
mail = Mail(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vhltvfuekxyisp:4e8e3284506f4903c26843cbeca2e8bc2ed4693c95ddd2dd8f104550c5700e27@ec2-79-125-6-250.eu-west-1.compute.amazonaws.com:5432/d4j9oravts15j7"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.secret_key = "3i\xf2\xf5@\xa5\xdb\xc7m\xe8_U\x16\xc5a6\x04\x1d\xee]\xb9\x9fS\x89"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/register',methods=['POST'])
def register():
    username = escape(request.form.get("username"))   
    email = escape(request.form.get("email"))  
    salt = gen_salt(5)    
    pepper = choice(ascii_letters)
    password = generate_password_hash(f'{escape(request.form.get("password"))}{salt}{pepper}')
    session['username'] = escape(request.form['username'])    
    user = User(username = username, email = email, salt = salt, password = password,confirmed=False)
    Check_db = User.query.filter(or_(User.username == username, User.email == email)).first()
    if Check_db is None:
        db.session.add(user)
        db.session.commit()        
        token = s.dumps(email, salt = 'email-confirm')
        msg = Message('Confirm Email', sender='hansbooks3000@gmail.com', recipients=[email])
        link = url_for('confirm_email', token = token, _external=True, username=username)
        msg.body =  'Your link is {}'.format(link)
        mail.send(msg)        
        session['username'] = escape(request.form['username'])     
    return '<h1>An email with a confirmation link has been sent to your email address</h1>'

@app.route('/confirm_email/<token>/<username>')
def confirm_email(token,username):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        confirm_user = User.query.filter(User.email == email).first()
        confirm_user.confirmed = True
        db.session.commit()        
    except SignatureExpired:
        return '<h1>The token is expired</h1>'
    return render_template('welcome.html', message = username)

@app.route("/")
def index():
    return render_template('index.html', message="Welcome!")

@app.route("/go_register", methods=["POST"])
def go_to_register():
    return render_template('register.html')


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    input_user = escape(request.form.get("username"))
    session['username'] = escape(request.form['username']) 
    user = User.query.filter_by(username = input_user, confirmed = True).first()
    if user is None:
        return render_template("error.html", message="You are not registered")    
    db_password = (User.query.filter_by(username = input_user, confirmed = True).first()).password
    db_salt = (User.query.filter_by(username = input_user, confirmed = True).first()).salt
    input_password = f'{escape(request.form.get("password"))}{db_salt}'    
    for character in ascii_letters:
        if check_password_hash(db_password,f'{input_password}{character}'):            
            return render_template('welcome.html', message = input_user)    
    return render_template("error.html", message="Wrong password")

@app.route('/forgot_password', methods = ['post'])
def forgot_password():
    return render_template('reset_password.html')

@app.route('/reset_password', methods = ['post'])
def reset_password():
    email = escape(request.form.get("email"))
    new_password = ''.join(choice(ascii_letters) for i in range(12))
    change_password = User.query.filter(User.email == email).first()
    salt = change_password.salt 
    pepper = choice(ascii_letters)
    new_hash = generate_password_hash(f'{new_password}{salt}{pepper}')    
    change_password.password = new_hash    
    
    return 'Success'
    
    
    

@app.route("/go_to_search", methods=["POST"])
def go_to_search():
    return render_template('welcome.html', message = "again")

@app.route("/sign_out", methods=["POST"])
def sign_out():
    session.pop('username', None)
    return render_template('index.html', message="You are logged out")

@app.route("/search", methods=["POST"])
def search():
    isbn = escape(request.form.get("isbn"))
    title = escape(request.form.get("title"))
    author = escape(request.form.get("author"))
    year = escape(request.form.get("year"))    
    results_isbn = Book.query.filter(Book.isbn.ilike(f"%{isbn}%")).all()
    results_title = Book.query.filter(Book.title.ilike(f"%{title}%")).all()
    results_author = Book.query.filter(Book.author.ilike(f"%{author}%")).all()
    results_year = Book.query.filter(Book.year.ilike(f"%{year}%")).all()
    results = Book.query.filter(Book.isbn.ilike(f"%{isbn}%"),Book.title.ilike(f"%{title}%"),Book.author.ilike(f"%{author}%"),Book.year.ilike(f"%{year}%")).all()
    if results== []:
        return render_template('error.html', message = "No results")
    return render_template('search_results.html', results = results)    
    

@app.route("/<string:isbn>/<string:title>/<string:author>/<string:year>", methods =["post"])
def details(isbn,title,author,year):
    key = "IhQrUp1cuWV8mu4SOw7QTQ"
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key, "isbns": isbn})
    numb = res.json()['books'][0]['ratings_count']
    avg = res.json()['books'][0]['average_rating']
    return render_template('page_book.html', isbn=isbn, title=title, author=author,year=year,avg=avg, numb=numb)


@app.route("/rating/<string:isbn>", methods =["post"])
def rating(isbn):
    rating = escape(request.form.get("rating")) 
    comment = escape(request.form.get("comment"))
    try: 
        review = Review(isbn = isbn, rating = rating, comment = comment)
        db.session.add(review)
        db.session.commit()        
        return render_template('success.html')
    except:
        return render_template('error.html', message = "Rating must be a number!")
    


if __name__ == "__main__":
    with app.app_context():
        main()     
