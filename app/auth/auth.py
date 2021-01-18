from flask import request, redirect, url_for, render_template, flash
from app import app, db, login_manager
from .forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(login=form.login.data,
                    password_hash=form.password.data,
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('auth/register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user is None:
            flash('No such user exists!')
            return render_template('auth/login.html', form=form)
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in Successfully!')

            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('index')
            return redirect(next)
    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('index'))
