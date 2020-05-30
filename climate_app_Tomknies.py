from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

base = automap_base()
base.prepare(engine, reflect=True)

Measurement = base.classes.measurement
Station = base.classes.station

app = Flask(__name__)

@app.route("/")
def index():
    print("Use the App to see the routes:")
    return (        
        "Routes are below </br>"
        "---------------------------------</br>"
        
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/YYYY-MM-DD<start></br>"
        f"/api/v1.0/YYYY-MM-DD<start>/YYYY-MM-DD<end></br>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    response = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    ListPrecipitation = []

    for date, prcp in response:
        DictionaryPrcp = {}
        DictionaryPrcp['Date']=date
        DictionaryPrcp['Prcp']=prcp
        ListPrecipitation.append(DictionaryPrcp)

    return jsonify(ListPrecipitation)


@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    response = session.query(Station.station).all()
    session.close()

    ListStation = list(np.ravel(response))

    return jsonify(ListStation)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    response = session.query(Measurement.tobs, Measurement.date)\
    .filter(Measurement.station == 'USC00519281').\
    order_by(Measurement.date.desc()).limit(357).all()
    session.close()

    ListTobs = []

    for date, tobs in response:
        DictionaryTobs = {}
        DictionaryTobs['Date']=date
        DictionaryTobs['Tobs']=tobs
        ListTobs.append(DictionaryTobs)

    return jsonify(ListTobs)


@app.route("/api/v1.0/<start>")
def start(start):

    session = Session(engine)
    
    def temp(function, start):
        response = session.query(Measurement, function(Measurement.tobs))\
        .filter(Measurement.date == start)
        return response[0][1]

    Tmin = temp(func.min, start)
    Tmax = temp(func.max, start)
    Tavg = temp(func.avg, start)

    DictionaryStart = {}
    DictionaryStart['TMIN']=Tmin
    DictionaryStart['TMAX']=Tmax
    DictionaryStart['TAVG']=Tavg

    return jsonify(DictionaryStart)


@app.route("/api/v1.0/<start>/<end>")
def stuff(start, end):

    session = Session(engine)
    
    def temp(function, start, end):
        response = session.query(Measurement, function(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date <= end)
        return response[0][1]

    Tmin = temp(func.min, start, end)
    Tmax = temp(func.max, start, end)
    Tavg = temp(func.avg, start, end)

    DictionarySpan = {}
    DictionarySpan['TMIN']=Tmin
    DictionarySpan['TMAX']=Tmax
    DictionarySpan['TAVG']=Tavg

    return jsonify(DictionarySpan)



if __name__ == "__main__":
    app.run(debug=True)