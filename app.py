import numpy as np
import sqlalchemy
import pandas as pd 
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Welcome to Your Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation_by_date():

    yr_prcp = session.query("date", "prcp").\
    filter(func.strftime(Measurement.date) >= "2016-08-23").\
    order_by(Measurement.date).all()
    
    prcp_by_date = []
    for date, prcp in yr_prcp:
        prcp_by_date_dict = {}
        prcp_by_date_dict["date"] = date
        prcp_by_date_dict["prcp"] = prcp
        prcp_by_date.append(prcp_by_date_dict)
        
    return jsonify(prcp_by_date)


@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(Measurement.station).group_by(Measurement.station).all()
    stations_list = list(np.ravel(stations))
    
    return jsonify(stations_list)
    
    
@app.route("/api/v1.0/tobs")
def tobs():
    
    yr_temps = session.query("date", "tobs").\
    filter(func.strftime(Measurement.date) >= "2016-08-23").\
    order_by(Measurement.date).all()

    temp_by_date = []
    for date, tobs in yr_temps:
        temp_by_date_dict = {}
        temp_by_date_dict["date"] = date
        temp_by_date_dict["tobs"] = tobs
        temp_by_date.append(temp_by_date_dict)
        
    return jsonify(temp_by_date)
    

@app.route("/api/v1.0/<start>")
def calc_temps_start(start):
    
    temp_stats = session.query(func.min(Measurement.tobs), 
                         func.avg(Measurement.tobs), 
                         func.max(Measurement.tobs)).\
                         filter(Measurement.date >= start).all()
    
    temps_list = list(np.ravel(temp_stats))

    key_names = ["Min_Temp", "Avg_Temp", "Max_Temp"]
    
    zipbObj = zip(key_names, temps_list)
 
    temp_dict = dict(zipbObj)
    
    return jsonify(temp_dict)
    
    
@app.route("/api/v1.0/<start>/<end>")
def calc_temps_start_end(start, end):
    
    temp_stats = session.query(func.min(Measurement.tobs), 
                         func.avg(Measurement.tobs), 
                         func.max(Measurement.tobs)).\
                         filter(Measurement.date >= start).\
                         filter(Measurement.date <= end).all()
    
    temps_list = list(np.ravel(temp_stats))

    key_names = ["Min_Temp", "Avg_Temp", "Max_Temp"]
    
    zipbObj = zip(key_names, temps_list)
 
    temp_dict = dict(zipbObj)
    
    return jsonify(temp_dict)

    
if __name__ == "__main__":
    app.run(debug=True)
