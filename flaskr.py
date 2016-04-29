# imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from contextlib import closing

app = Flask(__name__)
app.config.from_object('settings')


def connect_db():
    """Connect to the database specified in configuration"""
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """Initialise the database"""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    """Connect to the database before every request"""
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    """
    Close connection to the database after a response has been constructed
    """
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
