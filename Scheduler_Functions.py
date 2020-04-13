'''
This module contains the scheduling functions:

First Come, First Serve (FCFS) Scheduling
Priority Scheduling (Preemptive)
Priority Scheduling (Non-Preemptive)
Shortest Job First (SJF) Scheduling
Shortest Remaining Time First (SRTF) Scheduling
Round-Robin (RR) Scheduling
'''

def FCFS(arrival_time, processes_count, burst_time):
# Python3 program for implementurn_around_timeion
# of FCFS scheduling
    one_process_dictionary = {
    'Process ID'        : 0,
    'Arrival time'      : 0,
    'Waiting time'      : 0,
    'Turnaround time'   : 0,
    'Completion time'   : 0,
    'Start time'        : 0,
    }
    special_dictionary = {
        'Process ID'        : 0,
        'Start time 1'        : -1,
        'End time 1'          : 0
    }
    all_processes_list = [one_process_dictionary] * processes_count

    special_list = [special_dictionary] * processes_count
    for i in range(processes_count):
        if i > 0:
            all_processes_list[i] = all_processes_list[i-1].copy()
            special_list[i] = special_list[i - 1].copy()
        all_processes_list[i]['Process ID'] = i + 1
        all_processes_list[i]['Arrival time'] = arrival_time[i]
        all_processes_list[i]['Burst time'] = burst_time[i]
    all_processes_list = sorted(all_processes_list , key=lambda x:x['Arrival time'])

    #first process special case
    # since first process is special (because it never awaits) , so we do its calculation here not in loop like others
    all_processes_list[0]['Completion time'] = all_processes_list[0]['Arrival time'] + all_processes_list[0]['Burst time']
    all_processes_list[0]['Start time']= all_processes_list[0]['Arrival time']
    all_processes_list[0]['Turnaround time'] = all_processes_list[0]['Burst time']
    all_processes_list[0]['Waiting time'] = 0
    waiting_time = [0] * processes_count
    turn_around_time = [0] * processes_count
    total_waiting_time = 0
    total_turn_around_time = 0

    waiting_time[0] = 0


        # must guarantee that the first process after the one which has finished has arrived before the last process completion time
    for i in range (1,processes_count):
        # start time calculation
        if all_processes_list[i-1]['Completion time'] >= all_processes_list[i]['Arrival time']:
            all_processes_list[i]['Start time']  = all_processes_list[i - 1]['Completion time']
        elif all_processes_list[i-1]['Completion time'] < all_processes_list[i]['Arrival time']:
            all_processes_list[i]['Start time'] = all_processes_list[i]['Arrival time']
        # waiting time calculation
        waiting_time[i] = all_processes_list[i]['Start time'] - all_processes_list[i]['Arrival time']

        all_processes_list[i]['Completion time'] = all_processes_list[i]['Start time'] + all_processes_list[i]['Burst time']
        all_processes_list[i]['Turnaround time'] = all_processes_list[i]['Burst time'] + all_processes_list[i]['Waiting time']
        all_processes_list[i]['Waiting time'] = all_processes_list[i]['Start time'] - all_processes_list[i]['Arrival time']



    # calculating turnaround
    # time by adding burst_time[i] + waiting_time[i]
    for i in range(processes_count):
        turn_around_time[i] = burst_time[i] + waiting_time[i]


    # Calculate total waiting time
    # and total turn around time
    for i in range(processes_count):
        total_waiting_time = total_waiting_time + waiting_time[i]
        total_turn_around_time = total_turn_around_time + turn_around_time[i]

    for i in range(processes_count):
        special_list[i]['Process ID'] = all_processes_list[i]['Process ID']
        special_list[i]['Start time 1'] = all_processes_list[i]['Arrival time'] + all_processes_list[i]['Waiting time']
        special_list[i]['End time 1'] = all_processes_list[i]['Completion time']
    Average_waiting_time = (total_waiting_time / processes_count)
    
    return Average_waiting_time ,  special_list


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
        'Process ID' : 0,
        'Arrival time' : 0,
        'Burst time' : 0,
        'Waiting time' : 0,
        'Turnaround time' : 0,
        'Completion time' : 0,
        'Priority number' : 0
    }
    special_dictionary = {
        'Process ID':0,
        'Start time 1':-1,
        'End time 1':0
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


def P_NP(processes_count, arrival_times, burst_times, priority_numbers):   
# Priority Scheduling (Non-Preemptive)
#the original code is contriputed by Amir Abo zaid
#edited by Muhammad Kamal
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
        'Start time 1'        : -1,
        'End time 1'          : 0
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
            elif last_process_completion_time < all_processes_list[i]['Arrival time']:
                all_processes_list[i] , all_processes_list[j] = all_processes_list[j] , all_processes_list[i]

        # the process with min priority must come in i-th position
        for j in range(i+1, processes_count):
            if (last_process_completion_time >= all_processes_list[j]['Arrival time'] and
                 all_processes_list[i]['priority'] > all_processes_list[j]['priority']):
                    all_processes_list[i] , all_processes_list[j] = all_processes_list[j] , all_processes_list[i]
        if last_process_completion_time < all_processes_list[i]['Arrival time']:
            all_processes_list[i]['Start time']=all_processes_list[i]['Arrival time']
            all_processes_list[i]['Completion time'] = all_processes_list[i]['Arrival time'] + all_processes_list[i]['Burst time']
        else:
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


def SJF_Preemptive(processes_count, arrival_times, burst_times):
    from math import floor

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


def RoundRobin(arrival_times, processes_count, burst_times, quantum):
    # Function to calculate average waiting
  #  from math import floor

    one_process_dictionary = {
        'Process ID': 0,
        'Arrival time': 0,
        'Waiting time': 0,
        'Turnaround time': 0,
        'Completion time': 0,
        'Start time': 0,
        'Remaining time': 0
    }
    special_dictionary = {
        'Process ID': 0,
        'Start time 1': -1,
        'End time 1': 0
    }

    general_completion_time = 0
    all_process_list = [one_process_dictionary] * processes_count
    special_list = [special_dictionary] * processes_count
    # since this Algorithm is preemptive so we must know remaining time of each process before context switching
    # data entry
    for i in range(processes_count):
        if i > 0:
            all_process_list[i] = all_process_list[i - 1].copy()
            special_list[i] = special_list[i - 1].copy()
        all_process_list[i]['Process ID'] = i + 1
        all_process_list[i]['Arrival time'] = arrival_times[i]
        all_process_list[i]['Burst time'] = burst_times[i]
        all_process_list[i]['Remaining time'] = burst_times[i]
        general_completion_time += burst_times[i]
        special_list[i]['Process ID'] = i + 1

    # Function to find waiting time
    # of all processes
    # findWaitingTime(processes, n, burst_time,waiting_time,quantum)
    # Copy the burst time into rt[]
    for i in range(processes_count):
        all_process_list[i]['Remaining time'] = burst_times[i]
    t = min(arrival_times)  # Current time

    # Keep traversing processes in round
    # robin manner until all of them are
    # not done.
    while (1):
        done = True

        # Traverse all processes one by
        # one repeatedly
        for i in range(processes_count):
            # If burst time of a process is greater
            # than 0 then only need to process further
            if (all_process_list[i]['Remaining time'] > 0 and all_process_list[i]['Arrival time'] <= t):
                done = False  # There is a pending process
                if (all_process_list[i]['Remaining time'] > quantum):
                    # Increase the value of t i.e. shows
                    # how much time a process has been processed
                    if special_list[i]['Start time 1'] == -1:
                        special_list[i]['Start time 1'] = t
                    else:
                        special_list[i]['start time ' +
                                        str(int(((len(special_list[i])) / 2) + 1))] = t
                    t += quantum
                    if special_list[i]['End time 1'] == 0:
                        special_list[i]['End time 1'] = t
                    else:
                        special_list[i]['End time ' +
                                        str((floor((len(special_list[i])) / 2)))] = t

                    # Decrease the burst_time of current
                    # process by quantum
                    all_process_list[i]['Remaining time'] -= quantum

                # If burst time is smaller than or equal
                # to quantum. Last cycle for this process
                else:

                    # Increase the value of t i.e. shows
                    # how much time a process has been processed
                    if special_list[i]['Start time 1'] == -1:
                        special_list[i]['Start time 1'] = t
                    else:
                        special_list[i]['start time ' +
                                        str(int(((len(special_list[i])) / 2) + 1))] = t
                    t = t + all_process_list[i]['Remaining time']
                    if special_list[i]['End time 1'] == 0:
                        special_list[i]['End time 1'] = t
                    else:
                        special_list[i]['End time ' +
                                        str((floor((len(special_list[i])) / 2)))] = t

                    # Waiting time is current time minus
                    # time used by this process
                    all_process_list[i]['Waiting time'] = t - all_process_list[i]['Burst time']

                    # As the process gets fully executed
                    # make its remaining burst time = 0
                    all_process_list[i]['Remaining time'] = 0
            elif (all_process_list[i - 1]['Remaining time'] == 0 and all_process_list[i]['Arrival time'] > t):
                t = all_process_list[i]['Arrival time']
                done = False  # There is a pending process
                if (all_process_list[i]['Remaining time'] > quantum):
                    # Increase the value of t i.e. shows
                    # how much time a process has been processed
                    if special_list[i]['Start time 1'] == -1:
                        special_list[i]['Start time 1'] = t
                    else:
                        special_list[i]['start time ' +
                                        str(int(((len(special_list[i])) / 2) + 1))] = t
                    t += quantum
                    if special_list[i]['End time 1'] == 0:
                        special_list[i]['End time 1'] = t
                    else:
                        special_list[i]['End time ' +
                                        str((floor((len(special_list[i])) / 2)))] = t

                    # Decrease the burst_time of current
                    # process by quantum
                    all_process_list[i]['Remaining time'] -= quantum

                # If burst time is smaller than or equal
                # to quantum. Last cycle for this process
                else:

                    # Increase the value of t i.e. shows
                    # how much time a process has been processed
                    if special_list[i]['Start time 1'] == -1:
                        special_list[i]['Start time 1'] = t
                    else:
                        special_list[i]['start time ' +
                                        str(int(((len(special_list[i])) / 2) + 1))] = t
                    t = t + all_process_list[i]['Remaining time']
                    if special_list[i]['End time 1'] == 0:
                        special_list[i]['End time 1'] = t
                    else:
                        special_list[i]['End time ' +
                                        str((floor((len(special_list[i])) / 2)))] = t

                    # Waiting time is current time minus
                    # time used by this process
                    all_process_list[i]['Waiting time'] = t - all_process_list[i]['Burst time']

                    # As the process gets fully executed
                    # make its remaining burst time = 0
                    all_process_list[i]['Remaining time'] = 0

        # If all processes are done
        if (done == True):
            break

    # Function to find turn around time
    # for all processes
    # findTurnAroundTime(processes, n, burst_time,waiting_time,turn_around_time)
    # Calculating turnaround time
    for i in range(processes_count):
        all_process_list[i]['Turnaround time'] = burst_times[i] + \
                                                 all_process_list[i]['Waiting time']

    # Display processes along with all details
    # print("Processes Burst Time	 Waiting", "Time Turn-Around Time")
    total_waiting_time = 0
    total_turn_around_time = 0
    for i in range(processes_count):
        total_waiting_time = total_waiting_time + \
                             all_process_list[i]['Waiting time']
        total_turn_around_time = total_turn_around_time + \
                                 all_process_list[i]['Turnaround time']

    Average_waiting = (total_waiting_time / processes_count)
    return Average_waiting, special_list


