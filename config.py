import os
import pathlib

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = pathlib.Path(__file__).parent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')

    DB_NAME = os.getenv('DBNAME')
    DB_USER = os.getenv('USER')
    DB_PASSWORD = os.getenv('PASSWORD')
    DB_HOST = os.getenv('HOST')

    DB_CONNECTION = {
        'dbname': DB_NAME,
        'user': DB_USER,
        'password': DB_PASSWORD,
        'host': DB_HOST
    }

    ROWS_LIMIT = 10