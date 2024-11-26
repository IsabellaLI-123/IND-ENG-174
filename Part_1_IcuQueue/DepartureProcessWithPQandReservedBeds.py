import heapq

from ArrivalProcess import simulate_arrival_process, generate_length_of_stays

arrival_times, severity_level_list = simulate_arrival_process()
length_of_stays = generate_length_of_stays(severity_level_list)
capacity = 100  # Maximum ICU capacity
reserved_capacity = 30

def simulate_departure_process_priority_with_reserved(arrival_times=arrival_times, severity_level_list=severity_level_list, length_of_stays=length_of_stays, capacity=capacity, reserved_capacity=reserved_capacity):
    regular_capacity = capacity - reserved_capacity  # Regular beds
    current_regular_ICU_departures = []  # Priority queue for regular bed departures
    current_reserved_ICU_departures = []  # Priority queue for reserved bed departures
    
    departure_times = [None] * len(arrival_times)
    start_times = [None] * len(arrival_times)
    waiting_queue = []  # Priority queue for waiting patients
    temporary_regular_departure_time_list = []
    temporary_reserved_departure_time_list = []
    for i in range(len(arrival_times)):
        arrival_time = arrival_times[i]
        severity = severity_level_list[i]
        length_of_stay = length_of_stays[i] * 24  # Convert days to hours
        
        while current_regular_ICU_departures and current_regular_ICU_departures[0][0] <= arrival_time:
            previous_departure_time, departure_index = heapq.heappop(current_regular_ICU_departures)
            departure_times[departure_index] = previous_departure_time
            temporary_regular_departure_time_list.append(previous_departure_time)

        while current_reserved_ICU_departures and current_reserved_ICU_departures[0][0] <= arrival_time:
            previous_departure_time, departure_index = heapq.heappop(current_reserved_ICU_departures)
            departure_times[departure_index] = previous_departure_time
            temporary_reserved_departure_time_list.append(previous_departure_time)

 
        temp_waiting_queue = []
        while waiting_queue:
            _, waiting_severity, waiting_index = heapq.heappop(waiting_queue)
            wait_length_of_stay = length_of_stays[waiting_index] * 24

            # Assign to regular bed
            if len(current_regular_ICU_departures) < regular_capacity:
                earliest_available_time = temporary_regular_departure_time_list[0] 
                start_time = earliest_available_time
                start_times[waiting_index] = start_time
                departure_time = start_time + wait_length_of_stay
                departure_times[waiting_index] = departure_time
                heapq.heappush(current_regular_ICU_departures, (departure_time, waiting_index))
                temporary_regular_departure_time_list = temporary_regular_departure_time_list[1:]

            # Assign to reserved bed
            elif waiting_severity == 3 and len(current_reserved_ICU_departures) < reserved_capacity:
                earliest_available_time = temporary_reserved_departure_time_list[0]
                start_time = earliest_available_time
                start_times[waiting_index] = start_time
                departure_time = start_time + wait_length_of_stay
                departure_times[waiting_index] = departure_time
                heapq.heappush(current_reserved_ICU_departures, (departure_time, waiting_index))
                temporary_reserved_departure_time_list = temporary_reserved_departure_time_list[1:]
        
            else:
                temp_waiting_queue.append((waiting_severity, waiting_severity, waiting_index))

        # Restore unprocessed patients to the waiting queue
        for item in temp_waiting_queue:
            heapq.heappush(waiting_queue, item)

        # Assign the current patient
        if len(current_regular_ICU_departures) < regular_capacity:
            start_time = arrival_time
            start_times[i] = start_time
            departure_time = start_time + length_of_stay
            departure_times[i] = departure_time
            heapq.heappush(current_regular_ICU_departures, (departure_time, i))
            temporary_regular_departure_time_list = temporary_regular_departure_time_list[1:]

            

        elif severity == 3 and len(current_reserved_ICU_departures) < reserved_capacity:
            start_time = arrival_time
            start_times[i] = start_time
            departure_time = start_time + length_of_stay
            departure_times[i] = departure_time
            heapq.heappush(current_reserved_ICU_departures, (departure_time, i))
            temporary_reserved_departure_time_list = temporary_reserved_departure_time_list[1:]


        else:
            heapq.heappush(waiting_queue, (-severity, severity, i))

    # Process remaining patients in the waiting queue
    current_time = arrival_times[-1]

    while waiting_queue:
        # Free up regular and reserved beds
        
        while current_regular_ICU_departures and current_regular_ICU_departures[0][0] <= current_time:
            previous_departure_time, departure_index = heapq.heappop(current_regular_ICU_departures)
            departure_times[departure_index] = previous_departure_time
            temporary_regular_departure_time_list.append(previous_departure_time)
            

        while current_reserved_ICU_departures and current_reserved_ICU_departures[0][0] <= current_time:
            previous_departure_time, departure_index = heapq.heappop(current_reserved_ICU_departures)
            departure_times[departure_index] = previous_departure_time
            temporary_reserved_departure_time_list.append(previous_departure_time)
        # Assign waiting patients
        _, waiting_severity, waiting_index = heapq.heappop(waiting_queue)
        wait_length_of_stay = length_of_stays[waiting_index] * 24

        if len(current_regular_ICU_departures) < regular_capacity:
            start_time = temporary_regular_departure_time_list[0]
            print(start_time)
            start_times[waiting_index] = start_time
            departure_time = start_time + wait_length_of_stay
            departure_times[waiting_index] = departure_time
            heapq.heappush(current_regular_ICU_departures, (departure_time, waiting_index))
            temporary_regular_departure_time_list = temporary_regular_departure_time_list[1:]
        elif waiting_severity == 3 and len(current_reserved_ICU_departures) < reserved_capacity:
            # Assign to a reserved bed
            start_time = current_time
            start_times[waiting_index] = start_time
            departure_time = start_time + wait_length_of_stay
            departure_times[waiting_index] = departure_time
            heapq.heappush(current_reserved_ICU_departures, (departure_time, waiting_index))
            temporary_reserved_departure_time_list = temporary_reserved_departure_time_list[1:]

    return departure_times, start_times

departure_times, start_times = simulate_departure_process_priority_with_reserved()

# print(start_times)
def calculate_waiting_times(arrival_times = arrival_times, start_times = start_times):
    waiting_times = []

    for i in range(len(arrival_times)):
        waiting_time = start_times[i] - arrival_times[i]
        waiting_times.append(waiting_time)

    return waiting_times

waiting_times = calculate_waiting_times()

def simultaneously_return(arrival_times=arrival_times, severity_level_list=severity_level_list,
                          start_times=start_times, departure_times=departure_times, waiting_times=waiting_times):
    return arrival_times, severity_level_list, start_times, departure_times, waiting_times


