# # # # Update Line_data database
# # # #
# import csv
# from Flask_Database_Data_Input import db
# from Flask_Database_Data_Input import Line_data
# from Flask_Database_Data_Input import app
#
# with app.app_context():
#     with open('Line_data.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             exists = db.session.query(Line_data).filter_by(line=row['line'], station=row['station']).first()
#
#             if exists:
#                 continue
#             line_data = Line_data(line=row['line'], station=row['station'], distance=row['distance'], station_type=row['station_type'], transfer=row['transfer'])
#             db.session.add(line_data)
#
#         db.session.commit()
# #
#
# print("Line_data has been successfully updated!")


#
# # update Red_Line_Outbound_data database

# import csv
# from Flask_Database_Data_Input import db
# from Flask_Database_Data_Input import Red_Line_Outbound_data
# from Flask_Database_Data_Input import app
# from datetime import datetime
#
# with app.app_context():
#     with open('Red_Line_Outbound_data.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if row['arrival_time'].lower().strip() == 'null':
#                 row['arrival_time'] = None
#             else:
#                 row['arrival_time'] = datetime.strptime(row['arrival_time'], '%H:%M').time()
#
#             if row['departure_time'].lower().strip() == 'null':
#                 row['departure_time'] = None
#             else:
#                 row['departure_time'] = datetime.strptime(row['departure_time'], '%H:%M').time()
#
#             if row['transfer_station'] == 'TRUE':
#                 row['transfer_station'] = True
#             else:
#                 row['transfer_station'] = False
#
#             exists = db.session.query(Red_Line_Outbound_data).filter_by(train_id=row['train_id'], station=row['station']).first()
#
#             if exists:
#                 continue
#
#             line_data = Red_Line_Outbound_data(train_id=row['train_id'], station=row['station'], train_type=row['train_type'],
#                                       arrival_time=row['arrival_time'], departure_time=row["departure_time"], transfer_station=row["transfer_station"])
#             db.session.add(line_data)
#
#         db.session.commit()
#
#
# print("Red_Line_Outbound_data has been successfully updated!")


#
# # update Red_Line_Inbound_data database
#
# import csv
# from Flask_Database_Data_Input import db
# from Flask_Database_Data_Input import Red_Line_Inbound_data
# from Flask_Database_Data_Input import app
# from datetime import datetime
#
# with app.app_context():
#     with open('Red_Line_Inbound_data.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if row['arrival_time'].lower().strip() == 'null':
#                 row['arrival_time'] = None
#             else:
#                 row['arrival_time'] = datetime.strptime(row['arrival_time'], '%H:%M').time()
#
#             if row['departure_time'].lower().strip() == 'null':
#                 row['departure_time'] = None
#             else:
#                 row['departure_time'] = datetime.strptime(row['departure_time'], '%H:%M').time()
#
#             if row['transfer_station'] == 'TRUE':
#                 row['transfer_station'] = True
#             else:
#                 row['transfer_station'] = False
#
#             exists = db.session.query(Red_Line_Inbound_data).filter_by(train_id=row['train_id'], station=row['station']).first()
#
#             if exists:
#                 continue
#
#             line_data = Red_Line_Inbound_data(train_id=row['train_id'], station=row['station'], train_type=row['train_type'],
#                                       arrival_time=row['arrival_time'], departure_time=row["departure_time"], transfer_station=row["transfer_station"])
#             db.session.add(line_data)
#
#         db.session.commit()
#
#
# print("Red_Line_Inbound_data has been successfully updated!")

#
# # update Green_Line_Outbound_data database
#
# import csv
# from Flask_Database_Data_Input import db
# from Flask_Database_Data_Input import Green_Line_Outbound_data
# from Flask_Database_Data_Input import app
# from datetime import datetime
#
# with app.app_context():
#     with open('Green_Line_Outbound_data.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if row['arrival_time'].lower().strip() == 'null':
#                 row['arrival_time'] = None
#             else:
#                 row['arrival_time'] = datetime.strptime(row['arrival_time'], '%H:%M').time()
#
#             if row['departure_time'].lower().strip() == 'null':
#                 row['departure_time'] = None
#             else:
#                 row['departure_time'] = datetime.strptime(row['departure_time'], '%H:%M').time()
#
#             if row['transfer_station'] == 'TRUE':
#                 row['transfer_station'] = True
#             else:
#                 row['transfer_station'] = False
#
#             exists = db.session.query(Green_Line_Outbound_data).filter_by(train_id=row['train_id'], station=row['station']).first()
#
#             if exists:
#                 continue
#
#             line_data = Green_Line_Outbound_data(train_id=row['train_id'], station=row['station'], train_type=row['train_type'],
#                                       arrival_time=row['arrival_time'], departure_time=row["departure_time"], transfer_station=row["transfer_station"])
#             db.session.add(line_data)
#
#         db.session.commit()
#
#
# print("Green_Line_Outbound_data has been successfully updated!")


# # update Green_Line_Inbound_data database
#
# import csv
# from Flask_Database_Data_Input import db
# from Flask_Database_Data_Input import Green_Line_Inbound_data
# from Flask_Database_Data_Input import app
# from datetime import datetime
#
# with app.app_context():
#     with open('Green_Line_Inbound_data.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if row['arrival_time'].lower().strip() == 'null':
#                 row['arrival_time'] = None
#             else:
#                 row['arrival_time'] = datetime.strptime(row['arrival_time'], '%H:%M').time()
#
#             if row['departure_time'].lower().strip() == 'null':
#                 row['departure_time'] = None
#             else:
#                 row['departure_time'] = datetime.strptime(row['departure_time'], '%H:%M').time()
#
#             if row['transfer_station'] == 'TRUE':
#                 row['transfer_station'] = True
#             else:
#                 row['transfer_station'] = False
#
#             exists = db.session.query(Green_Line_Inbound_data).filter_by(train_id=row['train_id'], station=row['station']).first()
#
#             if exists:
#                 continue
#
#             line_data = Green_Line_Inbound_data(train_id=row['train_id'], station=row['station'], train_type=row['train_type'],
#                                       arrival_time=row['arrival_time'], departure_time=row["departure_time"], transfer_station=row["transfer_station"])
#             db.session.add(line_data)
#
#         db.session.commit()
#
#
# print("Green_Line_Inbound_data has been successfully updated!")

#
# # update Orange_Line_Outbound_data database
#
# import csv
# from Flask_Database_Data_Input import db
# from Flask_Database_Data_Input import Orange_Line_Outbound_data
# from Flask_Database_Data_Input import app
# from datetime import datetime
#
# with app.app_context():
#     with open('Orange_Line_Outbound_data.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if row['arrival_time'].lower().strip() == 'null':
#                 row['arrival_time'] = None
#             else:
#                 row['arrival_time'] = datetime.strptime(row['arrival_time'], '%H:%M').time()
#
#             if row['departure_time'].lower().strip() == 'null':
#                 row['departure_time'] = None
#             else:
#                 row['departure_time'] = datetime.strptime(row['departure_time'], '%H:%M').time()
#
#             if row['transfer_station'] == 'TRUE':
#                 row['transfer_station'] = True
#             else:
#                 row['transfer_station'] = False
#
#             exists = db.session.query(Orange_Line_Outbound_data).filter_by(train_id=row['train_id'], station=row['station']).first()
#
#             if exists:
#                 continue
#
#             line_data = Orange_Line_Outbound_data(train_id=row['train_id'], station=row['station'], train_type=row['train_type'],
#                                       arrival_time=row['arrival_time'], departure_time=row["departure_time"], transfer_station=row["transfer_station"])
#             db.session.add(line_data)
#
#         db.session.commit()
#
#
# print("Orange_Line_Outbound_data has been successfully updated!")

#
# # update Orange_Line_Inbound_data database
#
# import csv
# from Flask_Database_Data_Input import db
# from Flask_Database_Data_Input import Orange_Line_Inbound_data
# from Flask_Database_Data_Input import app
# from datetime import datetime
#
# with app.app_context():
#     with open('Orange_Line_Inbound_data.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if row['arrival_time'].lower().strip() == 'null':
#                 row['arrival_time'] = None
#             else:
#                 row['arrival_time'] = datetime.strptime(row['arrival_time'], '%H:%M').time()
#
#             if row['departure_time'].lower().strip() == 'null':
#                 row['departure_time'] = None
#             else:
#                 row['departure_time'] = datetime.strptime(row['departure_time'], '%H:%M').time()
#
#             if row['transfer_station'] == 'TRUE':
#                 row['transfer_station'] = True
#             else:
#                 row['transfer_station'] = False
#
#             exists = db.session.query(Orange_Line_Inbound_data).filter_by(train_id=row['train_id'], station=row['station']).first()
#
#             if exists:
#                 continue
#
#             line_data = Orange_Line_Inbound_data(train_id=row['train_id'], station=row['station'], train_type=row['train_type'],
#                                       arrival_time=row['arrival_time'], departure_time=row["departure_time"], transfer_station=row["transfer_station"])
#             db.session.add(line_data)
#
#         db.session.commit()
#
#
# print("Orange_Line_Inbound_data has been successfully updated!")



#
# # update Black_Line_Outbound_data database
#
# import csv
# from Flask_Database_Data_Input import db
# from Flask_Database_Data_Input import Black_Line_Outbound_data
# from Flask_Database_Data_Input import app
# from datetime import datetime
#
# with app.app_context():
#     with open('Black_Line_Outbound_data.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if row['arrival_time'].lower().strip() == 'null':
#                 row['arrival_time'] = None
#             else:
#                 row['arrival_time'] = datetime.strptime(row['arrival_time'], '%H:%M').time()
#
#             if row['departure_time'].lower().strip() == 'null':
#                 row['departure_time'] = None
#             else:
#                 row['departure_time'] = datetime.strptime(row['departure_time'], '%H:%M').time()
#
#             if row['transfer_station'] == 'TRUE':
#                 row['transfer_station'] = True
#             else:
#                 row['transfer_station'] = False
#
#             exists = db.session.query(Black_Line_Outbound_data).filter_by(train_id=row['train_id'], station=row['station']).first()
#
#             if exists:
#                 continue
#
#             line_data = Black_Line_Outbound_data(train_id=row['train_id'], station=row['station'], train_type=row['train_type'],
#                                       arrival_time=row['arrival_time'], departure_time=row["departure_time"], transfer_station=row["transfer_station"])
#             db.session.add(line_data)
#
#         db.session.commit()
#
#
# print("Black_Line_Outbound_data has been successfully updated!")


# update Black_Line_Inbound_data database
#
# import csv
# from Flask_Database_Data_Input import db
# from Flask_Database_Data_Input import Black_Line_Inbound_data
# from Flask_Database_Data_Input import app
# from datetime import datetime
#
# with app.app_context():
#     with open('Black_Line_Inbound_data.csv', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if row['arrival_time'].lower().strip() == 'null':
#                 row['arrival_time'] = None
#             else:
#                 row['arrival_time'] = datetime.strptime(row['arrival_time'], '%H:%M').time()
#
#             if row['departure_time'].lower().strip() == 'null':
#                 row['departure_time'] = None
#             else:
#                 row['departure_time'] = datetime.strptime(row['departure_time'], '%H:%M').time()
#
#             if row['transfer_station'] == 'TRUE':
#                 row['transfer_station'] = True
#             else:
#                 row['transfer_station'] = False
#
#             exists = db.session.query(Black_Line_Inbound_data).filter_by(train_id=row['train_id'], station=row['station']).first()
#
#             if exists:
#                 continue
#
#             line_data = Black_Line_Inbound_data(train_id=row['train_id'], station=row['station'], train_type=row['train_type'],
#                                       arrival_time=row['arrival_time'], departure_time=row["departure_time"], transfer_station=row["transfer_station"])
#             db.session.add(line_data)
#
#         db.session.commit()
#
#
# print("Black_Line_Inbound_data has been successfully updated!")
