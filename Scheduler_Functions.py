'''
This module contains the scheduling functions:

First Come, First Serve (FCFS) Scheduling
Priority Scheduling (Preemptive)
Priority Scheduling (Non-Preemptive)
Shortest Job First (SJF) Scheduling
Shortest Remaining Time First (SRTF) Scheduling
Round-Robin (RR) Scheduling
'''

def P_P(processes_count, arrival_times, burst_times, priority_numbers): # Priority Scheduling (Preemptive)
    from math import floor
    '''
    this function is an implemention of preemptive priority scheduling algorithm
    this function receives any positive number of process with the same number of arrival times , burst times , and priority number
    note that in this implementation , the process with the min priority number have the highest priority
    this function returns a tuple containing the average waiting time and a list of starting and ending times for each process
    very important : this function does not handle starvation problem
    '''
    #the values in following 2 dictionaries are just for initialization and will be changed according to user inputs
    one_process_dictionary = {
        'Process ID'        : 0,
        'Arrival time'      : 0,
        'Burst time'        : 0,
        'Waiting time'      : 0,
        'Turnaround time'   : 0,
        'Completion time'   : 0,
        'Priority number'   : 0
    }
    special_dictionary = {
        'Process ID'        :0,
        'Start time 1'      :-1,
        'End time 1'        :0
    }
    general_completion_time = 0
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
        general_completion_time += burst_times[i]
        all_process_list[i]['Priority number'] = priority_numbers[i]
        special_list[i]['Process ID'] = i+1

    #the process with min arrival time must be the first one to start
    #if there are multiple process with min arrival time , the one with min Priority number must be the first one to start
    running_process_index = 0  #initially we assume process 1 has min arrival time until we found something else
    for i in range(processes_count):
        if all_process_list[running_process_index]['Arrival time'] > all_process_list[i]['Arrival time']:
            running_process_index = i
        elif all_process_list[running_process_index]['Arrival time'] == all_process_list[i]['Arrival time']:
            if all_process_list[running_process_index]['Priority number'] > all_process_list[i]['Priority number']:
                running_process_index = i
    #after previous loop we guarantee that running process index is the index of process that must start
    #notice that index start from 0 while process ID start from 1
    min_arrival_time = all_process_list[running_process_index]['Arrival time']
    special_list[running_process_index]['Start time 1'] = min_arrival_time
    for i in range (min_arrival_time+1,min_arrival_time + 1 + general_completion_time):
        #we must check after each unit time which process to be run
        remaining_time_list[running_process_index] -= 1
        previous_running_index = running_process_index
        if remaining_time_list[running_process_index] == 0: #if a process has finished its work we must move into anpther one
            for k in range(processes_count):
                if remaining_time_list[k] !=0:
                    running_process_index = k
                    break
        for j in range(processes_count):
            if (all_process_list[j]['Arrival time'] <= i and
                all_process_list[j]['Priority number'] < all_process_list[running_process_index]['Priority number'] and
                remaining_time_list[j] > 0):
                    running_process_index = j

        if previous_running_index != running_process_index:
            if special_list[running_process_index]['Start time 1'] == -1:
                special_list[running_process_index]['Start time 1'] = i
            else:
                special_list[running_process_index]['Start time ' + str(int(((len(special_list[running_process_index])) / 2) + 1))] = i

        if previous_running_index != running_process_index:
            all_process_list[previous_running_index]['Completion time'] = i
            if special_list[previous_running_index]['End time 1'] == 0:
                special_list[previous_running_index]['End time 1'] = i
            else:
                special_list[previous_running_index]['End time '+str((floor((len(special_list[previous_running_index]))/2))+1)] = i
                #since the process may have multiple start times in this algorithm

    all_process_list[running_process_index]['Completion time'] = min_arrival_time + general_completion_time
    if special_list[running_process_index]['End time 1'] == 0:
        special_list[running_process_index]['End time 1'] = min_arrival_time + general_completion_time
    else:
        special_list[running_process_index]['End time '+str((floor((len(special_list[running_process_index]))/2))+1)] = min_arrival_time + general_completion_time
            # since the process have multiple start times , it must also have multiple end times

    total_waiting_time = 0
    avg_waiting_time = 0
    for i in all_process_list:
        i['Turnaround time'] = i['Completion time'] - i['Arrival time']
        i['Waiting time'] = i['Turnaround time'] - i['Burst time']
        total_waiting_time += i['Waiting time']

    avg_waiting_time = total_waiting_time / processes_count
    return avg_waiting_time, special_list


def P_NP(processes_count, arrival_times, burst_times, priority_numbers):    # Priority Scheduling (Non-Preemptive)
# the original code was contributed
# Shubham Singh(SHUBHAMSINGH10) GeeksForGeeks website
# edited by muhammedkamal
# this program for implementation for periority scheduling
    one_process_dictionary = {
    'Process ID'        : 0,
    'Arrival time'      : 0,
    'Waiting time'      : 0,
    'Turnaround time'   : 0,
    'Completion time'   : 0,
    'Start time'        : 0,
    'priority'          : 0
    }
    special_dictionary = {
        'Process ID'        : 0,
        'Start time'        : -1,
        'End time'          : 0
    }
    all_processes_list = [one_process_dictionary] * processes_count
    special_list = [special_dictionary] * processes_count    # data entry
    for i in range(processes_count):
        if i > 0:
            all_processes_list[i] = all_processes_list[i-1].copy()
            special_list[i] = special_list[i - 1].copy()
        all_processes_list[i]['Process ID'] = i + 1
        all_processes_list[i]['Arrival time'] = arrival_times[i]
        all_processes_list[i]['Burst time'] = burst_times[i]
        all_processes_list[i]['priority'] = priority_numbers[i]
    # the process with min arrival time must be the first one in the list
    # if there are multiple process with min arrival time , the one with min priority must be the first
    for i in range(1,processes_count):
        if all_processes_list[0]['Arrival time'] > all_processes_list[i]['Arrival time']:
            all_processes_list[0] , all_processes_list[i] = all_processes_list[i] , all_processes_list[0]
        elif all_processes_list[0]['Arrival time'] == all_processes_list[i]['Arrival time']:
            if all_processes_list[0]['priority'] > all_processes_list[i]['priority']:
                all_processes_list[0], all_processes_list[i] = all_processes_list[i], all_processes_list[0]

    # since first process is special (because it never awaits) , so we do its calculation here not in loop like others
    all_processes_list[0]['Completion time'] = all_processes_list[0]['Arrival time'] + all_processes_list[0]['Burst time']
    all_processes_list[0]['Start time']= all_processes_list[0]['Arrival time']
    all_processes_list[0]['Turnaround time'] = all_processes_list[0]['Burst time']
    all_processes_list[0]['Waiting time'] = 0
    last_process_completion_time = all_processes_list[0]['Completion time']
    total_waiting_time = 0

    for i in range(1,processes_count):
        # must guarantee that the first process after the one which has finished has arrived before the last process completion time
        for j in range(i+1,processes_count):
            if last_process_completion_time >= all_processes_list[i]['Arrival time']:
                break
            elif last_process_completion_time >= all_processes_list[j]['Arrival time']:
                all_processes_list[i], all_processes_list[j] = all_processes_list[j], all_processes_list[i]
                break
        # the process with min priority must come in i-th position
        for j in range(i+1, processes_count):
            if (last_process_completion_time >= all_processes_list[j]['Arrival time'] and
                 all_processes_list[i]['priority'] > all_processes_list[j]['priority']):
                    all_processes_list[i] , all_processes_list[j] = all_processes_list[j] , all_processes_list[i]
        all_processes_list[i]['Completion time'] = last_process_completion_time + all_processes_list[i]['Burst time']
        all_processes_list[i]['Start time']=last_process_completion_time
        last_process_completion_time = all_processes_list[i]['Completion time']
        all_processes_list[i]['Turnaround time'] = all_processes_list[i]['Completion time'] - all_processes_list[i]['Arrival time']
        all_processes_list[i]['Waiting time'] = all_processes_list[i]['Turnaround time'] - all_processes_list[i]['Burst time']
        total_waiting_time += all_processes_list[i]['Waiting time']


    for i in range(processes_count):
        special_list[i]['Process ID'] = all_processes_list[i]['Process ID']
        special_list[i]['Start time'] = all_processes_list[i]['Arrival time'] + all_processes_list[i]['Waiting time']
        special_list[i]['End time'] = all_processes_list[i]['Completion time']
    
    average_waiting_time = total_waiting_time / processes_count

    return average_waiting_time, special_list


def SJF(processes_count, arrival_times, burst_times):  # Shortest Job First (SJF) Scheduling
    '''
    This function receives any positive number of processes with same number of positive arrival times and burst times,
    and sorts them according to shortest job first Algorithm to obtain minimum average waiting time.
    This function does not handle starvation and returns a tuple containing avgerage waiting time and a list of
    starting and ending times for each process.
    '''
    # the values in following 2 dictionaries are just for initialization and will be changed according to user inputs
    one_process_dictionary = {
        'Process ID'        : 0,
        'Arrival time'      : 0,
        'Burst time'        : 0,
        'Waiting time'      : 0,
        'Turnaround time'   : 0,
        'Completion time'   : 0
    }
    special_dictionary = {
        'Process ID'        : 0,
        'Start time'        : -1,
        'End time'          : 0
    }

    all_processes_list = [one_process_dictionary] * processes_count
    special_list = [special_dictionary] * processes_count
    # data entry
    for i in range(processes_count):
        if i > 0:
            all_processes_list[i] = all_processes_list[i - 1].copy()
            special_list[i] = special_list[i - 1].copy()
        all_processes_list[i]['Process ID'] = i + 1
        all_processes_list[i]['Arrival time'] = arrival_times[i]
        all_processes_list[i]['Burst time'] = burst_times[i]

    # the process with min arrival time must be the first one in the list
    # if there are multiple process with min arrival time , the one with min burst time must be the first
    for i in range(1, processes_count):
        if all_processes_list[0]['Arrival time'] > all_processes_list[i]['Arrival time']:
            all_processes_list[0], all_processes_list[i] = all_processes_list[i], all_processes_list[0]
        elif all_processes_list[0]['Arrival time'] == all_processes_list[i]['Arrival time']:
            if all_processes_list[0]['Burst time'] > all_processes_list[i]['Burst time']:
                all_processes_list[0], all_processes_list[i] = all_processes_list[i], all_processes_list[0]

    # since first process is special (because it never awaits) , so we do its calculation here not in loop like others
    all_processes_list[0]['Completion time'] = all_processes_list[0]['Arrival time'] + all_processes_list[0][
        'Burst time']
    all_processes_list[0]['Turnaround time'] = all_processes_list[0]['Burst time']
    all_processes_list[0]['Waiting time'] = 0
    last_process_completion_time = all_processes_list[0]['Completion time']
    total_waiting_time = 0

    for i in range(1, processes_count):
        # must guarantee that the first process after the one which has finished has arrived before the last process completion time
        for j in range(i + 1, processes_count):
            if last_process_completion_time >= all_processes_list[i]['Arrival time']:
                break
            elif last_process_completion_time >= all_processes_list[j]['Arrival time']:
                all_processes_list[i], all_processes_list[j] = all_processes_list[j], all_processes_list[i]
                break
        # the process with min burst time must come in i-th position
        for j in range(i + 1, processes_count):
            if (last_process_completion_time >= all_processes_list[j]['Arrival time'] and
                    all_processes_list[i]['Burst time'] > all_processes_list[j]['Burst time']):
                all_processes_list[i], all_processes_list[j] = all_processes_list[j], all_processes_list[i]
        all_processes_list[i]['Completion time'] = last_process_completion_time + all_processes_list[i]['Burst time']
        last_process_completion_time = all_processes_list[i]['Completion time']
        all_processes_list[i]['Turnaround time'] = all_processes_list[i]['Completion time'] - all_processes_list[i][
            'Arrival time']
        all_processes_list[i]['Waiting time'] = all_processes_list[i]['Turnaround time'] - all_processes_list[i][
            'Burst time']
        total_waiting_time += all_processes_list[i]['Waiting time']

    for i in range(processes_count):
        special_list[i]['Process ID'] = all_processes_list[i]['Process ID']
        special_list[i]['Start time'] = all_processes_list[i]['Arrival time'] + all_processes_list[i]['Waiting time']
        special_list[i]['End time'] = all_processes_list[i]['Completion time']

    average_waiting_time = total_waiting_time / processes_count

    return average_waiting_time, special_list





