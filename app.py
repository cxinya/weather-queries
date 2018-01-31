from datetime import datetime
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to classes
Stations = Base.classes.sta
Measurements = Base.classes.meas

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return ("All available routes")

#################################################

@app.route("/api/v1.0/precipitation")
def precip():
    
    # Query
    last12 = datetime.strptime("8/23/2016", "%m/%d/%Y")
    precip_query = (session.query(Measurements.date, Measurements.prcp)
        .filter(Measurements.date > last12))
        
    # Append values to dictionary
    precip_dict = {}
    for row in precip_query:
        date = row[0].strftime("%Y/%m/%d")
        precip_dict[date] = row[1]
    
    # Return json
    return jsonify(precip_dict)

#################################################

@app.route("/api/v1.0/stations")
def stations():

    #Query
    station_query = (session.query(Stations.station))
    
    # Append values to dictionary
    all_stations = []
    for row in station_query:
        all_stations.append(row[0])
    stations_dict = {"Stations": all_stations}
    
    # Return json
    return jsonify(stations_dict)

#################################################

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Query
    last12 = datetime.strptime("8/23/2016", "%m/%d/%Y")
    temp_query = (session.query(Measurements.date, Measurements.tobs)
                   .filter(Measurements.date > last12))
                   
    # Create dictionary
    temp_dict = {}
    for row in temp_query:
        date = row[0].strftime("%Y/%m/%d")
        temp_dict[date] = row[1]
        
    # Return json
    return jsonify(temp_dict)

#################################################

@app.route("/api/v1.0/<start>")
def start():
    
    # Start date from link
    start_date = datetime.strptime(start, "%Y-%m-%d")
    
    # Query
    temp_query = (session.query(Measurements.tobs)
    .filter(Measurements.date >= start_date))
    
    # Create dict
    temps = []
    for row in temp_query:
        temps.append(row[0])
    
    tmin = min(temps)
    tavg = round(sum(temps)/len(temps),1)
    tmax = max(temps)
    
    temp_dict = {"Minimum temperature": tmin,
                 "Average temperature": tavg,
                 "Maximum temperature": tmax}
    
    return jsonify(temp_dict)

################################################

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    
    # Start date from link
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    
    # Query
    temp_query = (session.query(Measurements.tobs)
    .filter(Measurements.date >= start_date &
            Measurements.date <= end_date))
    
    # Create dict
    temps = []
    for row in temp_query:
        temps.append(row[0])
    
    tmin = min(temps)
    tavg = round(sum(temps)/len(temps),1)
    tmax = max(temps)
    
    temp_dict = {"Minimum temperature": tmin,
                 "Average temperature": tavg,
                 "Maximum temperature": tmax}
    
    return jsonify(temp_dict)

################################################

if __name__ == '__main__':
    app.run()
