import psycopg2
from settings.config import DB_NAME, DB_USER, DB_HOST, DB_PASSWORD

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASSWORD, host=DB_HOST)
cursor = conn.cursor()

cursor.execute('select * from users')

data = cursor.fetchall()

print(data)

cursor.close()
conn.close()