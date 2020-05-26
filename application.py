import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

app = Flask(__name__)

# Check for environment variable

# TODO: How do we run this line instead?
# if not os.getenv("postgres://wulnronkubqzoy:33880c816471a23ae0fb3ccf19871e1f52f8dbe9f0102c57d479c39b706e923e@ec2-52-87-135-240.compute-1.amazonaws.com:5432/d9i2hu0qmbc0jm"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystemre

""" GOODREADS
key: 5Bnk2patWxtDaOVNSsirw
secret: 49ZzXPNJWPdm5us08IJUjSD1qeTAzTp5AY6Q9hbMs
"""

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgres://jbuimiitaijunf:5e006a287d39930d2922e0a6bdaf1a9e69b73547a92f13f272307a2016d9cf68@ec2-34-200-15-192.compute-1.amazonaws.com:5432/dbm2hr587tr7rj")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    
    return render_template("welcome.html")

@app.route("/login", methods=["POST"])
def login():

    username = request.form['username']
    password = request.form['password']

    check = db.execute("SELECT * FROM users WHERE username = :usnm AND password = :paswd", {"usnm": username, "paswd": password}).fetchone()
    if(check is None):
        return "Invalid username or password"

    return render_template("search.html", username=username)

@app.route("/signuppage")
def signuppage():

    return render_template("login.html", signup=True)


@app.route("/loginpage")
def loginpage():

    return render_template("login.html", signup=False)


@app.route("/signup", methods=["POST"])
def signup():

    name = request.form['name']
    username = request.form['username']
    password = request.form['password']

    users = db.execute("SELECT * FROM users WHERE username=:usnm;",{"usnm": username}).fetchall()
    if(users != []):
        return "User already exists"
    db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)", {"name":name, "username": username, "password": password})
    db.commit()

    return render_template("search.html", username=username)

# TODO: search button not working in nav
@app.route("/search/<username>", methods=["POST", "GET"])
def search(username):
    
    option = request.form['options']
    search = request.form['search']
    # search = search.strip()

    # print(option, search)
    db_query = f"SELECT * FROM books WHERE LOWER({option}) LIKE LOWER('%{search}%');"
    books = db.execute(db_query).fetchall()
    print(books)

    return render_template("searchResults.html", books=books, number=0, username=username)


# TODO: This is not working
@app.route("/book/<isbn>/<username>")
def book(isbn, username):

    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).fetchone()

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"5Bnk2patWxtDaOVNSsirw", "isbns": isbn})
    goodreads = res.json()

    req = requests.get(f"https://www.goodreads.com/book/isbn/{isbn}?format=json", params={"key":"5Bnk2patWxtDaOVNSsirw", "isbn": '{isbn}', "user_id": '115533298'})
    reviews = req.json()
    print(reviews['reviews_widget'])


    return render_template("book.html", book=book, goodreads=goodreads, username=username)


@app.route("/review/<isbn>/<username>", methods=['POST', 'GET'])
def review(isbn, username):
    
    review = request.form['review']
    req = db.execute(f"SELECT * FROM reviews WHERE (username='{username}' AND book='{isbn}');").fetchone()
    if(req is None):
        db.execute("INSERT INTO reviews (username, book, review) VALUES (:username, :book, :review);", {"username":username, "book": isbn, "review": review})
        db.commit()
        return "Added"
    else:
        return "You cannot add review for the same book twice"

    return "Never reaching"

@app.route("/about")
def about():

    return render_template("about.html")


@app.route("/api/<isbn>", methods=["GET"])
def info(isbn):

    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    # TODO: Make this better
    if(book is None):
        return render_template("message.html", title="Error 404", message="Page not found")

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"5Bnk2patWxtDaOVNSsirw", "isbns": isbn})
    goodreads = res.json()


    description = {
    "title": book.title,
    "author": book.author,
    "year": int(book.year),
    "isbn": isbn,
    "review_count": goodreads['books'][0]['reviews_count'],
    "average_score": float(goodreads['books'][0]['average_rating'])
    }

    return f"{description}"
