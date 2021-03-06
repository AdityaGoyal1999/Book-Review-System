import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

app = Flask(__name__)


""" GOODREADS DATA
key: 5Bnk2patWxtDaOVNSsirw
secret: 49ZzXPNJWPdm5us08IJUjSD1qeTAzTp5AY6Q9hbMs
"""

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Sets up database
engine = create_engine("postgres://jbuimiitaijunf:5e006a287d39930d2922e0a6bdaf1a9e69b73547a92f13f272307a2016d9cf68@ec2-34-200-15-192.compute-1.amazonaws.com:5432/dbm2hr587tr7rj")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    
    return render_template("welcome.html")


@app.route("/signuppage")
def signuppage():

    # using a common page for signup/login so 'signup' indicates the situation
    return render_template("login.html", signup=True, val='None')


@app.route("/loginpage")
def loginpage():

    return render_template("login.html", signup=False, val='None')


@app.route("/signup", methods=["POST"])
def signup():

    name = request.form['name']
    username = request.form['username']
    password = request.form['password']

    users = db.execute("SELECT * FROM users WHERE username=:usnm;",{"usnm": username}).fetchall()
    if(users != []):
        return render_template("login.html", signup=True, val='Username is already taken')

    db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)", {"name":name, "username": username, "password": password})
    db.commit()
    
    # Login to session
    session['username'] = username

    return render_template("search.html", val="None")


@app.route("/login", methods=["POST"])
def login():

    username = request.form['username']
    password = request.form['password']

    check = db.execute("SELECT * FROM users WHERE username = :usnm AND password = :paswd", {"usnm": username, "paswd": password}).fetchone()
    if(check is None):
        return render_template("login.html", signup=False, val='Username or password is wrong')
    
    # Login to session
    session['username'] = username

    return render_template("search.html", val='None')


@app.route("/search/<val>", methods=["POST", "GET"])
def search(val):
    username = session['username']

    try:
        option = request.form['options']
        search = request.form['search']
        # additional spaces removed
        search = search.strip()
    except KeyError:
        # if not option is selected
        return render_template("search.html", val="The search inputs are wrong")

    # if empty string searched
    if(search == ''):
        return render_template("search.html", val="The search inputs are wrong")

    db_query = f"SELECT * FROM books WHERE LOWER({option}) LIKE LOWER('%{search}%');"
    books = db.execute(db_query).fetchall()

    return render_template("books.html", books=books, number=0)


@app.route("/book/<isbn>/<val>")
def book(isbn, val):

    username = session['username']
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).fetchone()

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"5Bnk2patWxtDaOVNSsirw", "isbns": isbn})
    goodreads = res.json()

    local_reviews = db.execute("SELECT * FROM book_reviews WHERE book=:book", {"book": isbn}).fetchall()

    req = requests.get(f"https://www.goodreads.com/book/isbn/{isbn}?format=json", params={"key":"5Bnk2patWxtDaOVNSsirw", "isbn": '{isbn}', "user_id": '115533298'})
    reviews = req.json()

    # Merging the local and goodreads ratings
    sum = 0
    for local_review in local_reviews:
        sum+=local_review[4]
    goodreads_rating = float(goodreads['books'][0]['average_rating'])
    goodreads_number_rating = float(goodreads['books'][0]['work_ratings_count'])
    total_rating = len(local_reviews)+goodreads_number_rating
    average_rating = ((goodreads_number_rating * goodreads_rating) + sum)/total_rating

    return render_template("book.html", book=book, goodreads=goodreads, local_reviews=local_reviews, val=val, average_rating=round(average_rating, 2), total_rating=int(total_rating))


@app.route("/review/<isbn>/<val>", methods=['POST', 'GET'])
def review(isbn, val='None'):
    
    username = session['username']
    review = request.form['review']
    rating = request.form['options']

    req = db.execute(f"SELECT * FROM book_reviews WHERE (username='{username}' AND book='{isbn}');").fetchone()
    if(req is None):
        db.execute("INSERT INTO book_reviews (username, book, review, rating) VALUES (:username, :book, :review, :rating);", {"username":username, "book": isbn, "review": review, "rating": rating})
        db.commit()
        return redirect(url_for('book', isbn=isbn, val='Review Added'))
    else:
        return redirect(url_for('book', isbn=isbn, val='You have already reviewed this book.'))


@app.route("/logout")
def logout():

    session.pop('username',None)
    return redirect(url_for('index'))


@app.route("/api/<isbn>", methods=["GET"])
def info(isbn):

    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if(book is None):
        return render_template("message.html", title="Error 404", message="Page not found")

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"5Bnk2patWxtDaOVNSsirw", "isbns": isbn})
    goodreads = res.json()

    local_reviews = db.execute("SELECT * FROM book_reviews WHERE book=:book", {"book": isbn}).fetchall()
    
    # Merging the local and goodreads ratings
    sum = 0
    for local_review in local_reviews:
        sum+=local_review[4]
    goodreads_rating = float(goodreads['books'][0]['average_rating'])
    goodreads_number_rating = float(goodreads['books'][0]['work_ratings_count'])
    total_rating = len(local_reviews)+goodreads_number_rating
    average_rating = ((goodreads_number_rating * goodreads_rating) + sum)/total_rating

    # Creates json for api
    description = {
    "title": book.title,
    "author": book.author,
    "year": int(book.year),
    "isbn": isbn,
    "review_count": int(total_rating),
    "average_score": round(average_rating, 2)
    }

    return f"{description}"
