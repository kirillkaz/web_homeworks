import sqlite3

def create_db_by_dump(db_name: str, dump_name):
    con = sqlite3.connect(db_name)
    cursor = con.cursor()

    with open(dump_name, 'r') as file:
        sql_dumb = file.read()

    cursor.executescript(sql_dumb)

    con.close()