import json
import sqlite3
from flask import Flask

app = Flask(__name__)


def get_data_from_db(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        return connection.execute(sql).fetchall()


def search_by_title(title):
    sql_query = f'''select n.title, n.country, n.release_year, n.description 
    from netflix n 
    where n.title like '%{title}%' 
    order by n.release_year desc limit 1
    '''
    for item in get_data_from_db(sql_query):
        result = dict(item)

    return result


@app.get('/movie/<title>')
def search_by_title_view(title):
    result = search_by_title(title)
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


@app.get('/movie/<year1>/to/<year2>')
def search_by_year_view(year1, year2):
    sql_query = f'''select n.title, n.release_year 
    from netflix n 
    where n.release_year between '{year1}' and '{year2}' limit 100
      '''
    result = []

    for item in get_data_from_db(sql_query):
        result.append(dict(item))

    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


app.run()
