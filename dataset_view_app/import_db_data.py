import psycopg2

from settings.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


def load_sales_data():
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cursor = connection.cursor()
    cursor.execute('select * from sales_data order by ordernumber limit 10')
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return columns, data



