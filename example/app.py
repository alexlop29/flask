from flask import Flask, request, render_template

# Importing escape from markupsafe to sanitize user input
from markupsafe import escape

# Initialize the Flask application
app = Flask(__name__)

# Demonstrates a simple route
@app.route('/')
def hello_world():
    return '<p>Hello, Alex!</p>'

# Demonstrates sanitization of user input
@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

# Demonstrates handling various HTTP methods in a route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "Handling POST request"
    else:
        return "Handling GET request"

# Demonstrates an alternative way to handle different HTTP methods
@app.get("/login2")
def login_get():
    return "Handling GET request"
@app.post("/login2")
def login_post():
    return "Handling POST request"

# Demonstrates rendering a template
@app.route("/hello/<name>")
def hello_with_template(name=None):
    return render_template("hello.html", person=name)