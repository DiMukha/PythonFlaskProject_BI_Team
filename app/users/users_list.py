from flask import render_template, redirect, flash, url_for
from flask_login import login_required

from app import app, db
from app.models import User


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


# @app.route('/update_user/<int:id_>', methods=['GET', 'POST'])
# def update_user(id_):
#     attributes = ['firstname', 'lastname', 'login', 'email']
#     user_data = {k: '' for k in attributes}
#     db = sqlite3.connect('db.report_system')
#     cursor = db.cursor()
#     if request.method == 'GET':
#         cursor.execute('select firstname, lastname, login, email from users where id = ?', (id_,))
#         data = cursor.fetchone()
#         for i in range(len(attributes)):
#             user_data[attributes[i]] = data[i]
#     if request.method == 'POST':
#         firstname = request.form.get('firstname', '')
#         lastname = request.form.get('lastname', '')
#         login = request.form.get('login', '')
#         email = request.form.get('email', '')
#         if firstname and lastname and login and email:
#             cursor.execute('''update users
#                               set firstname = ?, lastname = ?, login = ?, email = ?
#                               where id = ? ''', (firstname, lastname, login, email, id_))
#         cursor.close()
#         db.commit()
#         db.close()
#         print('yo')
#         return redirect(url_for('users.list_users'))
#     cursor.close()
#     db.commit()
#     db.close()
#
#     return render_template('users/update_user.html', **user_data)
