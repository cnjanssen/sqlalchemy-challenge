# 1. imports
import numpy as np

import sqlalchemy
from dateutil.parser import parse
import dateutil.relativedelta
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start><end><br/>"
    )


# Routes for precipitaiton
@app.route("/api/v1.0/precipitation")
def precipitaiton():
    session = Session(engine)
    #query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    #create dictionary form the row data and append to a list of all_precpipitation

    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict['prcp'] = prcp
        all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)

# Routes for stations
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    #query all stations
    results = session.query(Station.name).all()
    return jsonify(results)


 # Routes for tobs
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    #determine latest date entry
    str_newest_date = session.query(Measurement).order_by(desc(Measurement.date)).limit(1).all()[0].date
    date_oldest = parse(str_newest_date) - dateutil.relativedelta.relativedelta(years=1)
    str_oldest_date = str(date_oldest)[0:10]
    # Perform a query to retrieve the data and precipitation scores
    results_temp = session.query(Measurement.date, Measurement.tobs).order_by(desc(Measurement.date)).filter(Measurement.date.between(str_oldest_date, str_newest_date)).all()
    session.close()

    #create dictionary form the row data and append to a list of all_precpipitation

    all_tobs = []
    for date, tobs in results_temp:
        tobs_dict = {}
        tobs_dict['tobs'] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

  # Routes for by date
@app.route("/api/v1.0/<start>")
def start_only(start):
    session = Session(engine)
    #determine start date using provided date argument
    start_date = start
    #determine end date by returning the first result by ordering all dates, i.e. newest date in Measurement
    str_newest_date = session.query(Measurement).order_by(desc(Measurement.date)).limit(1).all()[0].date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date.between(start_date, str_newest_date)).all()
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    #determine start date using provided date argument
    start_date = start
    #determine end date by returning the first result by ordering all dates, i.e. newest date in Measurement
    end_date = end
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date.between(start_date, end_date)).all()
    return jsonify(results)



# 5. return jsonified output
@app.route("/jsonified")
def jsonified():
    return jsonify(hello_dict)



if __name__ == "__main__":
    app.run(debug=True)




