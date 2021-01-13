import sqlite3
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap

from settings.config import SECRET_KEY

import auth
from dataset_view_app import app_table_data_view

app = Flask(__name__)
Bootstrap(app)
app.register_blueprint(auth.bp)
app.register_blueprint(app_table_data_view.bp)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list_users')
@auth.login_required
def list_users():
    db = sqlite3.connect('db.report_system')
    cursor = db.cursor()
    cursor.execute('select id, login, firstname, lastname, email from users')
    users_data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('list_users.html', users_data=users_data)


@app.route('/update_user/<int:id_>', methods=['GET', 'POST'])
@auth.login_required
def update_user(id_):
    attributes = ['firstname', 'lastname', 'login', 'email']
    user_data = {k: '' for k in attributes}
    db = sqlite3.connect('db.report_system')
    cursor = db.cursor()
    if request.method == 'GET':
        cursor.execute('select firstname, lastname, login, email from users where id = ?', (id_,))
        data = cursor.fetchone()
        for i in range(len(attributes)):
            user_data[attributes[i]] = data[i]
    if request.method == 'POST':
        firstname = request.form.get('firstname', '')
        lastname = request.form.get('lastname', '')
        login = request.form.get('login', '')
        email = request.form.get('email', '')
        if firstname and lastname and login and email:
            cursor.execute('''update users 
                              set firstname = ?, lastname = ?, login = ?, email = ?
                              where id = ? ''', (firstname, lastname, login, email, id_))
        cursor.close()
        db.commit()
        db.close()
        return redirect(url_for('list_users'))
    cursor.close()
    db.commit()
    db.close()
    return render_template('update_user.html', **user_data)


if __name__ == '__main__':
    app.run(debug=True)
