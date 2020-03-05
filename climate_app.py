import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///C:/GWDataAnalytics/GWHomework/sqlalchemy-challenge/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Stations = Base.classes.station

climate_app = Flask(__name__)

### Routes

@climate_app.route("/")

def welcome():
  return (
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/temperature-observations<br/>"
    f"/api/v1.0/start/<start><br/>"
    f"/api/v1.0/start/end/<start>/<end><br/>")
  

@climate_app.route("/api/v1.0/precipitation")
def precipitation():
  session = Session(engine)
  precip = session.query(Measurement.date, Measurement.prcp).all()
  session.close()
  return jsonify(precip)
  
  #Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
  #Return the JSON representation of your dictionary.

@climate_app.route("/api/v1.0/stations")
def stations():
  session = Session(engine)
  station_query = session.query(Stations.station).group_by(Stations.station).all()
  session.close
  station_list = list(np.ravel(station_query))
  return jsonify(station_list)
  
  #Return a JSON list of stations from the dataset.

@climate_app.route("/api/v1.0/temperature-observations")
def tobs():
  session = Session(engine)
  tobs_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>'2016-08-23').all()
  session.close
  tobs_list = list(np.ravel(tobs_query))
  return jsonify(tobs_list)


  #query for the dates and temperature observations from a year from the last data point.
  #Return a JSON list of Temperature Observations (tobs) for the previous year.

@climate_app.route(f"/api/v1.0/start/<start>")
def start_date(start):
  session = Session(engine)
  start_date_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).group_by(Measurement.date).filter(Measurement.date>start).all()
  session.close()
  start_date_list = list(np.ravel(start_date_query))
  return jsonify(start_date_list)



@climate_app.route(f"/api/v1.0/start/end/<start>/<end>")
def start_end_date(start, end):
  session = Session(engine)
  start_end_query = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).group_by(Measurement.date).filter(Measurement.date>start).filter(Measurement.date < end).all()
  session.close()
  start_end_list = list(np.ravel(start_end_query))
  return jsonify(start_end_list)
  #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
  #When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
  #When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

if __name__ == '__main__':
    climate_app.run(debug=True)