import sqlite3
from flask import Flask, render_template, request, url_for, redirect, send_file, flash
from flask_bootstrap import Bootstrap
import pandas as pd

import auth
import db
import data_export


app = Flask(__name__)
Bootstrap(app)
db.init_app(app)
app.register_blueprint(auth.bp)
app.config['SECRET_KEY'] = '#$tyty4%^&*oijh454dfg53267GHJ56##8'


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/list_users')
def list_users():
    db = sqlite3.connect('db.report_system')
    cursor = db.cursor()
    cursor.execute('select id, login, firstname, lastname, email from users')
    users_data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('list_users.html', users_data=users_data)



@app.route('/update_user/<int:id_>', methods=['GET', 'POST'])
def update_user(id_=1):
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


@app.route('/send_xlsx')
def send_xlsx():
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(d)
    return send_file(data_export.export_dataframe(df), attachment_filename="testing.xlsx", as_attachment=True)


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload_file.html')
    if request.method == 'POST':
        file = request.files['file']
        df = data_export.import_bytes(file.read())
        flash(df.to_json())
        return redirect(url_for('upload_file'))


if __name__ == '__main__':
    app.run(debug=True)
