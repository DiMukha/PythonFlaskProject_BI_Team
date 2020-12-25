from flask import Flask, render_template
from flask_bootstrap import Bootstrap

import auth
import db

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
    return render_template('list_users.html')


if __name__ == '__main__':
    app.run(debug=True)
