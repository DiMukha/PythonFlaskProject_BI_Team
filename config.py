import os
import pathlib

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')

    DB_NAME = os.getenv('DBNAME')
    DB_NAME_ORM = os.getenv('DBNAMEORM')
    DB_USER = os.getenv('DBUSER')
    DB_PASSWORD = os.getenv('PASSWORD')
    DB_HOST = os.getenv('HOST')

    DB_CONNECTION = {
        'dbname': DB_NAME,
        'user': DB_USER,
        'password': DB_PASSWORD,
        'host': DB_HOST
    }

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME_ORM}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ROWS_LIMIT = 10