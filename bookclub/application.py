import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from .helpers import apology, login_required, lookup, hudate, usd

# Configure application
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Function defined to fetch environment variables
def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected variable '{}' not set.".format(name)
        raise Exception(message)


# The environment variables are fetched from the bin/activate of the virtualenv
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

# The connection to the database is specified
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Define users table with three columns id, username and hash


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    hash = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, username, hash):
        self.username = username
        self.hash = hash

# Define searchresults table


class Searchresults(db.Model):
    queryID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    authors = db.Column(db.Text, nullable=False)
    ISBN = db.Column(db.String(80), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)

    def __init__(self, title, authors, ISBN, description, image):
        self.title = title
        self.authors = authors
        self.ISBN = ISBN
        self.description = description
        self.image = image

# Define meetings table


class Meetings(db.Model):
    meetingID = db.Column(db.Integer, primary_key=True)
    meetingDATE = db.Column(db.DateTime, unique=True, nullable=False)
    location = db.Column(db.Text, nullable=True)
    id = db.Column(db.Integer, nullable=True)
    queryID = db.Column(db.Integer, nullable=True)
    title = db.Column(db.Text, nullable=True)
    authors = db.Column(db.Text, nullable=True)
    ISBN = db.Column(db.String(80), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.Text, nullable=True)

    def __init__(self, meetingDATE, location, id, queryID, title, authors, ISBN, description, image):
        self.meetingDATE = meetingDATE
        self.location = location
        self.id = id
        self.queryID = queryID
        self.title = title
        self.authors = authors
        self.ISBN = ISBN
        self.description = description
        self.image = image


@app.route("/")
@login_required
def index():
    """Show book club meetings"""
    # SQL query to capture meetings ahead of or on today's date
    # rows = db.execute(
    #    "SELECT * FROM meetings WHERE meetingDATE >= date('now', 'localtime')")

    # Loop through rows replacing machine date with human readable format
    # for i in range(len(rows)):
    #    rows[i]['meetingDATE'] = hudate(rows[i]['meetingDATE'])

    # SQLAlchemy to filter only for meetings after today's date and order by meetingDATE

    todays_datetime = datetime.today()

    return render_template("index.html", meetings=Meetings.query.filter(Meetings.meetingDATE >= todays_datetime).order_by(Meetings.meetingDATE).all())


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return apology("TODO")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username using SQLAlchemy
        # rows = db.execute("SELECT * FROM users WHERE username = :username",
        #                  username=request.form.get("username"))
        username = request.form.get("username")
        rows = Users.query.filter_by(username=username).first()

        # Ensure username exists and password is correct
        # if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        #    return apology("invalid username and/or password", 403)

        if rows is None or not check_password_hash(rows.hash, request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in. ERROR HERE rows is an object Not
        # an array. Try rows.id?
        session["user_id"] = rows.id

        # Redirect user to home page
        return redirect("/")

        # Redirect user to "/Query" while testing
        # return redirect("/query")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/query", methods=["GET", "POST"])
@login_required
def query():
    """Get query."""

# Display query page as user reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("query.html")

    #  User reached route via POST (as by submitting a form via POST)
    else:
        # If query field left blank give apology
        if not request.form.get("query"):
            return apology("must provide query", 400)

    # Clear database table searchresults of previous data and clear unused space
    #    db.execute("DELETE FROM searchresults")
        try:
            num_rows_deleted = db.session.query(Searchresults).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)

    # Don't need VACUUM as automatic in Postgresql
    #    db.execute("VACUUM")

    # Request books from lookup function
        books = lookup(request.form.get("query"))
        #response = lookup(request.form.get("query"))
    # If query not recognised give apology
    #    if not books:
    #        return apology("query error", 400)

        #booktitle = books[0].get('title')
        #authors = books[0].get('authors')
        #isbn = books[0].get('ISBN')
        #description = books[0].get('description')
        #image = books[0].get('image')
        #items = len(response['items'])
        #title = response['items'][5]['volumeInfo']['title']

    # SQL query to write books into database table 'searchresults'
    #    for book in books:
    #        db.execute("INSERT INTO searchresults (title, authors, ISBN, description, image) VALUES (:title, :authors, :ISBN, :description, :image)",
    #                   title=book['title'], authors=book['authors'], ISBN=book['ISBN'], description=book['description'], image=book['image'])

    # SQLAlchemy code to add book data to database table searchresults. Committing one row at a time

        for book in books:
            new_row = Searchresults(book['title'], book['authors'],
                                    book['ISBN'], book['description'], book['image'])
            db.session.add(new_row)

    # Commit new_row
            try:
                db.session.commit()
            except Exception as e:
                print (e)

    # SQL query to get searchresults from database
    #    rows = db.execute(
    #        "SELECT queryID, title, authors, ISBN FROM searchresults")

       # return render_template("queryresponse.html", booktitle = booktitle, authors = authors, isbn = isbn, description = description, image = image)
       # return render_template("queryresponse.html", books=books)
       # Add SQLAlchemy to render_template to get searchresults from database
        return render_template("queryresponse.html", books=Searchresults.query.all())


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password and confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # Generate hash of password
        hash = generate_password_hash(request.form.get("password"))

        # Insert user into users table of finance.db, check for username availabilty
        # result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
        #                    username=request.form.get("username"), hash=hash)
        username = request.form.get("username")
        new_user = Users(username, hash)

        db.session.add(new_user)

        # Need to handle exception in the case that the username is already taken. Usernames
        # are unique therefore commit() will fail. NEED TO IMPROVE ERROR HANDLING HERE
        result = True
        try:
            db.session.commit()
        except Exception as e:
            print (e)
            result = False

        if not result:
            return apology("username not available", 400)

        # Log user in automatically

        # Query database for username using SQLAlchemy
        # rows = db.execute("SELECT * FROM users WHERE username = :username",
        #                  username=request.form.get("username"))

        username = request.form.get("username")
        rows = Users.query.filter_by(username=username).first()

        # Store user_id in session
        session["user_id"] = rows.id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/assign", methods=["GET", "POST"])
@login_required
def assign():
    """Assign selected book to meeting"""
    # Display query page if user reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("query.html")

    #  User reached route via POST (as by submitting a form via POST)
    else:
        # If query field left blank give apology
        if not request.form.get("meetingdate"):
            return apology("must provide meeting date", 400)

        # If book selection left blank give apology
        elif not request.form.get("searchresult"):
            return apology("must provide book choice", 400)

        # Get current id of user
        user_id = session["user_id"]

        # Attempt to insert meetingdate and user_id into meetings table, check for meeting date availability (meetingDATE is unique field)
        # result = db.execute("INSERT INTO meetings (meetingDATE, id) VALUES (:meetingdate, :user_id)",
        #                     meetingdate=request.form.get("meetingdate"), user_id=user_id)

        meetingdate = request.form.get("meetingdate")

        # Use of 'None' should line up values with their correct columns in the meetings table

        new_meeting = Meetings(meetingdate, None, user_id, None, None, None, None, None, None)

        db.session.add(new_meeting)

        # Need to handle exception in the case that the meetingDATE is already taken. MeetingDATE
        # is unique therefore commit() will fail. NEED TO IMPROVE ERROR HANDLING HERE
        result = True
        try:
            db.session.commit()
        except Exception as e:
            print (e)
            result = False

        if not result:
            return apology("Meeting date not available", 400)

        # Add book details to meetingDATE row in meetings table by SELECT from searchresults table
        # Can't find ORM method to do this therefore going to use raw SQL. Note use of single quotes around query and
        # double quotes around column titles. Postgresql automatically converts column titles to lowercase
        # otherwise.

        flag = True
        try:
            db.session.execute('UPDATE meetings SET "queryID" = searchresults."queryID", title = searchresults.title, authors = searchresults.authors, "ISBN" = searchresults."ISBN", description = searchresults.description, image = searchresults.image FROM searchresults WHERE searchresults."queryID" = :searchresult AND meetings."meetingDATE" = :meetingdate', {
                'meetingdate': request.form.get("meetingdate"), 'searchresult': request.form.get("searchresult")})
            db.session.commit()

        except Exception as e:
            print (e)
            flag = False

        if not flag:
            return apology("book details not inserted")

        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
