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

# Configure session to use filesystem

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

    # res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"5Bnk2patWxtDaOVNSsirw", "isbns": "9781632168146"})
    # print(res.json())
    
    return render_template("welcome.html")

@app.route("/login", methods=["POST"])
def login():

    username = request.form['username']
    password = request.form['password']

    check = db.execute("SELECT * FROM users WHERE username = :usnm AND password = :paswd", {"usnm": username, "paswd": password}).fetchone()
    if(check is None):
        return "Invalid username or password"
    return render_template("search.html")

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
    return render_template("search.html")


@app.route("/search", methods=["POST", "GET"])
def search():
    
    option = request.form['options']
    search = request.form['search']

    print(option, search)
    db_query = f"SELECT * FROM books WHERE {option} LIKE '%{search}%';"
    books = db.execute(db_query).fetchall()
    print(books)

    return render_template("searchResults.html", books=books, number=0)


# TODO: This is not working
@app.route("/book")
def book():

    return "This is the book"