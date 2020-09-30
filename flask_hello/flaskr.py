# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

DATABASE="/tmp/flaskr.db"
SECRET_KEY = 'development key'

app = Flask(__name__)  # 创建 Flask 应用
app.config.from_object(__name__)
app.secret_key = 'abc'  # 设置表单交互密钥
app.debug = True

#export FLASKR_SETTINGS=./setting.cfg
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
db = ''


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with app.app_context():
        g.db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            g.db.cursor().executescript(f.read())
        g.db.commit()

@app.route('/')
def show_entries():
    # if not hasattr(g, 'db'):
    #     get_db()
    #     if g.db is None:
    #         return "Not Found db "
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    # if not hasattr(g, 'db'):
    #     get_db()
    #     if g.db is None:
    #         return "Not Found db "
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/user/<username>')
def profile(username): pass

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def test():
    with app.test_request_context():
        print( url_for("logout", abc="def", deff="cde") )
        print( url_for("profile", username="hello") )
        print( url_for("static", filename="style.css"))




if __name__ == '__main__':
    init_db()
    test()
    app.run(host='0.0.0.0', port=80)
