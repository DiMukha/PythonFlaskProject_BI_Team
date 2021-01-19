from flask import render_template, redirect, flash, url_for, request
from flask_login import login_required

from app import app, db
from app.models import User
from .forms import UpdateForm


@app.route('/list_users')
@login_required
def list_users():
    users = User.query.all()
    return render_template('users/list_users.html', users=users)


@app.route('/delete_user/<login>', methods=['GET', 'POST'])
@login_required
def delete_user(login):
    user = User.query.filter_by(login=login).first()
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.login} is deleted!')
    return redirect(url_for('index'))


@app.route('/update_user/<login>', methods=['GET', 'POST'])
@login_required
def update_user(login):
    user = User.query.filter_by(login=login).first()
    form = UpdateForm()
    print(form.validate_on_submit())
    if request.method == 'POST' and form.validate_on_submit():
        print(request.method)
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.last_name.data
        db.session.commit()
        flash(f'User {user.login} is updated!')
        return redirect(url_for('list_users'))
    return render_template('users/update_user.html', form=form, user=user)

