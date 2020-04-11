from math import floor

def SJF_Preemptive(processes_count, arrival_times, burst_times):

    '''
    this function is an implementation of preemptive shortest job first algorithm
    it's also called shortest remaining time first algorithm
    this function receives any positive number of process with the same number of arrival times and burst times
    this function handles any number of idle cycles between process correctly
    this function returns a tuple containing the average waiting time and a list of starting and ending times for each process
    note that this Algorithm returns the min Average waiting time between all CPU scheduling algorithms
    very important : this function does not handle starvation problem
    '''
    #the values in following 2 dictionaries are just for initialization and will be changed according to user inputs
    one_process_dictionary = {
        'Process ID' : 0,
        'Arrival time' : 0,
        'Burst time' : 0,
        'Waiting time' : 0,
        'Turnaround time' : 0,
        'Completion time' : 0
    }
    special_dictionary = {
        'Start time 1':-1,
        'End time 1':0
    }
    all_process_list = [one_process_dictionary] * processes_count
    special_list = [special_dictionary] * processes_count
    remaining_time_list = []  #since this Algorithm is preemptive so we must know remaining time of each process before context switching
    #data entry

    for i in range(processes_count):
        if i > 0:
            all_process_list[i] = all_process_list[i-1].copy()
            special_list[i] = special_list[i-1].copy()
        all_process_list[i]['Process ID'] = i+1
        all_process_list[i]['Arrival time'] = arrival_times[i]
        all_process_list[i]['Burst time'] = burst_times[i]
        remaining_time_list.append(burst_times[i])

    #the process with min arrival time must be the first one to start
    #if there are multiple process with min arrival time , the one with min burst time must be the first one to start
    running_process_index = 0  #initially we assume process 1 has min arrival time until we found something else
    for i in range(processes_count):
        if all_process_list[running_process_index]['Arrival time'] > all_process_list[i]['Arrival time']:
            running_process_index = i
        elif all_process_list[running_process_index]['Arrival time'] == all_process_list[i]['Arrival time']:
            if all_process_list[running_process_index]['Burst time'] > all_process_list[i]['Burst time']:
                running_process_index = i
    #after previous loop we guarantee that running process index is the index of process that must start
    #notice that index start from 0 while process ID start from 1
    min_arrival_time = all_process_list[running_process_index]['Arrival time']
    special_list[running_process_index]['Start time 1'] = min_arrival_time
    i = min_arrival_time
    while True:
        remaining_time_list[running_process_index] -= 1
        previous_running_index = running_process_index
        escape = True #we always want to go out the loop unless there is any process with positive remaining time
        skip = True #any cycle is considered an idle cycle unless we find any process which has arrived just now or earlier with +ve remaining time
        i += 1
        for h in range(processes_count):
            if all_process_list[h]['Arrival time'] <= i and remaining_time_list[h] > 0:
                skip = False
                break


        #we must check after each unit time which process to be run

        if remaining_time_list[running_process_index] <= 0: #if a process has finished its work we must move into anpther one
            for k in range(processes_count):
                if remaining_time_list[k] > 0:
                    escape = False
                    if all_process_list[k]['Arrival time'] <= i:
                        running_process_index = k
                        break
            if escape:
                break

        if skip:
            continue

        for j in range(processes_count):
            if (all_process_list[j]['Arrival time'] <= i and remaining_time_list[j] > 0):
                if remaining_time_list[j] < remaining_time_list[running_process_index]:
                    running_process_index = j
                elif (remaining_time_list[j] == remaining_time_list[running_process_index] and
                    all_process_list[j]['Arrival time'] < all_process_list[running_process_index]['Arrival time']):
                    running_process_index = j




        if previous_running_index != running_process_index:
            if special_list[running_process_index]['Start time 1'] == -1:
                special_list[running_process_index]['Start time 1'] = i
            else:
                special_list[running_process_index]['Start time ' + str(int(((len(special_list[running_process_index])) / 2) + 1))] = i
                # since the process may have multiple start times in this algorithm

        if previous_running_index != running_process_index:
            all_process_list[previous_running_index]['Completion time'] = i + remaining_time_list[previous_running_index]
            if remaining_time_list[previous_running_index] > 0:
                if special_list[previous_running_index]['End time 1'] == 0:
                    special_list[previous_running_index]['End time 1'] = i
                else:
                    special_list[previous_running_index]['End time '+str((floor((len(special_list[previous_running_index]))/2))+1)] = i
            else:
                if special_list[previous_running_index]['End time 1'] == 0:
                    special_list[previous_running_index]['End time 1'] = i + remaining_time_list[previous_running_index]
                else:
                    special_list[previous_running_index]['End time '+str((floor((len(special_list[previous_running_index]))/2))+1)] = i + remaining_time_list[previous_running_index]




    all_process_list[running_process_index]['Completion time'] = i
    if special_list[running_process_index]['End time 1'] == 0:
        special_list[running_process_index]['End time 1'] = i
    else:
        special_list[running_process_index]['End time '+str((floor((len(special_list[running_process_index]))/2))+1)] = i
            # since the process have multiple start times , it must also have multiple end times

    total_waiting_time = 0
    avg_waiting_time = 0
    for i in all_process_list:
        i['Turnaround time'] = i['Completion time'] - i['Arrival time']
        i['Waiting time'] = i['Turnaround time'] - i['Burst time']
        total_waiting_time += i['Waiting time']
    for i in range(processes_count):
        special_list[i]['Process ID'] = all_process_list[i]['Process ID']

    for i in all_process_list:
        print(i)

    avg_waiting_time = total_waiting_time / processes_count
    return avg_waiting_time,special_list


