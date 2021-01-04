from flask import render_template, Blueprint, send_file
from xlsxwriter import Workbook

import auth
from dataset_view_app.import_db_data import load_sales_data

bp = Blueprint('table_data', __name__, url_prefix='/table_data')


@bp.route('/data_view')
@bp.route('/data_view/<int:page>')
@auth.login_required
def data_view(page=0):
    columns, data = load_sales_data()
    prev = page
    page_from = page
    next = prev + 1
    if page > 0:
        prev = page - 1
        next = prev + 2
        page_from = page * 10
    page_to = page_from + 10
    data = data[page_from:page_to]
    return render_template('data_view/table_data.html',
                           columns=columns,
                           data=data,
                           prev=prev,
                           next=next,
                           page_from=page_from,
                           page_to=page_to)


@bp.route('/data_view/download', methods=['GET'])
@auth.login_required
def download():
    columns, data = load_sales_data()
    wb = Workbook('/dataset_view_app/xls_files/sales_data.xlsx')
    ws = wb.add_worksheet('SalesData')

    for col in range(len(columns)):
        ws.write(0, col, columns[col])
        print(col)
    for row in range(len(data)):
        for col in range(len(columns)):
            print(row)
            ws.write(row, col, data[row][col])
    wb.close()
    return send_file('/dataset_view_app/xls_files/sales_data.xlsx')
