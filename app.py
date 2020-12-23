from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import sqlite3


app = Flask(__name__)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/register', methods=["GET", "POST"])
# args: firstname, lastname, login, email, password
# if validation failed - we show 'message'
def register():
    firstname = lastname = email = password = ''
    if request.method == "POST":
        pass
    return render_template('register.html', firstname=firstname, lastname=lastname, email=email)




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




if __name__ == '__main__':
    app.run(debug=True)
