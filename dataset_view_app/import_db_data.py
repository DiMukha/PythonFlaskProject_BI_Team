from settings.config import connection

def load_sales_data():
    cursor = connection.cursor()
    cursor.execute('select * from sales_data limit 10')
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    return columns, data



