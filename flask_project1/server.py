import os
from flask import Flask, render_template, request, session, url_for
from models import *
import config
from sqlalchemy import or_
from flask_session import Session
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired



app = Flask(__name__)
app.config.from_pyfile('config.py')
mail = Mail(app)
s = URLSafeTimedSerializer('Thisisasecret!')
app.secret_key = "any random string"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://vhltvfuekxyisp:4e8e3284506f4903c26843cbeca2e8bc2ed4693c95ddd2dd8f104550c5700e27@ec2-79-125-6-250.eu-west-1.compute.amazonaws.com:5432/d4j9oravts15j7"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/register',methods=['GET','POST'])
def register():
    
    username = request.form.get("username")   
    email = request.form.get("email")   
    password = request.form.get("password")
    user = User(username = username, email = email, password = password,confirmed=False)
    Check_db = User.query.filter(or_(User.username == username, User.email == email)).first()
    if Check_db is None:
        db.session.add(user)
        db.session.commit()
        token = s.dumps(email, salt = 'email-confirm')
        
        msg = Message('Confirm Email', sender='c.delfg@gmail.com', recipients=[email])
        
        link = url_for('confirm_email', token = token, _external=True)
        msg.body =  'Your link is {}'.format(link)
        mail.send(msg)
        
    return 'An email with a confirmation link has been sent to your email address'

@app.route('/confirm_email/<token>/<email>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        
    except SignatureExpired:
        return '<h1>The token is expired</h1>'
    return 'The token works!'


@app.route("/register", methods=["POST"])
#def register():
    #username = request.form.get("username")   
    #email = request.form.get("email")
    #if "@" not in email:
        #return render_template("error.html", message = "Invalid email address")
    #password = request.form.get("password")        
    #user = User(username = username, email = email, password = password,confirmed=False)
    #Check_db = User.query.filter(or_(User.username == username, User.email == email)).first()
    #if Check_db is None:        
        ##send email to user after registration
        #try:
            #db.session.add(user) 
            #EMAIL_TO = email
            #server = smtplib.SMTP('smtp.gmail.com:587')
            #server.ehlo()
            #server.starttls()
            #server.login(config.EMAIL_FROM,config.PASSWORD)
            #subject = "Test. Welcome to books3000"
            #msg = "Hello {}. Thank you for your registration. This email has been sent automatically after your registration.".format(username)
            #message = 'Subject: {}\n\n{}'.format(subject,msg)
            #server.sendmail(config.EMAIL_FROM,EMAIL_TO, message)
            #server.quit()
            #print("Success: Email sent!")   
            #db.session.commit()
            #return render_template('success.html')
        #except:
            #return render_template("error.html", message = "Invalid email address")
    #else:
        #return render_template('error.html', message = "Username or email has already been used")

@app.route("/")
def index():
    return render_template('index.html', message="Welcome!")

@app.route("/go_register", methods=["POST"])
def go_to_register():
    return render_template('register.html')


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    input_user = request.form.get("username")
    input_password = request.form.get("password")  
    session['username'] = request.form['username']
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
    rating = request.form.get("rating") 
    comment = request.form.get("comment") 
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
