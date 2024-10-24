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

class Line_data(db.Model):
    line = db.Column("line", db.String(100), primary_key=True) # Line's name, such as red line, blue line
    station = db.Column("Station", db.String(100), primary_key=True) # station that this line will dwell
    distance = db.Column("distance", db.Integer) # station's corresponding distance from the 0km first station.
    station_type = db.Column("station_type", db.Integer) # describe station type. if local train stops at this station, +1, otherwise +0; if rapid train stops at this station, +10, otherwise + 0;
    transfer = db.Column("transfer", db.Integer)

class Red_Line_Outbound_data(db.Model):
    train_id = db.Column("train_id", db.String(100), primary_key=True) # ________, we design that train id has totally 8 digits, the first 3 numbers represent train's line, and the last 5 numbers represent train's id in that line. 100 for red line
    station = db.Column("station", db.String(100), primary_key=True) # station name that certain train stops by.
    train_type = db.Column("train_type", db.String(100)) # Local, Rapid, Special Rapid
    arrival_time = db.Column("arrival_time", db.Time, nullable=True)  # record train's arrival time from certain station.
    departure_time = db.Column("departure_time", db.Time, nullable=True) # record train's departure time from certain station.
    transfer_station = db.Column("transfer_station", db.Boolean) # 1 menas this station can transfer to other line, 0 otherwise.

class Red_Line_Inbound_data(db.Model):
    train_id = db.Column("train_id", db.String(100),
                         primary_key=True)  # ________, we design that train id has totally 8 digits, the first 3 numbers represent train's line, and the last 5 numbers represent train's id in that line. 100 for red line
    station = db.Column("station", db.String(100), primary_key=True)  # station name that certain train stops by.
    train_type = db.Column("train_type", db.String(100))  # Local, Rapid, Special Rapid
    arrival_time = db.Column("arrival_time", db.Time,
                             nullable=True)  # record train's arrival time from certain station.
    departure_time = db.Column("departure_time", db.Time,
                               nullable=True)  # record train's departure time from certain station.
    transfer_station = db.Column("transfer_station",
                                 db.Boolean)  # 1 menas this station can transfer to other line, 0 otherwise.
    #dwell_time = db.Column("dwell_time", db.Integer, nullable=True) # train's dwell time at this station
    #final_destination = db.Column("final_distination", db.String(100)) # train's final destination.
    #line = db.Column("line", db.String(100)) # Line of this train (e.g. Route A, Route B ...)
    #direction = db.Column("direction", db.Boolean) # 0 means from the first station (0km) to final destination(xxkm), 1 means from final destination (xxkm) to the first station (0km)
    # distance = db.Column("distance", db.Integer) # the distance from this station to the first station.
    # total_line_length = db.Column("total_distance", db.Integer) # total length of this line

class Green_Line_Outbound_data(db.Model):
    train_id = db.Column("train_id", db.Integer, primary_key=True) # ________, we design that train id has totally 8 digits, the first 3 numbers represent train's line, and the last 5 numbers represent train's id in that line. 200 for green line
    train_type = db.Column("train_type", db.String(100)) # Local, Rapid, Special Rapid
    station = db.Column("station", db.String(100), primary_key=True) # station name that certain train stops by.
    arrival_time = db.Column("arrival_time", db.Time, nullable=True)  # record train's arrival time from certain station.
    departure_time = db.Column("departure_time", db.Time, nullable=True) # record train's departure time from certain station.
    transfer_station = db.Column("transfer_station", db.Boolean) # 1 menas this station can transfer to other line, 0 otherwise.

class Green_Line_Inbound_data(db.Model):
    train_id = db.Column("train_id", db.Integer,
                         primary_key=True)  # ________, we design that train id has totally 8 digits, the first 3 numbers represent train's line, and the last 5 numbers represent train's id in that line. 200 for green line
    train_type = db.Column("train_type", db.String(100))  # Local, Rapid, Special Rapid
    station = db.Column("station", db.String(100), primary_key=True)  # station name that certain train stops by.
    arrival_time = db.Column("arrival_time", db.Time,
                             nullable=True)  # record train's arrival time from certain station.
    departure_time = db.Column("departure_time", db.Time,
                               nullable=True)  # record train's departure time from certain station.
    transfer_station = db.Column("transfer_station",
                                 db.Boolean)  # 1 menas this station can transfer to other line, 0 otherwise.

    #dwell_time = db.Column("dwell_time", db.Integer, nullable=True) # train's dwell time at this station
    #final_destination = db.Column("final_distination", db.String(100)) # train's final destination.
    #line = db.Column("line", db.String(100)) # Line of this train (e.g. Route A, Route B ...)
    #direction = db.Column("direction", db.Boolean) # 0 means from the first station (0km) to final destination(xxkm), 1 means from final destination (xxkm) to the first station (0km)
    # distance = db.Column("distance", db.Integer) # the distance from this station to the first station.
    # total_line_length = db.Column("total_distance", db.Integer) # total length of this line

class Orange_Line_Outbound_data(db.Model):
    train_id = db.Column("train_id", db.Integer,primary_key=True)  # ________, we design that train id has totally 8 digits, the first 3 numbers represent train's line, and the last 5 numbers represent train's id in that line. 300 for orange line
    train_type = db.Column("train_type", db.String(100))  # Local, Rapid, Special Rapid
    station = db.Column("station", db.String(100), primary_key=True)  # station name that certain train stops by.
    arrival_time = db.Column("arrival_time", db.Time, nullable=True)  # record train's arrival time from certain station.
    departure_time = db.Column("departure_time", db.Time, nullable=True)  # record train's departure time from certain station.
    transfer_station = db.Column("transfer_station",db.Boolean)  # 1 menas this station can transfer to other line, 0 otherwise.

class Orange_Line_Inbound_data(db.Model):
    train_id = db.Column("train_id", db.Integer,
                         primary_key=True)  # ________, we design that train id has totally 8 digits, the first 3 numbers represent train's line, and the last 5 numbers represent train's id in that line. 300 for orange line
    train_type = db.Column("train_type", db.String(100))  # Local, Rapid, Special Rapid
    station = db.Column("station", db.String(100), primary_key=True)  # station name that certain train stops by.
    arrival_time = db.Column("arrival_time", db.Time,
                             nullable=True)  # record train's arrival time from certain station.
    departure_time = db.Column("departure_time", db.Time,
                               nullable=True)  # record train's departure time from certain station.
    transfer_station = db.Column("transfer_station",
                                 db.Boolean)  # 1 menas this station can transfer to other line, 0 otherwise.

    #dwell_time = db.Column("dwell_time", db.Integer, nullable=True)  # train's dwell time at this station
    #final_destination = db.Column("final_distination", db.String(100))  # train's final destination.
    # line = db.Column("line", db.String(100)) # Line of this train (e.g. Route A, Route B ...)
    # direction = db.Column("direction", db.Boolean) # 0 means from the first station (0km) to final destination(xxkm), 1 means from final destination (xxkm) to the first station (0km)
    # distance = db.Column("distance", db.Integer) # the distance from this station to the first station.
    # total_line_length = db.Column("total_distance", db.Integer) # total length of this line

class Black_Line_Outbound_data(db.Model):
    train_id = db.Column("train_id", db.Integer,primary_key=True)  # ________, we design that train id has totally 8 digits, the first 3 numbers represent train's line, and the last 5 numbers represent train's id in that line. 400 for black line
    train_type = db.Column("train_type", db.String(100))  # Local, Rapid, Special Rapid
    station = db.Column("station", db.String(100), primary_key=True)  # station name that certain train stops by.
    arrival_time = db.Column("arrival_time", db.Time, nullable=True)  # record train's arrival time from certain station.
    departure_time = db.Column("departure_time", db.Time, nullable=True)  # record train's departure time from certain station.
    transfer_station = db.Column("transfer_station",
                                 db.Boolean)  # 1 menas this station can transfer to other line, 0 otherwise.

class Black_Line_Inbound_data(db.Model):
    train_id = db.Column("train_id", db.Integer,
                         primary_key=True)  # ________, we design that train id has totally 8 digits, the first 3 numbers represent train's line, and the last 5 numbers represent train's id in that line. 400 for black line
    train_type = db.Column("train_type", db.String(100))  # Local, Rapid, Special Rapid
    station = db.Column("station", db.String(100), primary_key=True)  # station name that certain train stops by.
    arrival_time = db.Column("arrival_time", db.Time,
                             nullable=True)  # record train's arrival time from certain station.
    departure_time = db.Column("departure_time", db.Time,
                               nullable=True)  # record train's departure time from certain station.
    transfer_station = db.Column("transfer_station",
                                 db.Boolean)  # 1 menas this station can transfer to other line, 0 otherwise.

    #dwell_time = db.Column("dwell_time", db.Integer, nullable=True)  # train's dwell time at this station
    #final_destination = db.Column("final_distination", db.String(100))  # train's final destination.
    # line = db.Column("line", db.String(100)) # Line of this train (e.g. Route A, Route B ...)
    # direction = db.Column("direction", db.Boolean) # 0 means from the first station (0km) to final destination(xxkm), 1 means from final destination (xxkm) to the first station (0km)
    # distance = db.Column("distance", db.Integer) # the distance from this station to the first station.
    # total_line_length = db.Column("total_distance", db.Integer) # total length of this line

    # def __init__(self, train_type, station, arrival_time, departure_time, dwell_time, distance, final_destination, transfer_station):
    #     self.name = name
    #     self.email = email


class User_data(db.Model):
    username = db.Column("username", db.String(100), primary_key=True) # Line's name, such as red line, blue line
    password = db.Column("password", db.String(100)) # station that this line will dwell
    gender = db.Column("email", db.String(100)) # station's corresponding distance from the 0km first station.
    #station_type = db.Column("station_type", db.Integer) # describe station type. if local train stops at this station, +1, otherwise +0; if rapid train stops at this station, +10, otherwise + 0;



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("New Train Database has been created successfully")
    #app.run(debug=True)





