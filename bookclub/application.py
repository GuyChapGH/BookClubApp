import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import datetime

from helpers import apology, login_required, lookup, hudate, usd

# Configure application
app = Flask(__name__)

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

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bookclub.db")


@app.route("/")
@login_required
def index():
    """Show book club meetings"""
    # SQL query to capture meetings ahead of or on today's date
    rows = db.execute(
        "SELECT * FROM meetings WHERE meetingDATE >= date('now', 'localtime')")

    # Loop through rows replacing machine date with human readable format
    for i in range(len(rows)):
        rows[i]['meetingDATE'] = hudate(rows[i]['meetingDATE'])
    
    return render_template("index.html", meetings=rows)


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

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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
        db.execute("DELETE FROM searchresults")
        db.execute("VACUUM")
    
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
        for book in books:
            db.execute("INSERT INTO searchresults (title, authors, ISBN, description, image) VALUES (:title, :authors, :ISBN, :description, :image)",
                       title=book['title'], authors=book['authors'], ISBN=book['ISBN'], description=book['description'], image=book['image'])
       
    # SQL query to get searchresults from database
        rows = db.execute(
        "SELECT queryID, title, authors, ISBN FROM searchresults")
        
       # return render_template("queryresponse.html", booktitle = booktitle, authors = authors, isbn = isbn, description = description, image = image)
       # return render_template("queryresponse.html", books=books)
        return render_template("queryresponse.html", books=rows)

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
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"), hash=hash)

        if not result:
            return apology("username not available", 400)

        # Log user in automatically

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Store user_id in session
        session["user_id"] = rows[0]["id"]

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
        result = db.execute("INSERT INTO meetings (meetingDATE, id) VALUES (:meetingdate, :user_id)",
                            meetingdate=request.form.get("meetingdate"), user_id=user_id)
        
        if not result:
            return apology("Meeting date not available", 400)
        
        # Add book details to meetingDATE row in meetings table by SELECT from searchresults table 
        res = db.execute("UPDATE meetings SET queryID = (SELECT queryID FROM searchresults WHERE queryID = :searchresult), title = (SELECT title FROM searchresults WHERE queryID = :searchresult), authors = (SELECT authors FROM searchresults WHERE queryID = :searchresult), ISBN = (SELECT ISBN FROM searchresults WHERE queryID = :searchresult), description = (SELECT description FROM searchresults WHERE queryID = :searchresult), image = (SELECT image FROM searchresults WHERE queryID = :searchresult) WHERE meetingDATE = :meetingdate",
                        meetingdate = request.form.get("meetingdate"), searchresult = request.form.get("searchresult"))
                        
        if not res:
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
