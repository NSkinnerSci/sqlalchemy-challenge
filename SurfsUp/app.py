from flask import Flask
from flask import Flask, jsonify

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#Setup sqlalchemy
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station


#############################################################

# Flask Setup
app = Flask(__name__)

@app.route("/")
def home():
    app_routes = ['/api/v1.0/precipitation', "/api/v1.0/stations", "/api/v1.0/tobs", "/api/v1.0/<start>", "/api/v1.0/<start>/<end>"]
    # return([print(f'{r} \n') for r in app_routes])
    return(app_routes)

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    # Starting from the most recent data point in the database. 
    date1 = datetime.strptime(session.query(measurement.date).order_by(measurement.date.desc()).first()[0], '%Y-%m-%d')
    # Calculate the date one year from the last date in data set.
    date2 = date1 - timedelta(days=365)
    
    # Perform a query to retrieve the data and precipitation scores
    query = session.query(measurement.date, measurement.prcp).filter(measurement.date >= date2.strftime("%Y-%m-%d"), measurement.date <= date1.strftime("%Y-%m-%d"))
    
    df = pd.read_sql(query.statement, engine)
    
    # Sort the dataframe by date
    df.sort_values(by = 'date', ascending = True, inplace=True)
    
    #convert to dictionary
    result = df.to_dict()
    
    return(jsonify(result))
    
    

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
        
    # Get names from sql and turn them into list
    station_names= list(np.ravel(session.query(station.name).all()))
    
    session.close()

    return(jsonify(station_names))
    

    
    
    
    

# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    # Starting from the most recent data point in the database. 
    date1 = datetime.strptime(session.query(measurement.date).order_by(measurement.date.desc()).first()[0], '%Y-%m-%d')
    # Calculate the date one year from the last date in data set.
    date2 = date1 - timedelta(days=365)
    
    #query for all tobs in the past year
    query_tobs = session.query(measurement.tobs).filter(measurement.date >= date2.strftime("%Y-%m-%d"), measurement.date <= date1.strftime("%Y-%m-%d")).all()

    #convert to df
    result = list(np.ravel(query_tobs))
    
    session.close()
    
    return(jsonify(result))
                                                        
    
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start range.
@app.route("/api/v1.0/<start>")
def get_start(start='nowhere'):
    session = Session(engine)
    
    #get the latest date for end
    end = datetime.strptime(session.query(measurement.date).order_by(measurement.date.desc()).first()[0], '%Y-%m-%d')

    #Query for each stat
    tob_min = session.query(func.min(measurement.tobs)).filter(measurement.date >= start, measurement.date <= end).all()[0][0]
    tob_max = session.query(func.max(measurement.tobs)).filter(measurement.date >= start, measurement.date <= end).all()[0][0]
    tob_avg = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start, measurement.date <= end).all()[0][0]
    
    #turn results into dictionary
    tob_dict = {'min_temp':tob_min, 'max_temp':tob_max, 'avg_temp':tob_avg}
    
    session.close()
    
    return(jsonify(tob_dict))
    

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
@app.route("/api/v1.0/<start>/<end>")
def get_end(start='nowhere', end='nowhere'):
    session = Session(engine)
    
    #Query for each stat
    tob_min = session.query(func.min(measurement.tobs)).filter(measurement.date >= start, measurement.date <= end).all()[0][0]
    tob_max = session.query(func.max(measurement.tobs)).filter(measurement.date >= start, measurement.date <= end).all()[0][0]
    tob_avg = session.query(func.avg(measurement.tobs)).filter(measurement.date >= start, measurement.date <= end).all()[0][0]
    
    #turn results into dictionary
    tob_dict = {'min_temp':tob_min, 'max_temp':tob_max, 'avg_temp':tob_avg}
    
    session.close()
    
    return(jsonify(tob_dict))



if __name__ == "__main__":
    app.run(debug=True)
