import os
import sqlite3

from flask import (Flask, request, session, g, redirect, url_for, abort, render_template, flash)


app = Flask(__name__) # create the application instance =)
app.config.from_object(__name__) # load the config from this file, flaskr.py

# load default config and override config from an environment variable
app.config.update(
    DATABASE = os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY = b'fgnfg45n4fgn44fgn4fg(-)',
    USERNAME = 'admin',
    PASSWORD = 'default',
)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries(title, text) values (?, ?)',
                [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries')
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_db():
    """Opens a new database connection if there is none yet for the current appliication context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def connect_db():
    """Connect to the specific database"""
    cnx = sqlite3.connect(app.config['DATABASE'])
    cnx.row_factory = sqlite3.Row

    return cnx


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as file:
        db.cursor().executescript(file.read())

    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
