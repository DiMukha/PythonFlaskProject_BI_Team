from flask import render_template, Blueprint, send_file, request, session, url_for
from xlsxwriter import Workbook

import auth
from dataset_view_app.import_db_data import load_sales_data, load_statuses

bp = Blueprint('table_data', __name__, url_prefix='/table_data')


@bp.route('/data_view', methods=['GET', 'POST'])
@auth.login_required
def data_view():
    filters = {parameter: value for parameter, value in request.args.items() if value}
    default_statuses = load_statuses()
    offset_page = int(filters.get('page', 0))
    columns, data = load_sales_data(filters, offset_page)

    base_url = f"{ url_for('table_data.data_view') }" \
           f"?order_num={filters.get('order_num', '')}" \
           f"&order_status={filters.get('order_status', '')}" \
           f"&min_order_date={filters.get('min_order_date', '')}" \
           f"&max_order_date={filters.get('max_order_date', '')}" \
           f"&min_price={filters.get('min_price', '')}" \
           f"&max_price={filters.get('max_price', '')}"

    prev = base_url + f"&page={offset_page}"
    if offset_page:
        prev = base_url + f"&page={offset_page-1}"
    next = base_url + f"&page={offset_page+1}"

    page_from = offset_page*10
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
