from flask import Flask, render_template, url_for, flash, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta
import sys
import os

app = Flask(__name__)
app.secret_key = "cpc"
WIN = sys.platform.startswith('win')
if WIN:  #three slash for Windows system
    prefix = 'sqlite:///'
else:   #four slash otherwise
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + 'train_data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)


class Train_data(db.Model):
    _train_id = db.Column("train_id", db.Integer, primary_key=True) # ________, we design that train id has totally 8 digits, the first 3 numbers represent train's line, and the last 5 numbers represent train's id in that line.
    train_type = db.Column("train_type", db.String(100)) # Local, Rapid, Special Rapid
    #direction = db.Column("direction", db.Boolean) # 0 means from the first station (0km) to final destination(xxkm), 1 means from final destination (xxkm) to the first station (0km)
    station = db.Column("station", db.String(100)) # station name that certain train stops by.
    arrival_time = db.Column("arrival_time", db.Time)  # record train's arrival time from certain station.
    departure_time = db.Column("departure_time", db.Time) # record train's departure time from certain station.
    dwell_time = db.Column("dwell_time", db.Integer) # train's dwell time at this station
    distance = db.Column("distance", db.Integer) # the distance from this station to the first station.
    #total_line_length = db.Column("total_distance", db.Integer) # total length of this line
    final_destination = db.Column("final_distination", db.String(100)) # train's final destination.
    transfer_station = db.Column("transfer_station", db.Boolean) # 1 menas this station can transfer to other line, 0 otherwise.

    # def __init__(self, ):
    #     self.name = name
    #     self.email = email




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)





