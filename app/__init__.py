from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import config

login_manager = LoginManager()

app = Flask(__name__)
app.config.from_object(config.Config)
Bootstrap(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'login'

from . import routes
from .auth import auth
from .users import users_list
from .sales_data import app_table_data_view