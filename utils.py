import sqlite3


def get_data_from_db(sql) -> list:
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        return connection.execute(sql).fetchall()


def search_double_play(name1, name2) -> list[str]:
    sql_query = f'''select n.cast
        from netflix n
        where n.cast like '%{name1}%' and n.cast like '%{name2}%'
            '''
    result = []
    data = get_data_from_db(sql_query)
    names_d = {}
    for item in data:
        names = set(dict(item).get('cast').split(",")) - set([name1, name2])
        for name in names:
            names_d[str(name).strip()] = names_d.get(str(name).strip(), 0) + 1

    for k, v in names_d.items():
        if v >= 2:
            result.append(k)
    return result


def search_film_by(_type, year, genre):
    sql_query = f'''select n.title, n.description 
    from netflix n 
    where n.type = '{_type}' and n.release_year = '{year}' and n.listed_in like '%{genre}%'
    '''
    result = []
    for item in get_data_from_db(sql_query):
        result.append(dict(item))
    return result

