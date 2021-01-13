from flask import Flask
from flask_bootstrap import Bootstrap
import config


app = Flask(__name__)
app.config.from_object(config.Config)
Bootstrap(app)

from . import routes