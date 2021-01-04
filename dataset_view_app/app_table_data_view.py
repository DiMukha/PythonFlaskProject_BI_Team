from flask import render_template, Blueprint, send_file, request
from xlsxwriter import Workbook

import auth
from dataset_view_app.import_db_data import load_sales_data, load_statuses

bp = Blueprint('table_data', __name__, url_prefix='/table_data')


@bp.route('/data_view', methods=['GET', 'POST'])
@bp.route('/data_view/<int:page>', methods=['GET', 'POST'])
@auth.login_required
def data_view(page=0):
    filters = {}
    default_statuses = load_statuses()
    if request.form.get('order_num'):
        filters['ORDERNUMBER'] = request.form.get('order_num')
    if request.form.get('order_status'):
        filters['STATUS'] = str(request.form.get('order_status'))
    if request.form.get('min_order_date'):
        filters['ORDERDATE_min'] = str(request.form.get('min_order_date'))
    if request.form.get('max_order_date'):
        filters['ORDERDATE_max'] = str(request.form.get('max_order_date'))
    if request.form.get('min_price'):
        filters['PRICEEACH_min'] = str(request.form.get('min_price'))
    if request.form.get('max_price'):
        filters['PRICEEACH_max'] = str(request.form.get('max_price'))
    offset_page = page
    columns, data = load_sales_data(filters, offset_page)
    prev = page
    page_from = page
    next = prev + 1
    if page:
        prev = page - 1
        next = prev + 2
        page_from = page * 10
    page_to = page_from + 10
    return render_template('data_view/table_data.html',
                           columns=columns,
                           data=data,
                           filters=filters,
                           statuses=default_statuses,
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
    for row in range(len(data)):
        for col in range(len(columns)):
            ws.write(row, col, data[row][col])
    wb.close()
    return send_file('/dataset_view_app/xls_files/sales_data.xlsx')
