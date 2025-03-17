### default
# module for manipulating dates and times
# https://docs.python.org/3/library/datetime.html
from datetime import datetime

### deps
# provides a light-weight db for prototyping and testing
# https://docs.python.org/3/library/sqlite3.html
import sqlite3

# package for creating command line interfaces
# https://click.palletsprojects.com/en/stable/
import click

# Rather than passing the application around to each function,
# the current_app and g proxies are accessed instead
# current_app - points to the application handling the current activity
# g - simple namespace object that has the same lifetime as an application context
# https://flask.palletsprojects.com/en/stable/appcontext/
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
