from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import Train_query
import sys
import os
from datetime import datetime, timedelta, time
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import sys

from Flask_Database_Data_Input import db, Line_data, Red_Line_Outbound_data, Red_Line_Inbound_data, \
    Green_Line_Outbound_data, Green_Line_Inbound_data, Orange_Line_Outbound_data, Orange_Line_Inbound_data, \
    Black_Line_Outbound_data, Black_Line_Inbound_data, User_data

app = Flask(__name__)

CORS(app)

app.secret_key = 'cpc'  

WIN = sys.platform.startswith('win')
prefix = 'sqlite:///' if WIN else 'sqlite:////'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(basedir, 'instance', 'train_data.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)

db.init_app(app)

@app.route('/api/less_money', methods=['POST'])
def less_money():
    data = request.json
    start_pos = data.get('start_pos')
    destination = data.get('destination')
    departure_time = data.get('departure_time')

    destination_reachable, total_step, solution, total_transfer_time, total_money_spent, initial_departure_time, final_arrival_time = Train_query.Less_money_algorithm(start_pos, destination, departure_time)

    result = {
        "destination_reachable": destination_reachable,
        "total_step": total_step,
        "solution": solution,
        "total_transfer_time": total_transfer_time,
        "total_money_spent": total_money_spent,
        "initial_departure_time": initial_departure_time,
        "final_arrival_time": final_arrival_time
    }

    for key, value in result.items():
        if isinstance(value, datetime):
            result[key] = value.strftime("%H:%M")
        elif isinstance(value, time):
            result[key] = value.strftime("%H:%M")

    print("Result after serialization:", result)

    return jsonify(result)

@app.route('/api/less_travel_time', methods=['POST'])
def less_travel_time():
    data = request.json
    start_pos = data.get('start_pos')
    destination = data.get('destination')
    departure_time = data.get('departure_time')
    result = Train_query.Less_travel_time_algorithm(start_pos, destination, departure_time)

    destination_reachable, total_step, solution, total_transfer_time, total_money_spent, initial_departure_time, final_arrival_time = Train_query.Less_travel_time_algorithm(start_pos, destination, departure_time)

    result = {
        "destination_reachable": destination_reachable,
        "total_step": total_step,
        "solution": solution,
        "total_transfer_time": total_transfer_time,
        "total_money_spent": total_money_spent,
        "initial_departure_time": initial_departure_time,
        "final_arrival_time": final_arrival_time
    }

    for key, value in result.items():
        
        if isinstance(value, datetime):
            result[key] = value.strftime("%H:%M")
        
        elif isinstance(value, time):
            result[key] = value.strftime("%H:%M")

    print("Result after serialization:", result)

    return jsonify(result)

@app.route('/api/less_transfer_time', methods=['POST'])
def less_transfer_time():
    data = request.json
    start_pos = data.get('start_pos')
    destination = data.get('destination')
    departure_time = data.get('departure_time')

    destination_reachable, total_step, solution, total_transfer_time, total_money_spent, initial_departure_time, final_arrival_time = Train_query.Less_transfer_time_algorithm(start_pos, destination, departure_time)

    result = {
        "destination_reachable": destination_reachable,
        "total_step": total_step,
        "solution": solution,
        "total_transfer_time": total_transfer_time,
        "total_money_spent": total_money_spent,
        "initial_departure_time": initial_departure_time,
        "final_arrival_time": final_arrival_time
    }

    
    for key, value in result.items():
        
        if isinstance(value, datetime):
            result[key] = value.strftime("%H:%M")
       
        elif isinstance(value, time):
            result[key] = value.strftime("%H:%M")

    print("Result after serialization:", result)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)