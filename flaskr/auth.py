# default
# Functools module is for higher-order functions that work on other functions.
# https://www.geeksforgeeks.org/functools-module-in-python/
import functools

# deps
# Blueprints can greatly simplify how large applications work and provide a central means for
# Flask extensions to register operations on applications.
# https://flask.palletsprojects.com/en/stable/blueprints/
# -----------------------------------------------------------
# Flask provides a really simple way to give feedback to a user with the flashing system.
# https://flask.palletsprojects.com/en/stable/patterns/flashing/
# -----------------------------------------------------------
# g - simple namespace object that has the same lifetime as an application context
# https://flask.palletsprojects.com/en/stable/appcontext/
# -----------------------------------------------------------
# A redirect is used in the Flask class to send the user to a particular URL with the status code.
# https://www.geeksforgeeks.org/redirecting-to-url-in-flask/
# -----------------------------------------------------------
# render_template in Flask is used to render HTML templates with dynamic data
# Google AI
# -----------------------------------------------------------
# In Flask, the request object provides access to incoming request data.
# Google AI
# -----------------------------------------------------------
# In Flask, sessions enable storing user-specific data across multiple requests.
# Google AI
# -----------------------------------------------------------
# The url_for() method, is used to prepare a URL, for a function dynamically,
# such that, changing URLs, in the application, is avoided.
# https://www.geeksforgeeks.org/flask-url-helper-function-flask-url_for/
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# -----------------------------------------------------------
# werkzeug.check_password_hash - check a password against a given salted and hashed password value.
# https://tedboy.github.io/flask/generated/werkzeug.check_password_hash.html
# -----------------------------------------------------------
# werkzeug.generate_password_hash - Hash a password with the given method and salt with with a string of the given length
# https://tedboy.github.io/flask/generated/werkzeug.generate_password_hash.html?highlight=generate_password_hash
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM user WHERE useranme = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
