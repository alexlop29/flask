# __init___ creates a package

# default
import os

# deps
from flask import Flask
from . import db


def create_app(test_config=None):
    # Creates the flask instance
    # __name__ is the name of the current Python module.
    # instance_relative_config=True tells the app that configuration files are relative to the instance folder.
    app = Flask(__name__, instance_relative_config=True)

    # Sets default configuration options
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exist, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database
    db.init_app(app)

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
