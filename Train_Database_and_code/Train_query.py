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
    def __init__(self, station, time, transfer, type, transfer_time = 999, cost = 0,  previous_train_id = 0, previous_station = "", reachable = False):
        self.station = station
        self.time = time
        self.transfer = transfer
        self.type = type
        self.transfer_time = transfer_time
        self.cost = cost
        self.previous_train_id = previous_train_id #id
        self.previous_station = previous_station
        self.reachable = reachable

# check start_pos validation
def Start_pos_input_test(start_pos):
    judge_validation = Line_data.query.filter_by(station=start_pos).first() is not None
    if judge_validation:
        return True
    else:
        # print("Start position Error")
        return False

#check destination validation
def Destination_input_test(start_pos, destination):
    # destination = input("Destination:")
    judge_validation = Line_data.query.filter_by(station=destination).first() is not None
    if judge_validation and destination != start_pos:
        return True
    else:
        # if destination == start_pos:
        #     print("Destination cannot be the same as the start position!")
        # else:
        #     print("Destination Error")
        return False

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
def Departure_time_input_text(time_input):

    if re.fullmatch(r'([0-1]?\d|2[0-3]):[0-5]\d', time_input):
        #time_obj = datetime.strptime(time_input, "%H:%M").time()
        return True
    else:
        #print("Invalid time format. Please enter time in HH:MM format (e.g., 11:22).")
        return False

#initial setup for every station
def Initialize_station(wait_list, departure_time, start_pos):
    latest_time = datetime.strptime("23:59", "%H:%M").time()

    # Red_line station set up
    redLine_station = []
    for i in range(1, 14):
        temp_station = "R" + str(i)
        temp_data = Line_data.query.filter_by(station=temp_station).first()
        if temp_station in wait_list:
            if temp_station != start_pos:
                temp = Station_Structure(temp_station, departure_time, temp_data.transfer, temp_data.station_type, 1, 0, 0, start_pos, True)
            else:
                temp = Station_Structure(temp_station, departure_time, temp_data.transfer, temp_data.station_type, 0, 0, 0, "", True)

        else:
            temp = Station_Structure(temp_station, latest_time, temp_data.transfer, temp_data.station_type)
        redLine_station.append(temp)

    # Green_line station set up
    greenLine_station = []
    for i in range(1, 15):
        temp_station = "G" + str(i)
        temp_data = Line_data.query.filter_by(station=temp_station).first()
        if temp_station in wait_list:
            if temp_station != start_pos:
                temp = Station_Structure(temp_station, departure_time, temp_data.transfer, temp_data.station_type, 1, 0, 0, start_pos, True)
            else:
                temp = Station_Structure(temp_station, departure_time, temp_data.transfer, temp_data.station_type, 0, 0, 0, "", True)
        else:
            temp = Station_Structure(temp_station, latest_time, temp_data.transfer, temp_data.station_type)
        greenLine_station.append(temp)

    # Orange_line station set up
    orangeLine_station = []
    for i in range(1, 9):
        temp_station = "O" + str(i)
        temp_data = Line_data.query.filter_by(station=temp_station).first()
        if temp_station in wait_list:
            if temp_station != start_pos:
                temp = Station_Structure(temp_station, departure_time, temp_data.transfer, temp_data.station_type, 1, 0, 0, start_pos, True)
            else:
                temp = Station_Structure(temp_station, departure_time, temp_data.transfer, temp_data.station_type, 0, 0, 0, "", True)
        else:
            temp = Station_Structure(temp_station, latest_time, temp_data.transfer, temp_data.station_type)
        orangeLine_station.append(temp)

    # Black_line station set up
    blackLine_station = []
    for i in range(1, 10):
        temp_station = "B" + str(i)
        temp_data = Line_data.query.filter_by(station=temp_station).first()
        if temp_station in wait_list:
            if temp_station != start_pos:
                temp = Station_Structure(temp_station, departure_time, temp_data.transfer, temp_data.station_type, 1, 0, 0, start_pos, True)
            else:
                temp = Station_Structure(temp_station, departure_time, temp_data.transfer, temp_data.station_type, 0, 0, 0, "", True)
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
def Assign_time_to_transfer_station(new_wait_list, station_info, time, previous_station, cost, transfer_time):
    for station in new_wait_list:
        station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(station[0], -1)
        station_number = int(station[1:]) - 1
        station_info[station_line_number][station_number].time = time
        station_info[station_line_number][station_number].previous_station = previous_station
        station_info[station_line_number][station_number].cost = cost
        station_info[station_line_number][station_number].reachable = True
        station_info[station_line_number][station_number].transfer_time = transfer_time + 1

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
    if distance <= 5:
        total_price = 2
    elif distance <= 10:
        total_price = 2 + 0.3*(distance - 5)
        total_price = round(total_price, 2)
    elif distance <= 15:
        total_price = 2 + 0.3 * 5 + 0.2 * (distance - 10)
        total_price = round(total_price, 2)
    else:
        total_price = 2 + 0.3 * 5 + 0.2 * 5 + 0.1 * (distance - 15)
        total_price = round(total_price, 2)
    return round(total_price, 2)

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
    #departure_time = Departure_time_input_text(departure_time)
    departure_time = datetime.strptime(departure_time, "%H:%M").time()
    destination_line = destination[0]
    destination_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(destination[0], -1)
    destination_number = int(destination[1:]) - 1
    #redLine_station, greenLine_station, orangeLine_station, blackLine_station = Initialize_station(departure_time)
    wait_list = Initialize_wait_list(start_pos)
    station_info = Initialize_station(wait_list, departure_time, start_pos)
    checked = 0
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
                temp_cost = Money_cost(station, temp_station)
                temp_transfer_time = station_info[station_line_number][station_number].transfer_time
                if temp_time <= station_info[station_line_number][i].time:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = inbound_train_id
                    station_info[station_line_number][i].reachable = True
                    money_cost = temp_cost + station_info[station_line_number][station_number].cost
                    station_info[station_line_number][i].cost = money_cost
                    station_info[station_line_number][i].transfer_time = temp_transfer_time

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station, money_cost, temp_transfer_time)
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
                temp_cost = Money_cost(station, temp_station)
                temp_transfer_time = station_info[station_line_number][station_number].transfer_time

                if temp_time <= station_info[station_line_number][i].time:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = outbound_train_id
                    station_info[station_line_number][i].reachable = True
                    money_cost = temp_cost + station_info[station_line_number][station_number].cost
                    station_info[station_line_number][i].cost = money_cost
                    station_info[station_line_number][i].transfer_time = temp_transfer_time

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station, money_cost, temp_transfer_time)
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
                temp_cost = Money_cost(station, temp_station)
                temp_transfer_time = station_info[station_line_number][station_number].transfer_time

                if temp_time <= station_info[station_line_number][i].time and temp_inbound_train_id != station_info[station_line_number][i].previous_train_id:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = temp_inbound_train_id
                    station_info[station_line_number][i].reachable = True
                    money_cost = temp_cost + station_info[station_line_number][station_number].cost
                    station_info[station_line_number][i].cost = money_cost
                    station_info[station_line_number][i].transfer_time = temp_transfer_time

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station, money_cost, temp_transfer_time)
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
                temp_cost = Money_cost(station, temp_station)
                temp_transfer_time = station_info[station_line_number][station_number].transfer_time

                if temp_time <= station_info[station_line_number][i].time and temp_outbound_train_id != station_info[station_line_number][i].previous_train_id:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = temp_outbound_train_id
                    station_info[station_line_number][i].reachable = True
                    money_cost = temp_cost + station_info[station_line_number][station_number].cost
                    station_info[station_line_number][i].cost = money_cost
                    station_info[station_line_number][i].transfer_time = temp_transfer_time

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station, money_cost, temp_transfer_time)
                        wait_list = new_wait_list + wait_list
            if destination_line == station_line:

                if station_info[destination_line_number][destination_number].type == 1 and checked == 0:
                    new_wait_list = Find_closest_rapid_station(destination, station_info)
                    wait_list_set = set(wait_list)
                    new_wait_list_set = set(new_wait_list)
                    combined_set = wait_list_set.union(new_wait_list_set)
                    wait_list = list(combined_set)
                    checked = 1

            # print(station_info[station_line_number][station_number].type)
            if station_info[station_line_number][station_number].type == 1:
                new_wait_list = Find_closest_rapid_station(station, station_info)
                wait_list = wait_list + new_wait_list


    wait_list = Initialize_wait_list(start_pos)
    for data in wait_list:
        data_line = data[0]
        data_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(data[0], -1)
        data_number = int(data[1:]) - 1
        station_info[data_line_number][data_number].cost = 0
    solution = []  # transfer_or_not, start_pos of this step, destination of this step, departure_time of this step, arrival_time of this step, train_id, type of this train(rapid or local), cost for this step
    destination_reachable = True
    total_transfer_time = 0
    total_money_spent = station_info[destination_line_number][destination_number].cost
    total_step = 0
    initial_departure_time = departure_time
    final_arrival_time = station_info[destination_line_number][destination_number].time
    current_station = destination
    while current_station != start_pos:
        current_station_line = current_station[0]
        current_station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(current_station[0], -1)
        current_station_number = int(current_station[1:]) - 1
        if station_info[current_station_line_number][current_station_number].reachable == False:
            destination_reachable = False
            break
        temp_station = station_info[current_station_line_number][current_station_number].previous_station
        temp_station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(temp_station[0], -1)
        temp_station_number = int(temp_station[1:]) - 1
        solution_data = [None] * 9
        if Line_data.query.filter_by(station=temp_station).first().transfer == Line_data.query.filter_by(
                station=current_station).first().transfer and Line_data.query.filter_by(
            station=current_station).first().transfer > 0:
            total_transfer_time += 1

            solution_data[0] = 1
            solution_data[1] = temp_station
            solution_data[2] = current_station

        else:
            solution_data[0] = 0
            solution_data[1] = temp_station
            solution_data[2] = current_station

            solution_data[4] = station_info[current_station_line_number][current_station_number].time
            solution_data[5] = station_info[current_station_line_number][current_station_number].previous_train_id
            solution_data[6] = station_info[current_station_line_number][current_station_number].type
            solution_data[7] = str(station_info[current_station_line_number][current_station_number].cost - station_info[temp_station_line_number][temp_station_number].cost)

            train_direction = int(str(solution_data[5])[3])
            if train_direction == 0:
                solution_data[3] = line_outbound_data_mapping[current_station_line].query.filter_by(
                    station=temp_station,
                    train_id=solution_data[5]).first().departure_time
            else:
                solution_data[3] = line_inbound_data_mapping[current_station_line].query.filter_by(
                    station=temp_station, train_id=solution_data[5]).first().departure_time
            start_time = datetime.combine(datetime.min, solution_data[3])
            end_time = datetime.combine(datetime.min, solution_data[4])
            time_difference = start_time - end_time
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes = remainder // 60
            hours = 23 - hours
            minutes = 60 - minutes
            solution_data[8] = f"{hours}h{minutes}min"
            solution_data[5] = str(solution_data[5])
            solution_data[4] = solution_data[4].strftime("%H:%M")
            solution_data[3] = solution_data[3].strftime("%H:%M")
            if solution_data[6] == 11:
                solution_data[6] = "Rapid"
            else:
                solution_data[6] = "Local"
        solution.append(solution_data)

        total_step += 1
        current_station = temp_station
    solution = solution[::-1]
    return destination_reachable, total_step, solution, total_transfer_time, total_money_spent, initial_departure_time, final_arrival_time

        # if station_line == "R":

def Less_money_algorithm(start_pos, destination, departure_time):
    #departure_time = Departure_time_input_text(departure_time)
    departure_time = datetime.strptime(departure_time, "%H:%M").time()

    destination_line = destination[0]
    destination_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(destination[0], -1)
    destination_number = int(destination[1:]) - 1
    wait_list = Initialize_wait_list(start_pos)
    station_info = Initialize_station(wait_list, departure_time, start_pos)
    checked = 0
    while len(wait_list) > 0:
        station = wait_list.pop()
        station_line = station[0]
        station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(station[0], -1)
        station_number = int(station[1:]) - 1
        if(station_line == "G" or station_line == "B"):
            temp_inbound_data = line_inbound_data_mapping[station_line].query.filter_by(station=station).filter(line_inbound_data_mapping[station_line].departure_time >= station_info[station_line_number][station_number].time).first()
            temp_outbound_data = line_outbound_data_mapping[station_line].query.filter_by(station=station).filter(line_outbound_data_mapping[station_line].departure_time >= station_info[station_line_number][station_number].time).first()
            # station_distance = Line_data.query.filter_by(station=station).first().distance
            for i in range(station_number - 1, -1, -1):
            # for i in range(station_number):
                temp_station = station_line + str(i + 1)

                if temp_inbound_data == None:
                    break

                inbound_train_id = temp_inbound_data.train_id
                temp_time = line_inbound_data_mapping[station_line].query.filter_by(station=temp_station).filter_by(
                    train_id=inbound_train_id).first().arrival_time
                # temp_station_distance = Line_data.query.filter_by(station=temp_station).first().distance
                # distance_difference = station_distance - temp_station_distance
                temp_cost = Money_cost(station, temp_station)
                temp_transfer_time = station_info[station_line_number][station_number].transfer_time

                if station_info[station_line_number][i].cost == 0 or station_info[station_line_number][i].cost > temp_cost + station_info[station_line_number][station_number].cost: #temp_time <= station_info[station_line_number][i].time:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = inbound_train_id
                    station_info[station_line_number][i].reachable = True
                    money_cost = temp_cost + station_info[station_line_number][station_number].cost
                    station_info[station_line_number][i].cost = money_cost
                    station_info[station_line_number][i].transfer_time = temp_transfer_time

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station, money_cost, temp_transfer_time)
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
                temp_cost = Money_cost(station, temp_station)
                temp_transfer_time = station_info[station_line_number][station_number].transfer_time

                if station_info[station_line_number][i].cost == 0 or station_info[station_line_number][i].cost > temp_cost + station_info[station_line_number][station_number].cost:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = outbound_train_id
                    station_info[station_line_number][i].reachable = True
                    money_cost = temp_cost + station_info[station_line_number][station_number].cost
                    station_info[station_line_number][i].cost = money_cost
                    station_info[station_line_number][i].transfer_time = temp_transfer_time

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station, money_cost, temp_transfer_time)
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

                temp_cost = Money_cost(station, temp_station)
                temp_transfer_time = station_info[station_line_number][station_number].transfer_time

                if station_info[station_line_number][i].cost == 0 or station_info[station_line_number][i].cost > temp_cost + station_info[station_line_number][station_number].cost:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = temp_inbound_train_id
                    station_info[station_line_number][i].reachable = True
                    money_cost = temp_cost + station_info[station_line_number][station_number].cost
                    station_info[station_line_number][i].cost = money_cost
                    station_info[station_line_number][i].transfer_time = temp_transfer_time

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station, money_cost, temp_transfer_time)
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
                temp_cost = Money_cost(station, temp_station)
                temp_transfer_time = station_info[station_line_number][station_number].transfer_time

                if station_info[station_line_number][i].cost == 0 or station_info[station_line_number][i].cost > temp_cost + station_info[station_line_number][station_number].cost:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = temp_outbound_train_id
                    station_info[station_line_number][i].reachable = True
                    money_cost = temp_cost + station_info[station_line_number][station_number].cost
                    station_info[station_line_number][i].cost = money_cost
                    station_info[station_line_number][i].transfer_time = temp_transfer_time

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time, temp_station, money_cost, temp_transfer_time)
                        wait_list = new_wait_list + wait_list
    wait_list = Initialize_wait_list(start_pos)
    for data in wait_list:
        data_line = data[0]
        data_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(data[0], -1)
        data_number = int(data[1:]) - 1
        station_info[data_line_number][data_number].cost = 0
    solution = []  # transfer_or_not, start_pos of this step, destination of this step, departure_time of this step, arrival_time of this step, train_id, type of this train(rapid or local), cost for this step
    destination_reachable = True
    total_transfer_time = 0
    total_money_spent = station_info[destination_line_number][destination_number].cost
    total_step = 0
    initial_departure_time = departure_time
    final_arrival_time = station_info[destination_line_number][destination_number].time
    current_station = destination
    while current_station != start_pos:
        current_station_line = current_station[0]
        current_station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(current_station[0], -1)
        current_station_number = int(current_station[1:]) - 1
        if station_info[current_station_line_number][current_station_number].reachable == False:
            destination_reachable = False
            break
        temp_station = station_info[current_station_line_number][current_station_number].previous_station
        temp_station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(temp_station[0], -1)
        temp_station_number = int(temp_station[1:]) - 1
        solution_data = [None] * 9
        if Line_data.query.filter_by(station=temp_station).first().transfer == Line_data.query.filter_by(
                station=current_station).first().transfer and Line_data.query.filter_by(
            station=current_station).first().transfer > 0:
            total_transfer_time += 1

            solution_data[0] = 1
            solution_data[1] = temp_station
            solution_data[2] = current_station

        else:
            solution_data[0] = 0
            solution_data[1] = temp_station
            solution_data[2] = current_station

            solution_data[4] = station_info[current_station_line_number][current_station_number].time.strftime("%H:%M")
            solution_data[5] = station_info[current_station_line_number][current_station_number].previous_train_id
            solution_data[6] = station_info[current_station_line_number][current_station_number].type
            solution_data[7] = str(station_info[current_station_line_number][current_station_number].cost - station_info[temp_station_line_number][temp_station_number].cost)

            train_direction = int(str(solution_data[5])[3])
            if train_direction == 0:
                solution_data[3] = line_outbound_data_mapping[current_station_line].query.filter_by(
                    station=temp_station,
                    train_id=solution_data[5]).first().departure_time
            else:
                solution_data[3] = line_inbound_data_mapping[current_station_line].query.filter_by(
                    station=temp_station, train_id=solution_data[5]).first().departure_time
            start_time = datetime.combine(datetime.min, solution_data[3])
            end_time_str = solution_data[4]
            end_time = datetime.combine(datetime.min, datetime.strptime(end_time_str, "%H:%M").time())
            time_difference = start_time - end_time
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes = remainder // 60
            hours = 23 - hours
            minutes = 60 - minutes
            solution_data[8] = f"{hours}h{minutes}min"
            solution_data[5] = str(solution_data[5])
            #solution_data[4] = solution_data[4].strftime("%H:%M")
            solution_data[3] = solution_data[3].strftime("%H:%M")
            if solution_data[6] == 11:
                solution_data[6] = "Rapid"
            else:
                solution_data[6] = "Local"
        solution.append(solution_data)

        total_step += 1
        current_station = temp_station
    solution = solution[::-1]
    return destination_reachable, total_step, solution, total_transfer_time, total_money_spent, initial_departure_time, final_arrival_time


def Less_transfer_time_algorithm(start_pos, destination, departure_time):
    departure_time = datetime.strptime(departure_time, "%H:%M").time()
    destination_line = destination[0]
    destination_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(destination[0], -1)
    destination_number = int(destination[1:]) - 1
    wait_list = Initialize_wait_list(start_pos)
    station_info = Initialize_station(wait_list, departure_time, start_pos)
    checked = 0
    while len(wait_list) > 0:
        station = wait_list.pop()
        station_line = station[0]
        station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(station[0], -1)
        station_number = int(station[1:]) - 1
        if (station_line == "G" or station_line == "B"):
            temp_inbound_data = line_inbound_data_mapping[station_line].query.filter_by(station=station).filter(
                line_inbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            temp_outbound_data = line_outbound_data_mapping[station_line].query.filter_by(station=station).filter(
                line_outbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            # station_distance = Line_data.query.filter_by(station=station).first().distance
            for i in range(station_number - 1, -1, -1):
                # for i in range(station_number):
                temp_station = station_line + str(i + 1)

                if temp_inbound_data == None:
                    break

                inbound_train_id = temp_inbound_data.train_id
                temp_time = line_inbound_data_mapping[station_line].query.filter_by(station=temp_station).filter_by(
                    train_id=inbound_train_id).first().arrival_time
                # temp_station_distance = Line_data.query.filter_by(station=temp_station).first().distance
                # distance_difference = station_distance - temp_station_distance
                temp_cost = Money_cost(station, temp_station)
                temp_transfer_time = station_info[station_line_number][station_number].transfer_time

                if station_info[station_line_number][i].transfer_time > station_info[station_line_number][station_number].transfer_time:
                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = inbound_train_id
                    station_info[station_line_number][i].reachable = True
                    money_cost = temp_cost + station_info[station_line_number][station_number].cost
                    station_info[station_line_number][i].cost = money_cost
                    station_info[station_line_number][i].transfer_time = temp_transfer_time

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time,
                                                                       temp_station, money_cost, temp_transfer_time)
                        wait_list = new_wait_list + wait_list

                # print(station_info[station_line_number][i].time)
            upperbound = 9 if station_line == "B" else 14
            for i in range(station_number + 1, upperbound):
                temp_station = station_line + str(i + 1)
                if temp_outbound_data == None:
                    break
                outbound_train_id = temp_outbound_data.train_id
                temp_time = line_outbound_data_mapping[station_line].query.filter_by(
                    station=temp_station).filter_by(train_id=outbound_train_id).first().arrival_time
                temp_cost = Money_cost(station, temp_station)
                temp_transfer_time = station_info[station_line_number][station_number].transfer_time

                if station_info[station_line_number][i].transfer_time > station_info[station_line_number][station_number].transfer_time:

                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = outbound_train_id
                    station_info[station_line_number][i].reachable = True
                    money_cost = temp_cost + station_info[station_line_number][station_number].cost
                    station_info[station_line_number][i].cost = money_cost
                    station_info[station_line_number][i].transfer_time = temp_transfer_time

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time,
                                                                       temp_station, money_cost, temp_transfer_time)
                        wait_list = new_wait_list + wait_list
        else:  # station_line == "R" or "O", lines have rapid train service
            temp_inbound_local_data = line_inbound_data_mapping[station_line].query.filter_by(station=station,
                                                                                              train_type="Local").filter(
                line_inbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            temp_outbound_local_data = line_outbound_data_mapping[station_line].query.filter_by(station=station,
                                                                                                train_type="Local").filter(
                line_outbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            temp_inbound_rapid_data = line_inbound_data_mapping[station_line].query.filter_by(station=station,
                                                                                              train_type="Rapid").filter(
                line_inbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            temp_outbound_rapid_data = line_outbound_data_mapping[station_line].query.filter_by(station=station,
                                                                                                train_type="Rapid").filter(
                line_outbound_data_mapping[station_line].departure_time >= station_info[station_line_number][
                    station_number].time).first()
            for i in range(station_number):
                temp_station = station_line + str(i + 1)
                if temp_inbound_local_data == None:
                    break

                inbound_local_train_id = temp_inbound_local_data.train_id
                temp_local_time = line_inbound_data_mapping[station_line].query.filter_by(station=temp_station,
                                                                                          train_id=inbound_local_train_id).first().arrival_time
                temp_time = temp_local_time
                temp_inbound_train_id = inbound_local_train_id
                if temp_inbound_rapid_data != None and station_info[station_line_number][i].type > 1:
                    inbound_rapid_train_id = temp_inbound_rapid_data.train_id
                    temp_rapid_time = line_inbound_data_mapping[station_line].query.filter_by(station=temp_station,
                                                                                              train_id=inbound_rapid_train_id).first().arrival_time
                    if temp_rapid_time < temp_time:
                        temp_time = temp_rapid_time
                        temp_inbound_train_id = inbound_rapid_train_id

                temp_cost = Money_cost(station, temp_station)
                temp_transfer_time = station_info[station_line_number][station_number].transfer_time

                if station_info[station_line_number][i].transfer_time > station_info[station_line_number][station_number].transfer_time:


                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = temp_inbound_train_id
                    station_info[station_line_number][i].reachable = True
                    money_cost = temp_cost + station_info[station_line_number][station_number].cost
                    station_info[station_line_number][i].cost = money_cost
                    station_info[station_line_number][i].transfer_time = temp_transfer_time

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time,
                                                                       temp_station, money_cost, temp_transfer_time)
                        wait_list = new_wait_list + wait_list
                        # print(wait_list)
            upperbound = 13 if station_line == "R" else 8
            for i in range(station_number + 1, upperbound):
                temp_station = station_line + str(i + 1)
                if temp_outbound_local_data == None:
                    break

                outbound_local_train_id = temp_outbound_local_data.train_id
                temp_local_time = line_outbound_data_mapping[station_line].query.filter_by(station=temp_station,
                                                                                           train_id=outbound_local_train_id).first().arrival_time
                temp_time = temp_local_time
                temp_outbound_train_id = outbound_local_train_id
                if temp_outbound_rapid_data != None and station_info[station_line_number][i].type > 1:
                    outbound_rapid_train_id = temp_outbound_rapid_data.train_id
                    temp_rapid_time = line_outbound_data_mapping[station_line].query.filter_by(station=temp_station,
                                                                                               train_id=outbound_rapid_train_id).first().arrival_time
                    if temp_rapid_time < temp_time:
                        temp_time = temp_rapid_time
                        temp_outbound_train_id = outbound_rapid_train_id
                temp_cost = Money_cost(station, temp_station)
                temp_transfer_time = station_info[station_line_number][station_number].transfer_time

                if station_info[station_line_number][i].transfer_time > station_info[station_line_number][station_number].transfer_time:


                    station_info[station_line_number][i].time = temp_time
                    station_info[station_line_number][i].previous_station = station
                    station_info[station_line_number][i].previous_train_id = temp_outbound_train_id
                    station_info[station_line_number][i].reachable = True
                    money_cost = temp_cost + station_info[station_line_number][station_number].cost
                    station_info[station_line_number][i].cost = money_cost
                    station_info[station_line_number][i].transfer_time = temp_transfer_time

                    if station_info[station_line_number][i].transfer > 0:
                        new_wait_list = Initialize_wait_list(temp_station)
                        new_wait_list.remove(temp_station)
                        station_info = Assign_time_to_transfer_station(new_wait_list, station_info, temp_time,
                                                                       temp_station, money_cost, temp_transfer_time)
                        wait_list = new_wait_list + wait_list
    wait_list = Initialize_wait_list(start_pos)
    for data in wait_list:
        data_line = data[0]
        data_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(data[0], -1)
        data_number = int(data[1:]) - 1
        station_info[data_line_number][data_number].cost = 0
    solution = []  # transfer_or_not, start_pos of this step, destination of this step, departure_time of this step, arrival_time of this step, train_id, type of this train(rapid or local), cost for this step
    destination_reachable = True
    total_transfer_time = 0
    total_money_spent = station_info[destination_line_number][destination_number].cost
    total_step = 0
    initial_departure_time = departure_time
    final_arrival_time = station_info[destination_line_number][destination_number].time
    current_station = destination
    while current_station != start_pos:
        current_station_line = current_station[0]
        current_station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(current_station[0], -1)
        current_station_number = int(current_station[1:]) - 1
        if station_info[current_station_line_number][current_station_number].reachable == False:
            destination_reachable = False
            break
        temp_station = station_info[current_station_line_number][current_station_number].previous_station
        temp_station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(temp_station[0], -1)
        temp_station_number = int(temp_station[1:]) - 1
        solution_data = [None] * 9
        if Line_data.query.filter_by(station=temp_station).first().transfer == Line_data.query.filter_by(
                station=current_station).first().transfer and Line_data.query.filter_by(
            station=current_station).first().transfer > 0:
            total_transfer_time += 1

            solution_data[0] = 1
            solution_data[1] = temp_station
            solution_data[2] = current_station

        else:
            solution_data[0] = 0
            solution_data[1] = temp_station
            solution_data[2] = current_station

            solution_data[4] = station_info[current_station_line_number][current_station_number].time.strftime("%H:%M")
            solution_data[5] = station_info[current_station_line_number][current_station_number].previous_train_id
            solution_data[6] = station_info[current_station_line_number][current_station_number].type
            solution_data[7] = str(station_info[current_station_line_number][current_station_number].cost - station_info[temp_station_line_number][temp_station_number].cost)

            train_direction = int(str(solution_data[5])[3])
            if train_direction == 0:
                solution_data[3] = line_outbound_data_mapping[current_station_line].query.filter_by(
                    station=temp_station,
                    train_id=solution_data[5]).first().departure_time
            else:
                solution_data[3] = line_inbound_data_mapping[current_station_line].query.filter_by(
                    station=temp_station, train_id=solution_data[5]).first().departure_time
            start_time = datetime.combine(datetime.min, solution_data[3])
            end_time_str = solution_data[4]
            end_time = datetime.combine(datetime.min, datetime.strptime(end_time_str, "%H:%M").time())
            time_difference = start_time - end_time
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes = remainder // 60
            hours = 23 - hours
            minutes = 60 - minutes
            solution_data[8] = f"{hours}h{minutes}min"
            solution_data[5] = str(solution_data[5])
            #solution_data[4] = solution_data[4].strftime("%H:%M")
            solution_data[3] = solution_data[3].strftime("%H:%M")
            if solution_data[6] == 11:
                solution_data[6] = "Rapid"
            else:
                solution_data[6] = "Local"
        solution.append(solution_data)

        total_step += 1
        current_station = temp_station
    solution = solution[::-1]
    return destination_reachable, total_step, solution, total_transfer_time, total_money_spent, initial_departure_time, final_arrival_time

"""
def main():
    with app.app_context():
        start_pos = input("Start position:")
        if Start_pos_input_test(start_pos) == False:
            print("start position input error")
        destination = input("Destination:")

        if Destination_input_test(start_pos, destination) == False:
            print("destination input error")
        criteria = Criteration_input_test()
        time_input = input("Enter departure time (HH:MM): ")
        departure_time = Departure_time_input_text(time_input)

        if int(criteria) == 1:
            destination_reachable, total_step, solution, total_transfer_time, total_money_spent, initial_departure_time,\
            final_arrival_time = Less_travel_time_algorithm(start_pos, destination, departure_time)
        elif int(criteria) == 2:
            destination_reachable, total_step, solution, total_transfer_time, total_money_spent, initial_departure_time,\
            final_arrival_time = Less_money_algorithm(start_pos, destination, departure_time)
        else:
            destination_reachable, total_step, solution, total_transfer_time, total_money_spent, initial_departure_time,\
            final_arrival_time = Less_transfer_time_algorithm(start_pos, destination, departure_time)
        if destination_reachable == False:
            print("No Available Route!")
        else:
            for i in range(total_step):
                print("Step " + str(i + 1) + ":")
                if solution[i][0] == 1:
                    print("Transfer here!")
                    print("From: " + solution[i][1])
                    print("To: " + solution[i][2])
                else:
                    print("Take train!")
                    print("From: " + solution[i][1] + "; Departure time: " + solution[i][3])
                    print("Train_id: " + solution[i][5] + "; Train_type: " + solution[i][6])
                    print("Cost in this step: " + solution[i][7] + "; Travel time in this train: " + solution[i][8])
                    print("To: " + solution[i][2] + "; Arrival time: " + solution[i][4])
                print("")
        print("")
        print("Total step(s):" + str(total_step))
        print("Total transfer time(s):" + str(total_transfer_time))
        print("Total Money Spent:" + str(total_money_spent))
        print("Initial departure time:" + str(initial_departure_time))
        print("Final arrival time:" + str(final_arrival_time))
        # if int(criteria) == 1:
        #     station_info = Less_travel_time_algorithm(start_pos, destination, departure_time)
        #     current_station = destination
        #     solution = [[] for _ in range(6)]
        #     print("\n\n\n")
        #     while current_station != start_pos:
        #         current_station_line = current_station[0]
        #         current_station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(current_station[0], -1)
        #         current_station_number = int(current_station[1:]) - 1
        #         if station_info[current_station_line_number][current_station_number].reachable == False:
        #             print("No Available Route!")#在返回的时候只要发现就把transfer的值设置为2，表明解不存在
        #             break
        #         temp_station = station_info[current_station_line_number][current_station_number].previous_station
        #         if Line_data.query.filter_by(station=temp_station).first().transfer == Line_data.query.filter_by(station=current_station).first().transfer and Line_data.query.filter_by(station=current_station).first().transfer > 0:
        #             print("transfer here")
        #             print(current_station)
        #             print(temp_station)
        #         else:
        #             print(current_station)
        #             print(station_info[current_station_line_number][current_station_number].previous_train_id)
        #             print(station_info[current_station_line_number][current_station_number].type)
        #             print(station_info[current_station_line_number][current_station_number].time)
        #             print(station_info[current_station_line_number][current_station_number].previous_station)
        #             print(station_info[current_station_line_number][current_station_number].cost)
        #             print(station_info[current_station_line_number][current_station_number].transfer_time)
        #
        #         current_station = temp_station
        #         print("\n\n\n")
        #         #增加一个费用计算
        # elif int(criteria) == 2:
        #     station_info = Less_money_algorithm(start_pos, destination, departure_time)
        #     current_station = destination
        #     solution = [[] for _ in range(6)]
        #     print("\n\n\n")
        #     while current_station != start_pos:
        #         current_station_line = current_station[0]
        #         current_station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(current_station[0], -1)
        #         current_station_number = int(current_station[1:]) - 1
        #         if station_info[current_station_line_number][current_station_number].reachable == False:
        #             print("No Available Route!")  # 在返回的时候只要发现就把transfer的值设置为2，表明解不存在
        #             break
        #         temp_station = station_info[current_station_line_number][current_station_number].previous_station
        #         if Line_data.query.filter_by(station=temp_station).first().transfer == Line_data.query.filter_by(
        #                 station=current_station).first().transfer and Line_data.query.filter_by(
        #                 station=current_station).first().transfer > 0:
        #             print("transfer here")
        #             print(current_station)
        #             print(temp_station)
        #         else:
        #             print(current_station)
        #             print(station_info[current_station_line_number][current_station_number].previous_train_id)
        #             print(station_info[current_station_line_number][current_station_number].type)
        #             print(station_info[current_station_line_number][current_station_number].time)
        #             print(station_info[current_station_line_number][current_station_number].previous_station)
        #             print(station_info[current_station_line_number][current_station_number].cost)
        #             print(station_info[current_station_line_number][current_station_number].transfer_time)
        #
        #         current_station = temp_station
        #         print("\n\n\n")
        #         #输出cost的时候转换为字符串
        # else:
        #     station_info = Less_transfer_time_algorithm(start_pos, destination, departure_time)
        #     current_station = destination
        #     solution = [[] for _ in range(6)]
        #     print("\n\n\n")
        #     while current_station != start_pos:
        #         current_station_line = current_station[0]
        #         current_station_line_number = {'R': 0, 'G': 1, 'O': 2, 'B': 3}.get(current_station[0], -1)
        #         current_station_number = int(current_station[1:]) - 1
        #         if station_info[current_station_line_number][current_station_number].reachable == False:
        #             print("No Available Route!")  # 在返回的时候只要发现就把transfer的值设置为2，表明解不存在
        #             break
        #         temp_station = station_info[current_station_line_number][current_station_number].previous_station
        #         if Line_data.query.filter_by(station=temp_station).first().transfer == Line_data.query.filter_by(
        #                 station=current_station).first().transfer and Line_data.query.filter_by(
        #             station=current_station).first().transfer > 0:
        #             print("transfer here")
        #             print(current_station)
        #             print(temp_station)
        #         else:
        #             print(current_station)
        #             print(station_info[current_station_line_number][current_station_number].previous_train_id)
        #             print(station_info[current_station_line_number][current_station_number].type)
        #             print(station_info[current_station_line_number][current_station_number].time)
        #             print(station_info[current_station_line_number][current_station_number].previous_station)
        #             print(station_info[current_station_line_number][current_station_number].cost)
        #             print(station_info[current_station_line_number][current_station_number].transfer_time)
        #
        #         current_station = temp_station
        #         print("\n\n\n")
                # 输出cost的时候转换为字符串
main()

"""