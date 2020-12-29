import sqlite3
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap

from dataset_view_app.import_db_data import load_sales_data, load_statuses
from settings.config import SECRET_KEY

import auth
import db


app = Flask(__name__)
Bootstrap(app)
db.init_app(app)
app.register_blueprint(auth.bp)
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


@app.route('/data_view/', methods=['GET', 'POST'])
@app.route('/data_view/<int:page>', methods=['GET', 'POST'])
def data_view(page=0):
    filters = {}
    # default_filters = load_default_filters()
    default_statuses = load_statuses()
    # print(default_filters)
    print(default_statuses)
    if request.method == 'POST':
        print(request.form)
        if request.form.get('order_num'):
            filters['ORDERNUMBER'] = request.form.get('order_num')
        if request.form.get('order_status'):
            filters['STATUS'] = str(request.form.get('order_status'))
        if request.form.get('min_order_date'):
            filters['ORDERDATE_min'] = str(request.form.get('min_order_date'))
        if request.form.get('max_order_date'):
            filters['ORDERDATE_max'] = str(request.form.get('max_order_date'))
        if request.form.get('min_price'):
            filters['PRICEEACH_min'] = str(request.form.get('min_price'))
        if request.form.get('max_price'):
            filters['PRICEEACH_max'] = str(request.form.get('max_price'))

    columns, data = load_sales_data(filters)
    prev = page
    page_from = page
    next = prev + 1
    if page > 0:
        prev = page - 1
        next = prev + 2
        page_from = page * 10
    page_to = page_from + 10
    data = data[page_from:page_to]
    return render_template('data_view/table_data.html',
                           columns=columns,
                           data=data,
                           filters=filters,
                           statuses=default_statuses,
                           prev=prev,
                           next=next,
                           page_from=page_from,
                           page_to=page_to)





if __name__ == '__main__':
    app.run(debug=True)
