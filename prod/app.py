import pandas as pd
import numpy as np

from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, render_template

## Database ##

# Need to set 'check_same_thread' argument to avoid threading errors 
engine = create_engine("sqlite:///db/mcu.sqlite",connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
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
    return render_template("index.html",movies=results)

## Return JSON list of movie titles
@app.route("/movies")
def movies():
    results = session.query(Movies.title).all()
    movie_names = list(np.ravel(results))
    return jsonify(movie_names)

## Return JSON list of character names
@app.route("/characters")
def characters():
    results = session.query(Characters.name).all()
    char_names = list(np.ravel(results))
    return jsonify(char_names)

## Return title of movie given the movie_id
@app.route("/movies/<movie_id>")
def movies_id(movie_id):
    sel = [Movies.movie_id, Movies.title]
    results = session.query(*sel).filter(Movies.movie_id == movie_id).all()
    if len(results):
        return jsonify(results[0][1])
    else:
        return (f"Index out of range")

## Return characters in movie given the movie_id
@app.route("/characters/<movie_id>")
def characters_id(movie_id):
    sel = [Characters.name, Characters.movie_id, Characters.screen_time]
    results = session.query(*sel).filter(Characters.movie_id == movie_id).all()
    if len(results):
        names = []
        for result in results:
            d = {}
            d["name"] = result.name
            d["screen_time"] = result.screen_time
            names.append(d)
        return jsonify(names)
    else:
        return (f"Index out of range")

'''
@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Query for the dates and precipitation observations """
    """ Convert the results to a dictionary and return the JSON representation """
    results = session.query(Measurement).all()
    all_measurements = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["date"] = measurement.date
        measurement_dict["prcp"] = measurement.prcp
        all_measurements.append(measurement_dict)
    return jsonify(all_measurements)

@app.route("/api/v1.0/tobs")
def tobs():
    """ Query for the dates and temperature observations from a year from the last data point """
    """ Return a JSON list of that query """
    q = session.query(Measurement.date)
    last = q.order_by(Measurement.date.desc()).first()
    lastday = datetime.strptime(last[0],'%Y-%m-%d').date()
    startday = lastday.replace(lastday.year-1)
    results = session.query(Measurement).filter(Measurement.date>=startday).all()
    temps = []
    for result in results:
        t_dict = {}
        t_dict["date"] = result.date
        t_dict["tobs"] = result.tobs
        temps.append(t_dict)
    return jsonify(temps)

@app.route("/api/v1.0/<start_date>")
def tobs_start(start_date):
    startday = datetime.strptime(start_date,'%Y-%m-%d').date()
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date>=startday).all()
    t_stats = list(np.ravel(results))
    return jsonify(t_stats)
'''

if __name__ == '__main__':
    app.run(debug=True)