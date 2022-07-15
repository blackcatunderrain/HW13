import sqlite3


def get_data_from_db(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        return connection.execute(sql).fetchall()



