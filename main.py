import json
from flask import Flask
from utils import get_data_from_db

app = Flask(__name__)


@app.get('/movie/<title>/')
def search_by_title_view(title):
    sql_query = f'''select n.title, n.country, n.release_year, n.description 
        from netflix n 
        where n.title like '%{title}%' 
        order by n.release_year desc limit 1
        '''

    for item in get_data_from_db(sql_query):
        result = dict(item)

    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


@app.get('/movie/<year1>/to/<year2>/')
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


@app.get('/rating/<rating>/')
def search_by_rating_view(rating):
    ratings = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    sql_query = f'''select n.title, n.rating, n.description from netflix n where n.rating in {ratings.get(rating, ("G", "G"))}'''

    result = []
    for item in get_data_from_db(sql_query):
        result.append(dict(item))

    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


@app.get('/genre/<genre>/')
def search_by_genre_view(genre):
    sql_query = f'''select n.title, n.description
        from netflix n
        where n.listed_in like '%{genre}%' 
        order by n.release_year desc limit 10
        '''

    for item in get_data_from_db(sql_query):
        result = dict(item)

    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=4),
        status=200,
        mimetype="application/json"
    )


def search_double_play(name1, name2):
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


print(search_double_play('Rose McIver', 'Ben Lamb'))
# app.run()
