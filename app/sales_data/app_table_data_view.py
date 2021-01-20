from flask import render_template, request, url_for, redirect
from flask_login import login_required

from app import app, excel
from app.sales_data.import_db_data import load_sales_data, load_statuses


@app.route('/data_view', methods=['GET', 'POST'])
@login_required
def data_view():
    filters = {parameter: value for parameter, value in request.args.items() if value}
    default_statuses = load_statuses()
    offset_page = int(filters.get('page', 0))
    columns, data = load_sales_data(filters, offset_page)

    base_url = f"{url_for('data_view')}" \
               f"?order_num={filters.get('order_num', '')}" \
               f"&order_status={filters.get('order_status', '')}" \
               f"&min_order_date={filters.get('min_order_date', '')}" \
               f"&max_order_date={filters.get('max_order_date', '')}" \
               f"&min_price={filters.get('min_price', '')}" \
               f"&max_price={filters.get('max_price', '')}"

    prev = base_url + f"&page={offset_page}"
    if offset_page:
        prev = base_url + f"&page={offset_page - 1}"
    next = base_url + f"&page={offset_page + 1}"

    page_from = offset_page * app.config['ROWS_LIMIT']
    page_to = page_from + app.config['ROWS_LIMIT']

    excel_export = base_url + f"&mode=xls"

    if 'mode' in filters.keys():
        xlsx_data = []
        xlsx_data.append(columns)
        for item in data:
            xlsx_data.append(item)

        return excel.make_response_from_array(xlsx_data, "xlsx", file_name='Sales data')
    return render_template('sales_data/table_data.html',
                           columns=columns,
                           data=data,
                           filters=filters,
                           statuses=default_statuses,
                           prev=prev,
                           next=next,
                           page_from=page_from,
                           page_to=page_to,
                           excel=excel_export)
