from io import BytesIO
import pandas as pd


def export_dataframe(dataframe: pd.DataFrame) -> BytesIO:
    """
    to send this data as file
    Flask.send_file(output, attachment_filename="testing.xlsx", as_attachment=True)
    """

    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    dataframe.to_excel(writer, sheet_name='Sheet1', header=True, index=False)
    writer.close()
    output.seek(0)
    return output


def import_bytes(data: BytesIO) -> pd.DataFrame:
    reader = pd.read_excel(data)
    df = pd.DataFrame(reader)
    return df
