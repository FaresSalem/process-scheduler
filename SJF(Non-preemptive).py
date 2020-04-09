def SJF(processes_count, arrival_times, burst_times):  # Shortest Job First (SJF) Scheduling
    '''
    This function receives any positive number of processes with same number of positive arrival times and burst times,
    and sorts them according to shortest job first Algorithm to obtain minimum average waiting time.
    This function does not handle starvation and returns a tuple containing avgerage waiting time and a list of
    starting and ending times for each process.
    '''
    # the values in following 2 dictionaries are just for initialization and will be changed according to user inputs
    one_process_dictionary = {
        'Process ID': 0,
        'Arrival time': 0,
        'Burst time': 0,
        'Waiting time': 0,
        'Turnaround time': 0,
        'Completion time': 0
    }
    special_dictionary = {
        'Process ID': 0,
        'Start time': -1,
        'End time': 0
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

