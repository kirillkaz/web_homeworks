import sqlite3

def create_db(db_name: str):
    con = sqlite3.connect('library_db.db')
    cursor = con.cursor()

    with open('library.db', 'r') as file:
        sql_dumb = file.read()

    cursor.executescript(sql_dumb)

    con.close()