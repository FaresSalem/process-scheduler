def SJF_Non_Preemptive():
    '''
    This function receives any positive number of processes with any positive arrival times and burst times,
    and sorts them according to shortest job first Algorithm to obtain minimum average waiting time.
    This function does not handle starvation and returns minimum average waiting time.
    '''
    one_process_dictionary = {
        'Process ID'        : 0,
        'Arrival time'      : 0,
        'Burst time'        : 0,
        'Waiting time'      : 0,
        'Turnaround time'   : 0,
        'Completion time'   : 0
    }
    processes_count = int(input("Please enter number of processes you want : "))
    all_processes_list = [one_process_dictionary] * processes_count
    #data entry
    for i in range(processes_count):
        if i > 0:
            all_processes_list[i] = all_processes_list[i-1].copy()
        all_processes_list[i]['Process ID'] = i+1
        y = int(input("Please enter arrival time of process {} : ".format(i+1)))
        all_processes_list[i]['Arrival time'] = y
        y = int(input("Please enter burst time of process {} : ".format(i+1)))
        all_processes_list[i]['Burst time'] = y
    #the process with min arrival time must be the first one in the list
    #if there are multiple process with min arrival time , the one with min burst time must be the first
    for i in range(1,processes_count):
        if all_processes_list[0]['Arrival time'] > all_processes_list[i]['Arrival time']:
            all_processes_list[0] , all_processes_list[i] = all_processes_list[i] , all_processes_list[0]
        elif all_processes_list[0]['Arrival time'] == all_processes_list[i]['Arrival time']:
            if all_processes_list[0]['Burst time'] > all_processes_list[i]['Burst time']:
                all_processes_list[0], all_processes_list[i] = all_processes_list[i], all_processes_list[0]

    #since first process is special (because it never awaits) , so we do its calculation here not in loop like others
    all_processes_list[0]['Completion time'] = all_processes_list[0]['Arrival time'] + all_processes_list[0]['Burst time']
    all_processes_list[0]['Turnaround time'] = all_processes_list[0]['Burst time']
    all_processes_list[0]['Waiting time'] = 0
    last_process_completion_time = all_processes_list[0]['Completion time']
    total_waiting_time = 0

    for i in range(1,processes_count):
        #must guarantee that the first process after the one which has finished has arrived before the last process completion time
        for j in range(i+1,processes_count):
            if last_process_completion_time >= all_processes_list[i]['Arrival time']:
                break
            elif last_process_completion_time >= all_processes_list[j]['Arrival time']:
                all_processes_list[i], all_processes_list[j] = all_processes_list[j], all_processes_list[i]
                break
        #the process with min burst time must come in i-th position
        for j in range(i+1, processes_count):
            if (last_process_completion_time >= all_processes_list[j]['Arrival time'] and
                 all_processes_list[i]['Burst time'] > all_processes_list[j]['Burst time']):
                    all_processes_list[i] , all_processes_list[j] = all_processes_list[j] , all_processes_list[i]
        all_processes_list[i]['Completion time'] = last_process_completion_time + all_processes_list[i]['Burst time']
        last_process_completion_time = all_processes_list[i]['Completion time']
        all_processes_list[i]['Turnaround time'] = all_processes_list[i]['Completion time'] - all_processes_list[i]['Arrival time']
        all_processes_list[i]['Waiting time'] = all_processes_list[i]['Turnaround time'] - all_processes_list[i]['Burst time']
        total_waiting_time += all_processes_list[i]['Waiting time']

    average_waiting_time = total_waiting_time / processes_count
    return average_waiting_time


