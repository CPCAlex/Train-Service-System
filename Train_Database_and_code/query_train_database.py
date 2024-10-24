#query Line_data database

# from Flask_Database_Data_Input import db
# from Flask_Database_Data_Input import Line_data
# from Flask_Database_Data_Input import app
#
# with app.app_context():
#     # db.session.query(Line_data).delete()
#     # db.session.commit()
#     all_data = Line_data.query.all()
#     for data in all_data:
#         print(data.line, data.station, data.distance, data.station_type, data.transfer)
#

#query Red_Line_Outbound_data database
#
# from Flask_Database_Data_Input import db
# from Flask_Database_Data_Input import Red_Line_Outbound_data
# from Flask_Database_Data_Input import app
#
# with app.app_context():
#
#     all_data = Red_Line_Outbound_data.query.all()
#     for data in all_data:
#         print(data.train_id, data.train_type, data.station, data.arrival_time, data.departure_time, data.transfer_station)




#query Red_Line_Inbound_data database

from Flask_Database_Data_Input import db
from Flask_Database_Data_Input import Red_Line_Inbound_data
from Flask_Database_Data_Input import app

with app.app_context():
    all_data = Red_Line_Inbound_data.query.all()
    for data in all_data:
        print(data.train_id, data.train_type, data.station, data.arrival_time, data.departure_time, data.transfer_station)



#query Green_Line_data database
#
# from Flask_Database_Data_Input import db
# from Flask_Database_Data_Input import Green_Line_data
# from Flask_Database_Data_Input import app
#
# with app.app_context():
#
#     all_data = Green_Line_data.query.all()
#     for data in all_data:
#         print(data.train_id, data.train_type, data.station, data.arrival_time, data.departure_time, data.transfer_station)