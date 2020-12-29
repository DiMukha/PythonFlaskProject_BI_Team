from flask import render_template, Blueprint

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
