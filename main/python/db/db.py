from flask import g
from flask import current_app
from flask_mysqldb import MySQL


def get_db():
    if 'db' not in g:
        g.db = MySQL(current_app).connection
    return g.db


def query(stmt, args=''):
    try:
        with current_app.app_context():
            mysql_conn = get_db()
            cursor = mysql_conn.cursor()
            cursor.execute(stmt, args)
            mysql_conn.commit()
            data = cursor.fetchall()
    except Exception as e:
        if str(e) == "(2006, '')":
            ""
        else:
            raise e
    return data
