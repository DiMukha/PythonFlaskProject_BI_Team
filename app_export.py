from flask import render_template, request, url_for, redirect, send_file, flash, Blueprint
import data_export
import pandas as pd
from sqlalchemy import create_engine


bp = Blueprint('data_export', __name__, url_prefix='/data_export')


@bp.route('/send_xlsx')
def send_xlsx():
    d = {'col1': [1, 2], 'col2': [3, 4]}
    df = pd.DataFrame(d)
    return send_file(data_export.export_dataframe(df), attachment_filename="testing.xlsx", as_attachment=True)


# TODO not secure method ?
@bp.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        df = data_export.import_bytes(file.read())
        sqlite_engine = create_engine('sqlite:///db.report_system')
        df.to_sql(name=file.filename, con=sqlite_engine, schema=None, if_exists='fail', index=True, index_label=None,
                  chunksize=None, dtype=None, method="multi")
        flash(df.head(5).to_json())
        return redirect(url_for('upload_file'))
    return render_template('upload_file.html')
