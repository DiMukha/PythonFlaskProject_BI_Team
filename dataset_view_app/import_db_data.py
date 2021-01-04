import psycopg2

from settings.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


def load_sales_data(filters, offset_page):
    sql = 'select * from sales_data where  '
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cursor = connection.cursor()
    if len(filters) > 0:

        if 'ORDERNUMBER' in filters.keys():
            sql += ' ORDERNUMBER = '
            sql += filters['ORDERNUMBER']
            sql += ' AND '
        if 'STATUS' in filters.keys():
            sql += ' STATUS = \''
            sql += filters['STATUS']
            sql += '\' AND'
        if 'ORDERDATE_min' in filters.keys():
            sql += ' CAST(ORDERDATE as date) >= \''
            sql += filters['ORDERDATE_min']
            sql += '\' AND'
        if 'ORDERDATE_max' in filters.keys():
            sql += ' CAST(ORDERDATE as date) <= \''
            sql += filters['ORDERDATE_max']
            sql += '\' AND'
        if 'PRICEEACH_min' in filters.keys():
            sql += ' PRICEEACH >= '
            sql += filters['PRICEEACH_min']
            sql += ' AND'
        if 'PRICEEACH_max' in filters.keys():
            sql += ' PRICEEACH <= '
            sql += filters['PRICEEACH_max']
            sql += ' AND'

    sql += f" 1=1 order by ordernumber, orderlinenumber limit {10} offset {offset_page*10}"
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return columns, data


def load_statuses():
    sql = 'select DISTINCT(STATUS) from sales_data  '
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cursor = connection.cursor()
    cursor.execute(sql)
    row_data = cursor.fetchall()
    statuses_list = [item[0] for item in row_data]
    cursor.close()
    connection.close()
    print(statuses_list)
    return statuses_list
