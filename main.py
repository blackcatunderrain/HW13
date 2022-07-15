import sqlite3


def get_data_from_db(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        return connection.execute(sql).fetchall()


def search_by_title(title):
    sql_query = f'''select * from netflix n where n.title like '#Roxy' order by n.release_year desc limit 1'''
    for item in get_data_from_db(sql_query):
        result = dict(item)

    return result

pd = search_by_title('Roxy')
print(pd)