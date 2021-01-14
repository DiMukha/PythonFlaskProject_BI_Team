from flask import render_template
from . import app

from .auth import auth
from .sales_data import app_table_data_view
from .users import users_list

app.register_blueprint(auth.bp)
app.register_blueprint(app_table_data_view.bp)
app.register_blueprint(users_list.bp)

@app.route('/')
def index():
    return render_template('index.html')

