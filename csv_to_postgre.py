import psycopg2

from settings.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


def csv_to_postgre():
    db = None
    filename = 'example_data/sales_data.csv'
    ct_script = 'sales_data.sql'
    try:
        # connect to the PostgreSQL db
        db = psycopg2.connect(dbname=DB_NAME,
                              user=DB_USER,
                              password=DB_PASSWORD,
                              host=DB_HOST)
        cur = db.cursor()
        cur.execute("DROP TABLE IF EXISTS sales_data;")
        # create table from script
        with open(ct_script) as s:
            cur.execute(s.read())
            with open(filename, 'r') as f:
                next(f)
                cur.copy_from(f, 'sales_data', sep='\t')
                db.commit()
                db.close()
        f.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if db is not None:
            db.close()
            print('Database connection closed')
