import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from facerecogweb import db

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Username/Password is required')
        else:
            user_logged = db.login_user(username, password)
            if not user_logged is None:
                session.clear()
                session['user_id'] = user_logged
                return redirect(url_for('admin.dashboard'))
    else:
        return render_template('login.html', form_url="/", title="Login", loginpage=True)

@bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('index.index'))

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Username/Password is required')
        else:
            db.register_user(username, password)
            user_logged = db.login_user(username, password)
            if not user_logged is None:
                session.clear()
                session['username'] = user_logged.username
                return redirect(url_for('admin.dashboard'))
    else:
        names = db.retrieve_names()
        for name in names:
            print(str(name))
        return render_template('login.html', form_url="/register", title="Register", loginpage=False)
