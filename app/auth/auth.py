import functools

from flask import Blueprint, request, redirect, url_for, render_template, flash, session, g
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    username = email = firstname = lastname = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        db = get_db()
        error = None

        if not password:
            error = 'Password is required.'
        if not email:
            error = 'Email is required.'
        if not username:
            error = 'Username is required.'
        if db.execute(
                'SELECT id FROM users WHERE login = ? or email = ?',
                (username, email,)
        ).fetchone() is not None:
            error = 'User {} or {} is already registered.'.format(username, email)

        if error is None:
            db.execute(
                'INSERT INTO users (login, email, password, firstname, lastname) VALUES (?, ?, ?, ?, ?)',
                (username, email, generate_password_hash(password), firstname, lastname)
            )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html', username=username, email=email, firstname=firstname, lastname=lastname)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    username = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None
        user = db.execute(
            'SELECT id, login as username, email, password, firstname, lastname FROM users WHERE login = ?', (username,)
        ).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html', username=username)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT id, login as username FROM users WHERE id = ?',
            (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
