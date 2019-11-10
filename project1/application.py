
import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
#@app.route("/search")

def search():
    """Search for a book by ISBN, Title or Author"""
    
    #Get form information
    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")

    books = db.execute("SELECT isbn, title, author, year FROM books JOIN authors ON books.author_id = authors.id WHERE isbn LIKE :isbn AND authors.author LIKE :author AND title LIKE :title", {"isbn": f"%{isbn}%", "author": f"%{author}%", "title": f"%{title}%"}).fetchall()
    if len(books) == 0:
        return render_template("error.html", message="No books were found.")
    else:
        return render_template("books.html", books=books)

@app.route("/book/<isbn>")
def book(isbn):
    """ List details about a book. """

    book = db.execute("SELECT * FROM books JOIN authors ON books.author_id = authors.id WHERE isbn = :isbn", {"isbn": f"{isbn}"}).fetchone()
    if book is None:
        return render_template("error.html", message="No book was found.")
    else:
        return render_template("book.html", book=book)

