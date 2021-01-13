import psycopg2

from app import app


def load_sales_data(filters, offset_page):
    sql = 'select * from sales_data where  '
    connection = psycopg2.connect(**app.config['DB_CONNECTION'])
    cursor = connection.cursor()
    if len(filters) > 0:

        if 'order_num' in filters.keys():
            sql += ' ORDERNUMBER = '
            sql += filters['order_num']
            sql += ' AND '
        if 'order_status' in filters.keys():
            sql += ' STATUS = \''
            sql += filters['order_status']
            sql += '\' AND'
        if 'min_order_date' in filters.keys():
            sql += ' CAST(ORDERDATE as date) >= \''
            sql += filters['min_order_date']
            sql += '\' AND'
        if 'max_order_date' in filters.keys():
            sql += ' CAST(ORDERDATE as date) <= \''
            sql += filters['max_order_date']
            sql += '\' AND'
        if 'min_price' in filters.keys():
            sql += ' PRICEEACH >= '
            sql += filters['min_price']
            sql += ' AND'
        if 'max_price' in filters.keys():
            sql += ' PRICEEACH <= '
            sql += filters['max_price']
            sql += ' AND'

    sql += f" 1=1 order by ordernumber, orderlinenumber limit {app.config['ROWS_LIMIT']} " \
           f"offset {offset_page*app.config['ROWS_LIMIT']}"
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return columns, data


def load_statuses():
    sql = 'select DISTINCT(STATUS) from sales_data'
    connection = psycopg2.connect(**app.config['DB_CONNECTION'])
    cursor = connection.cursor()
    cursor.execute(sql)
    row_data = cursor.fetchall()
    statuses_list = [item[0] for item in row_data]
    cursor.close()
    connection.close()
    return statuses_list
