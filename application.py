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
engine = create_engine("postgres://wulnronkubqzoy:33880c816471a23ae0fb3ccf19871e1f52f8dbe9f0102c57d479c39b706e923e@ec2-52-87-135-240.compute-1.amazonaws.com:5432/d9i2hu0qmbc0jm")
db = scoped_session(sessionmaker(bind=engine))

# TODO: need a way to change global one locally
signup = True

@app.route("/")
def index():

    # res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key":"5Bnk2patWxtDaOVNSsirw", "isbns": "9781632168146"})
    # print(res.json())

    # return "Project 1: TODO"
    signup = True
    return render_template("login.html", signup=signup)

@app.route("/login", methods=["POST"])
def login():

    username = request.form['username']
    password = request.form['password']

    check = db.execute("SELECT * FROM users WHERE username = :usnm AND password = :paswd", {"usnm": username, "paswd": password}).fetchone()
    if(check is None):
        return "Invalid username or password"
    return "You are logged in"


@app.route("/signup")
def signup():

    name = request.form['name']
    username = request.form['username']
    password = request.form['password']

    users = db.execute("SELECT * FROM users WHERE username=:usnm;",{"usnm": username}).fetchall()
    if(users != []):
        return "User already exists"
    db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)", {"name":name, "username": username, "password": password})
    db.commit()
    return "You have created an account"