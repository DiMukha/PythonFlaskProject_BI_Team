import sqlite3
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


app = Flask(__name__)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    firstname = lastname = email = ''
    if request.method == "POST":
        pass
    return render_template('register.html', firstname=firstname, lastname=lastname, email=email)


@app.route('/list_users')
def list_users():
    return render_template('list_users.html')


@login_manager.user_loader
def load_user(user_id):
    # return User.get(user_id)
    pass


# https://flask-login.readthedocs.io/en/latest/
@app.route('/login', methods=["GET", "POST"])
def login():
    user = ''
    if request.method == "POST":
        pass
    return render_template('login.html', user=user)


@app.route('/update_user/', methods=['GET', 'POST'])
def update_user(id=1):
    db = sqlite3.connect('db.report_system')
    cursor =db.cursor()
    if request.method == 'GET':
        user_data = cursor.execute('select firstname, lastname, login, email, password from users where id = ?', (id,))
    else:
        user_data = ''
    return render_template('update_user.html', user_data=user_data.fetchall())


if __name__ == '__main__':
    app.run(debug=True)
