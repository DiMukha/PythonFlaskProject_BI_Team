import os
import psycopg2

from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

DB_NAME = os.getenv('DBNAME')
DB_USER = os.getenv('USER')
DB_PASSWORD = os.getenv('PASSWORD')
DB_HOST = os.getenv('HOST')