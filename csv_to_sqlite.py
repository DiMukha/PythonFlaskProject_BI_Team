import sqlite3
import csv


def csv_to_sqlite():
    db = None
    filename = 'example_data/sales_data.csv'
    ct_script = 'sales_data.sql'
    try:
        db = sqlite3.connect('db.report_system')
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS sales_data;")
        cnt = 0
        with open(filename, 'r') as csv_f:
            reader = csv.reader(csv_f, delimiter='\t')
            for row in reader:
                row = ['NULL' if val == '' else val for val in row]
                row = [x.replace("'", "''") for x in row]
                out = "'" + "', '".join(str(item) for item in row) + "'"
                out = out.replace("'NULL'", 'NULL')
                with open(ct_script) as f:
                    cursor.execute(f.read())
                    query = "INSERT INTO sales_data VALUES (" + out + ")"
                    cursor.execute(query)
                    cnt = cnt + 1
                    if cnt % 10000 == 0:
                        db.commit()
            # Commit Changes
            db.commit()
        print("Uploaded " + str(cnt) + " rows into table sales_data")
        # Close connection
        db.close()
    except (Exception, db.DatabaseError) as error:
        print(error)
    finally:
        if db is not None:
            db.close()
            print('Database connection closed')
