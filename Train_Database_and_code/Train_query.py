from Flask_Database_Data_Input import Line_data
from Flask_Database_Data_Input import Red_Line_Inbound_data
from Flask_Database_Data_Input import Red_Line_Outbound_data
from Flask_Database_Data_Input import Green_Line_Inbound_data
from Flask_Database_Data_Input import Green_Line_Outbound_data
from Flask_Database_Data_Input import Black_Line_Inbound_data
from Flask_Database_Data_Input import Black_Line_Outbound_data
from Flask_Database_Data_Input import Orange_Line_Inbound_data
from Flask_Database_Data_Input import Orange_Line_Outbound_data
from Flask_Database_Data_Input import app
import re
from datetime import datetime

class Station_Structure:
    def __init__(self, station, time, transfer, type, cost = 0, previous_train_id = 0, previous_station = "", reachable = False):
        self.station = station
        self.time = time
        self.transfer = transfer
        self.type = type
        self.cost = cost
        self.previous_train_id = previous_train_id #id
        self.previous_station = previous_station
        self.reachable = reachable

# check start_pos validation
def Start_pos_input_test():
    start_pos = input("Start position:")
    judge_validation = Line_data.query.filter_by(station=start_pos).first() is not None
    if judge_validation:
        return start_pos
    else:
        print("Start position Error")
        return Start_pos_input_test()

#check destination validation
def Destination_input_test(start_pos):
    destination = input("Destination:")
    judge_validation = Line_data.query.filter_by(station=destination).first() is not None
    if judge_validation and destination != start_pos:
        return destination
    else:
        if destination == start_pos:
            print("Destination cannot be the same as the start position!")
        else:
            print("Destination Error")
        return Destination_input_test()

#check criteria validation
def Criteration_input_test():
    print("Criteration:\n1.Less Travel Time\n2.Less Money\n3.Less Transfer Times")
    criteria = input("Your choice:")
    if criteria in ["1", "2", "3"]:
        return criteria
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        return Criteration_input_test()

#check departure time validation
def Departure_time_input_text():
    time_input = input("Enter departure time (HH:MM): ")
    if re.fullmatch(r'([0-1]?\d|2[0-3]):[0-5]\d', time_input):
        time_obj = datetime.strptime(time_input, "%H:%M").time()
        return time_obj
    else:
        print("Invalid time format. Please enter time in HH:MM format (e.g., 11:22).")
        return Departure_time_input_text()

#initial setup for every station
def Initialize_station(wait_list, departure_time):
    latest_time = datetime.strptime("23:59", "%H:%M").time()

    # Red_line station set up
    redLine_station = []
    for i in range(1, 14):
        temp_station = "R" + str(i)
        temp_data = Line_data.query.filter_by(station=temp_station).first()
        if temp_station in wait_list:
            temp = Station_Structure(temp_station, departure_time, temp_data.transfer, temp_data.station_type, 0, 0, "", True)
        else:
            temp = Station_Structure(temp_station, latest_time, temp_data.transfer, temp_data.station_type)
        redLine_station.append(temp)

    # Green_line station set up
    greenLine_station = []
    for i in range(1, 15):
        temp_station = "G" + str(i)
        temp_data = Line_data.query.filter_by(station=temp_station).first()
        if temp_station in wait_list:
            temp = Station_Structure(temp_station, departure_time, temp_data.transfer, temp_data.station_type, 0, 0, "", True)
        else:
            temp = Station_Structure(temp_station, latest_time, temp_data.transfer, temp_data.station_type)
        greenLine_station.append(temp)

    # Orange_line station set up
    orangeLine_station = []
    for i in range(1, 9):
        temp_station = "O" + str(i)
        temp_data = Line_data.query.filter_by(station=temp_station).first()
        if temp_station in wait_list:
            temp = Station_Structure(temp_station, departure_time, temp_data.transfer, temp_data.station_type, 0, 0, "", True)
        else:
            temp = Station_Structure(temp_station, latest_time, temp_data.transfer, temp_data.station_type)
        orangeLine_station.append(temp)

    # Black_line station set up
    blackLine_station = []
    for i in range(1, 10):
        temp_station = "B" + str(i)
        temp_data = Line_data.query.filter_by(station=temp_station).first()
        if temp_station in wait_list:
            temp = Station_Structure(temp_station, departure_time, temp_data.transfer, temp_data.station_type, 0, 0, "", True)
        else:
            temp = Station_Structure(temp_station, latest_time, temp_data.transfer, temp_data.station_type)
        blackLine_station.append(temp)

    station_info = [[] for _ in range(4)]
    for station in redLine_station:
        station_info[0].append(station)

    for station in greenLine_station:
        station_info[1].append(station)

    for station in orangeLine_station:
        station_info[2].append(station)

    for station in blackLine_station:
        station_info[3].append(station)

    return station_info
    # return redLine_station, greenLine_station, orangeLine_station, blackLine_station

#assign time to the same transfer stations
def Assign_time_to_transfer_station(new_wait_list, station_info, time, previous_station):
    for station in new_wait_list:
        station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(station[0], -1)
        station_number = int(station[1:]) - 1
        station_info[station_line_number][station_number].time = time
        station_info[station_line_number][station_number].previous_station = previous_station

    return station_info

#initialize wait_list
def Initialize_wait_list(start_pos):
    wait_list = []
    start_pos_data = Line_data.query.filter_by(station=start_pos).first()
    is_transfer = start_pos_data.transfer
    if is_transfer > 0:
        transfer_line = Line_data.query.filter_by(transfer=is_transfer)
        for data in transfer_line:
            wait_list.append(data.station)
    else:
        wait_list.append(start_pos)
    return wait_list

#find the closest rapid stations
def Find_closest_rapid_station(current_station, station_info):
    new_list = []
    current_station_line = current_station[0]
    current_station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(current_station[0], -1)
    current_station_number = int(current_station[1:]) - 1
    i = current_station_number - 1
    while True:
        if station_info[current_station_line_number][i].type == 11:
            rapid_station = current_station_line + str(i + 1)
            new_list.append(rapid_station)
            break
        i = i + 1
    j = current_station_number + 1
    while True:
        if station_info[current_station_line_number][j].type == 11:
            rapid_station = current_station_line + str(j + 1)
            new_list.append(rapid_station)
            break
        j = j + 1
    return new_list

# calculate money cost
# rule: first 6km costs 2$, 6-10km costs 0.2$/km, 10-15km costs 0.15$/km, 15km or more cost 0.1$/km
def Money_cost(start_pos, destination):
    start_pos_data = Line_data.query.filter_by(station=start_pos).first()
    destination_data = Line_data.query.filter_by(station=destination).first()
    if destination > start_pos:
        distance = destination_data.distance - start_pos_data.distance
    else:
        distance = start_pos_data.distance - destination_data.distance
    if distance <= 6:
        total_price = 2
    elif distance <= 10:
        total_price = 2 + 0.2*(distance - 6)
        total_price = round(total_price, 2)
    elif distance <= 15:
        total_price = 2 + 0.2 * 4 + 0.15 * (distance - 10)
        total_price = round(total_price, 2)
    else:
        total_price = 2 + 0.2 * 4 + 0.15 * 5 + 0.1 * (distance - 15)
        total_price = roung(total_price, 2)
    return total_price

line_inbound_data_mapping = {
    'R': Red_Line_Inbound_data,
    'G': Green_Line_Inbound_data,
    'O': Orange_Line_Inbound_data,
    'B': Black_Line_Inbound_data
}

line_outbound_data_mapping = {
    'R': Red_Line_Outbound_data,
    'G': Green_Line_Outbound_data,
    'O': Orange_Line_Outbound_data,
    'B': Black_Line_Outbound_data
}

def Less_travel_time_algorithm(start_pos, destination, departure_time):
    destination_line = destination[0]
    destination_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(destination[0], -1)
    destination_number = int(destination[1:]) - 1
    #redLine_station, greenLine_station, orangeLine_station, blackLine_station = Initialize_station(departure_time)
    wait_list = Initialize_wait_list(start_pos)
    station_info = Initialize_station(wait_list, departure_time)
    while len(wait_list) > 0:
        station = wait_list.pop()
        station_line = station[0]
        station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(station[0], -1)
        station_number = int(station[1:]) - 1
        if(station_line == "G" or station_line == "B"):
            temp_inbound_data = line_inbound_data_mapping[station_line].query.filter_by(station=station).filter(line_inbound_data_mapping[station_line].departure_time >= station_info[station_line_number][station_number].time).first()
            temp_outbound_data = line_outbound_data_mapping[station_line].query.filter_by(station=station).filter(line_outbound_data_mapping[station_line].departure_time >= station_info[station_line_number][station_number].time).first()
            for i in range(station_number - 1, -1, -1):
            # for i in range(station_number):
                temp_station = station_line + str(i + 1)
                # print(station_info[station_line_number][i].time)

                if temp_inbound_data == None:
                    break

                inbound_train_id = temp_inbound_data.train_id
                temp_time = line_inbound_data_mapping[station_line].query.filter_by(station=temp_station).filter_by(
                    train_id=inbound_train_id).first().arrival_time
                if temp_time <= station_info[station_line_number][i].time:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = inbound_train_id
                    station_info[station_line_number][i].reachable = True

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station)
                        wait_list = new_wait_list + wait_list

                # print(station_info[station_line_number][i].time)
            upperbound = 9 if station_line == "B" else 14
            for i in range (station_number + 1, upperbound):
                temp_station = station_line + str(i + 1)
                if temp_outbound_data == None:
                    break
                outbound_train_id = temp_outbound_data.train_id
                temp_time = line_outbound_data_mapping[station_line].query.filter_by(
                    station=temp_station).filter_by(train_id=outbound_train_id).first().arrival_time
                if temp_time <= station_info[station_line_number][i].time:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = outbound_train_id
                    station_info[station_line_number][i].reachable = True

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station)
                        wait_list = new_wait_list + wait_list
        else: #station_line == "R" or "O", lines have rapid train service
            temp_inbound_local_data = line_inbound_data_mapping[station_line].query.filter_by(station=station, train_type="Local").filter(
                line_inbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            temp_outbound_local_data = line_outbound_data_mapping[station_line].query.filter_by(station=station, train_type="Local").filter(
                line_outbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            temp_inbound_rapid_data = line_inbound_data_mapping[station_line].query.filter_by(station=station, train_type="Rapid").filter(
                line_inbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            temp_outbound_rapid_data = line_outbound_data_mapping[station_line].query.filter_by(station=station, train_type="Rapid").filter(
                line_outbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            for i in range(station_number):
                temp_station = station_line + str(i + 1)
                if temp_inbound_local_data == None:
                    break

                inbound_local_train_id = temp_inbound_local_data.train_id
                temp_local_time = line_inbound_data_mapping[station_line].query.filter_by(station=temp_station, train_id=inbound_local_train_id).first().arrival_time
                temp_time = temp_local_time
                temp_inbound_train_id = inbound_local_train_id
                if temp_inbound_rapid_data != None and station_info[station_line_number][i].type > 1:
                    inbound_rapid_train_id = temp_inbound_rapid_data.train_id
                    temp_rapid_time = line_inbound_data_mapping[station_line].query.filter_by(station=temp_station, train_id=inbound_rapid_train_id).first().arrival_time
                    if temp_rapid_time < temp_time:
                        temp_time = temp_rapid_time
                        temp_inbound_train_id = inbound_rapid_train_id
                if temp_time <= station_info[station_line_number][i].time and temp_inbound_train_id != station_info[station_line_number][i].previous_train_id:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = temp_inbound_train_id
                    station_info[station_line_number][i].reachable = True

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station)
                        wait_list = new_wait_list + wait_list
                        # print(wait_list)
            upperbound = 13 if station_line == "R" else 8
            for i in range(station_number + 1, upperbound):
                temp_station = station_line + str(i + 1)
                if temp_outbound_local_data == None:
                    break

                outbound_local_train_id = temp_outbound_local_data.train_id
                temp_local_time = line_outbound_data_mapping[station_line].query.filter_by(station=temp_station, train_id=outbound_local_train_id).first().arrival_time
                temp_time = temp_local_time
                temp_outbound_train_id = outbound_local_train_id
                if temp_outbound_rapid_data != None and station_info[station_line_number][i].type > 1:
                    outbound_rapid_train_id = temp_outbound_rapid_data.train_id
                    temp_rapid_time = line_outbound_data_mapping[station_line].query.filter_by(station=temp_station, train_id=outbound_rapid_train_id).first().arrival_time
                    if temp_rapid_time < temp_time:
                        temp_time = temp_rapid_time
                        temp_outbound_train_id = outbound_rapid_train_id
                if temp_time <= station_info[station_line_number][i].time and temp_outbound_train_id != station_info[station_line_number][i].previous_train_id:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = temp_outbound_train_id
                    station_info[station_line_number][i].reachable = True

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station)
                        wait_list = new_wait_list + wait_list
            if destination_line == station_line:

                if station_info[destination_line_number][destination_number].type == 1:
                    new_wait_list = Find_closest_rapid_station(destination, station_info)
                    wait_list = wait_list + new_wait_list
            # print(station_info[station_line_number][station_number].type)
            if station_info[station_line_number][station_number].type == 1:
                new_wait_list = Find_closest_rapid_station(station, station_info)
                wait_list = wait_list + new_wait_list

    return station_info

        # if station_line == "R":

def Less_money_algorithm(start_pos, destination, departure_time):
    destination_line = destination[0]
    destination_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(destination[0], -1)
    destination_number = int(destination[1:]) - 1
    wait_list = Initialize_wait_list(start_pos)
    station_info = Initialize_station(wait_list, departure_time)
    while len(wait_list) > 0:
        station = wait_list.pop()
        station_line = station[0]
        station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(station[0], -1)
        station_number = int(station[1:]) - 1
        if(station_line == "G" or station_line == "B"):
            temp_inbound_data = line_inbound_data_mapping[station_line].query.filter_by(station=station).filter(line_inbound_data_mapping[station_line].departure_time >= station_info[station_line_number][station_number].time).first()
            temp_outbound_data = line_outbound_data_mapping[station_line].query.filter_by(station=station).filter(line_outbound_data_mapping[station_line].departure_time >= station_info[station_line_number][station_number].time).first()
            for i in range(station_number - 1, -1, -1):
            # for i in range(station_number):
                temp_station = station_line + str(i + 1)
                # print(station_info[station_line_number][i].time)

                if temp_inbound_data == None:
                    break

                inbound_train_id = temp_inbound_data.train_id
            #here hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
                temp_time = line_inbound_data_mapping[station_line].query.filter_by(station=temp_station).filter_by(
                    train_id=inbound_train_id).first().arrival_time
                if temp_time <= station_info[station_line_number][i].time:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = inbound_train_id
                    station_info[station_line_number][i].reachable = True

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station)
                        wait_list = new_wait_list + wait_list

                # print(station_info[station_line_number][i].time)
            upperbound = 9 if station_line == "B" else 14
            for i in range (station_number + 1, upperbound):
                temp_station = station_line + str(i + 1)
                if temp_outbound_data == None:
                    break
                outbound_train_id = temp_outbound_data.train_id
                temp_time = line_outbound_data_mapping[station_line].query.filter_by(
                    station=temp_station).filter_by(train_id=outbound_train_id).first().arrival_time
                if temp_time <= station_info[station_line_number][i].time:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = outbound_train_id
                    station_info[station_line_number][i].reachable = True

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station)
                        wait_list = new_wait_list + wait_list
        else: #station_line == "R" or "O", lines have rapid train service
            temp_inbound_local_data = line_inbound_data_mapping[station_line].query.filter_by(station=station, train_type="Local").filter(
                line_inbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            temp_outbound_local_data = line_outbound_data_mapping[station_line].query.filter_by(station=station, train_type="Local").filter(
                line_outbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            temp_inbound_rapid_data = line_inbound_data_mapping[station_line].query.filter_by(station=station, train_type="Rapid").filter(
                line_inbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            temp_outbound_rapid_data = line_outbound_data_mapping[station_line].query.filter_by(station=station, train_type="Rapid").filter(
                line_outbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            for i in range(station_number):
                temp_station = station_line + str(i + 1)
                if temp_inbound_local_data == None:
                    break

                inbound_local_train_id = temp_inbound_local_data.train_id
                temp_local_time = line_inbound_data_mapping[station_line].query.filter_by(station=temp_station, train_id=inbound_local_train_id).first().arrival_time
                temp_time = temp_local_time
                temp_inbound_train_id = inbound_local_train_id
                if temp_inbound_rapid_data != None and station_info[station_line_number][i].type > 1:
                    inbound_rapid_train_id = temp_inbound_rapid_data.train_id
                    temp_rapid_time = line_inbound_data_mapping[station_line].query.filter_by(station=temp_station, train_id=inbound_rapid_train_id).first().arrival_time
                    if temp_rapid_time < temp_time:
                        temp_time = temp_rapid_time
                        temp_inbound_train_id = inbound_rapid_train_id
                if temp_time <= station_info[station_line_number][i].time and temp_inbound_train_id != station_info[station_line_number][i].previous_train_id:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = temp_inbound_train_id
                    station_info[station_line_number][i].reachable = True

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station)
                        wait_list = new_wait_list + wait_list
                        # print(wait_list)
            upperbound = 13 if station_line == "R" else 8
            for i in range(station_number + 1, upperbound):
                temp_station = station_line + str(i + 1)
                if temp_outbound_local_data == None:
                    break

                outbound_local_train_id = temp_outbound_local_data.train_id
                temp_local_time = line_outbound_data_mapping[station_line].query.filter_by(station=temp_station, train_id=outbound_local_train_id).first().arrival_time
                temp_time = temp_local_time
                temp_outbound_train_id = outbound_local_train_id
                if temp_outbound_rapid_data != None and station_info[station_line_number][i].type > 1:
                    outbound_rapid_train_id = temp_outbound_rapid_data.train_id
                    temp_rapid_time = line_outbound_data_mapping[station_line].query.filter_by(station=temp_station, train_id=outbound_rapid_train_id).first().arrival_time
                    if temp_rapid_time < temp_time:
                        temp_time = temp_rapid_time
                        temp_outbound_train_id = outbound_rapid_train_id
                if temp_time <= station_info[station_line_number][i].time and temp_outbound_train_id != station_info[station_line_number][i].previous_train_id:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = temp_outbound_train_id
                    station_info[station_line_number][i].reachable = True

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station)
                        wait_list = new_wait_list + wait_list
            if destination_line == station_line:

                if station_info[destination_line_number][destination_number].type == 1:
                    new_wait_list = Find_closest_rapid_station(destination, station_info)
                    wait_list = wait_list + new_wait_list
            # print(station_info[station_line_number][station_number].type)
            if station_info[station_line_number][station_number].type == 1:
                new_wait_list = Find_closest_rapid_station(station, station_info)
                wait_list = wait_list + new_wait_list

    return station_info



def main():
    with app.app_context():
        start_pos = Start_pos_input_test()
        destination = Destination_input_test(start_pos)
        criteria = Criteration_input_test()
        departure_time = Departure_time_input_text()
        if int(criteria) == 1:
            station_info = Less_travel_time_algorithm(start_pos, destination, departure_time)
            current_station = destination

            print("\n\n\n")
            while current_station != start_pos:
                current_station_line = current_station[0]
                current_station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(current_station[0], -1)
                current_station_number = int(current_station[1:]) - 1
                # if station_info[current_station_line_number][current_station_number].reachable == False:
                #     print("No Available Route!")
                #     break
                temp_station = station_info[current_station_line_number][current_station_number].previous_station
                if Line_data.query.filter_by(station=temp_station).first().transfer == Line_data.query.filter_by(station=current_station).first().transfer and Line_data.query.filter_by(station=current_station).first().transfer > 0:
                    print("transfer here")
                    print(current_station)
                    print(temp_station)
                else:
                    print(current_station)
                    print(station_info[current_station_line_number][current_station_number].previous_train_id)
                    print(station_info[current_station_line_number][current_station_number].type)
                    print(station_info[current_station_line_number][current_station_number].time)
                    print(station_info[current_station_line_number][current_station_number].previous_station)
                current_station = temp_station
                print("\n\n\n")
        # if int(criteria) == 2:
        #     station_info = Less_money_algorithm(start_pos, destination, departure_time)

main()

