# Dependencies

import sqlalchemy
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect
from flask import Flask, jsonify

# First we will create an app
app = Flask(__name__)

# Let's create the engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Create a base
Base = automap_base()

# let us reflect the tables
Base.prepare(engine, reflect = True)

# Take a look at the classes
Base.classes.keys()

# References for the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

# /
@app.route("/")
def welcome():
    """List all available api routes."""
    return (

        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date><br/>"
        f"/api/v1.0/<start_date>/<end_date>"
    )

# /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
     
# Convert the Query Results to a Dictionary Using `date` as the Key and `prcp` as the Value    
def precipitation():
        # Create session
        session = Session(engine)
        # Bring the precipitation data from part 1
        precipitation_data = session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.date(2016, 8, 23)).all()
        
        # make the results into a dictionary
        precipitation_data_dict = dict(precipitation_data)
        
        # make the dictionary into json format
        return jsonify(precipitation_data_dict)

# /api/v1.0/stations
@app.route("/api/v1.0/stations")

def stations():
        # Create session
        session = Session(engine)

        # Return a JSON List of Stations From the Dataset
        stations = session.query(Station.station, Station.name).all()

        # convert list to json
        return jsonify(stations)

# /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
        # Create session
        session = Session(engine)
        
        # we are bringing the data for stations from part 1
        active_stations = (session.query(Measurement.station, func.count(Measurement.station))
                        .group_by(Measurement.station)
                        .order_by(func.count(Measurement.station).desc())
                        .all())

        
        most_active= 'USC00519281'
        
        # we are bringing the temperature data from part 1
        temp_observation = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active).\
    filter(func.strftime("%Y-%m-%d", Measurement.date) >= dt.date(2016, 8, 23)).all()
        
        temperature_list = list(np.ravel(temp_observation))


        # return list in json for temperature of previous year
        return jsonify(temperature_list)

# /api/v1.0/<start>
@app.route("/api/v1.0/<start>")
def temp_start(start):

        # Create session
        session = Session(engine)

        # session that gets a date with their registered minimum, average, and maximum temperatures filter by a starting date
        temp_start = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()

        # Convert to normal
        temp_start_list = list(np.ravel(temp_start))


        # Return list in json
        return jsonify(temp_start_list)

# Start-End Day Route. /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):

        # Create session
        session = Session(engine)

        # session that gets a date with their registered minimum, average, and maximum temperatures filter by a starting date, and enging date
        temp_start_end = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()

        # Convert to normal list
        temp_start_end_list = list(np.ravel(temp_start_end))


        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(temp_start_end_list)

# the behavior for main
if __name__ == '__main__':
    app.run(debug=True)
