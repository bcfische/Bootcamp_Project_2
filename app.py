import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template


## Database ##

# Need to set 'check_same_thread' argument to avoid threading errors 
engine = create_engine("sqlite:///db/mcu.sqlite",connect_args={'check_same_thread': False})

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)
#print(Base.classes.keys())

# Save reference to the table
Movies = Base.classes.movies
Characters = Base.classes.characters

# Create our session (link) from Python to the DB
session = Session(engine)


## Flask ##

app = Flask(__name__)

## Index.html
@app.route("/")
def index():
    results = session.query(Movies).all()
    return render_template("index.html")

## Return JSON list of movie titles
@app.route("/movies")
def movies():
    results = session.query(Movies).all()
    data = []
    for result in results:
        d = {}
        d["movie_id"] = result.movie_id
        d["title"] = result.title
        d["release_date"] = result.release_date
        d["gross"] = result.gross
        data.append(d)
    return jsonify(data)

## Return JSON list of character names
@app.route("/characters")
def characters():
    results = session.query(Characters).all()
    data = []
    for result in results:
        d = {}
        d["name"] = result.name
        d["alias"] = result.alias
        d["movie_id"] = result.movie_id
        d["screen_time"] = result.screen_time
        data.append(d)
    return jsonify(data)

## Return title of movie given the movie_id
@app.route("/movies/<movie_id>")
def movies_id(movie_id):
    sel = [Movies.movie_id, Movies.title]
    results = session.query(*sel).filter(Movies.movie_id == movie_id).all()
    if len(results):
        return jsonify(results[0][1])
    else:
        return (f"No data")

## Return characters in movie given the movie_id
@app.route("/characters/<movie_id>")
def characters_id(movie_id):
    sel = [Characters.name, Characters.alias, Characters.movie_id, Characters.screen_time]
    results = session.query(*sel).filter(Characters.movie_id == movie_id).all()
    if len(results):
        data = []
        for result in results:
            d = {}
            d["name"] = result.name
            d["alias"] = result.alias
            d["screen_time"] = result.screen_time
            data.append(d)
        return jsonify(data)
    else:
        return (f"No data")

## Return sorted list of characters by total movie appearances
@app.route("/characters/sort_by_number")
def characters_sort_number():
    with engine.connect() as con:
        print("Executing <sort_number> sql query")
        rows = con.execute('select name, alias, count(name) from characters group by name')
        data = {}
        for row in rows:
            key = row[0]
            if row[1] is not None:
                key = row[1]
            value = row[2]
            if key in data.keys():
                data[key] = data[key] + value
            else:
                data[key] = value
        sort = sorted(data.items(), key=lambda x: x[1], reverse=True)
        return jsonify(sort)
        #data = []
        #for k,v in sort.items():
        #    d = {}
        #    d["character"] = k
        #    d["appearances"] = v
        #    data.append(d) 
        #return jsonify(data)

## Return sorted list of characters by total screen time
@app.route("/characters/sort_by_time")
def characters_sort_time():
    with engine.connect() as con:
        print("Executing <sort_time> sql query")
        rows = con.execute('select name, alias, sum(screen_time) from characters group by name')
        data = {}
        for row in rows:
            key = row[0]
            if row[1] is not None:
                key = row[1]
            value = row[2]
            if key in data.keys():
                data[key] = data[key] + value
            else:
                data[key] = value
        sort = sorted(data.items(), key=lambda x: x[1], reverse=True)
        return jsonify(sort)

## Return sorted list of characters by highest average gross
@app.route("/characters/sort_by_gross")
def characters_sort_time():
    with engine.connect() as con:
        print("Executing <sort_gross> sql query")
        rows = con.execute('select name, alias, sum(gross) from characters group by name')
        data = {}
        for row in rows:
            key = row[0]
            if row[1] is not None:
                key = row[1]
            value = row[2]
            if key in data.keys():
                data[key] = data[key] + value
            else:
                data[key] = value
        sort = sorted(data.items(), key=lambda x: x[1], reverse=True)
        return jsonify(sort)

## Return sorted list of movies by total gross
@app.route("/movies/sort_by_gross")
def characters_sort_time():
    with engine.connect() as con:
        print("Executing <sort_gross> sql query")
        rows = con.execute('select title, release_date, sum(gross) from movies group by title')
        data = {}
        for row in rows:
            key = row[0]
            if row[1] is not None:
                key = row[1]
            value = row[2]
            if key in data.keys():
                data[key] = data[key] + value
            else:
                data[key] = value
        sort = sorted(data.items(), key=lambda x: x[1], reverse=True)
        return jsonify(sort)

if __name__ == '__main__':
    app.run(debug=True)

