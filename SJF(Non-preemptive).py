def SJF_Non_Preemptive():
    '''
    This function receives any positive number of process with any positive arrival times and burst times
    and sorts them according to shortest job first Algorithm to obtain min average waiting time.
    This function does not handle starvation and returns min average waiting time.
    '''
    one_process_dictionary = {
        'Process ID' : 0,
        'Arrival time' : 0,
        'Burst time' : 0,
        'Waiting time' : 0,
        'Turnaround time' : 0,
        'Completion time' : 0
    }
    x = int(input("Please enter number of process you want : "))
    all_process_list = [one_process_dictionary] * x
    #data entry
    for i in range(x):
        if i > 0:
            all_process_list[i] = all_process_list[i-1].copy()
        all_process_list[i]['Process ID'] = i+1
        y = int(input("Please enter arrival time of process {} : ".format(i+1)))
        all_process_list[i]['Arrival time'] = y
        y = int(input("Please enter burst time of process {} : ".format(i+1)))
        all_process_list[i]['Burst time'] = y
    #the process with min arrival time must be the first one in the list
    #if there are multiple process with min arrival time , the one with min burst time must be the first
    for i in range(1,x):
        if all_process_list[0]['Arrival time'] > all_process_list[i]['Arrival time']:
            all_process_list[0] , all_process_list[i] = all_process_list[i] , all_process_list[0]
        elif all_process_list[0]['Arrival time'] == all_process_list[i]['Arrival time']:
            if all_process_list[0]['Burst time'] > all_process_list[i]['Burst time']:
                all_process_list[0], all_process_list[i] = all_process_list[i], all_process_list[0]

    #since first process is special (because it never awaits) , so we do its calculation here not in loop like others
    all_process_list[0]['Completion time'] = all_process_list[0]['Arrival time'] + all_process_list[0]['Burst time']
    all_process_list[0]['Turnaround time'] = all_process_list[0]['Burst time']
    all_process_list[0]['Waiting time'] = 0
    last_process_completion_time = all_process_list[0]['Completion time']
    total_waiting_time = 0

    for i in range(1,x):
        #must guarantee that the first process after the one which has finished has arrived before the last process completion time
        for j in range(i+1,x):
            if last_process_completion_time >= all_process_list[i]['Arrival time']:
                break
            elif last_process_completion_time >= all_process_list[j]['Arrival time']:
                all_process_list[i], all_process_list[j] = all_process_list[j], all_process_list[i]
                break
        #the process with min burst time must come in i-th position
        for j in range(i+1, x):
            if (last_process_completion_time >= all_process_list[j]['Arrival time'] and
                 all_process_list[i]['Burst time'] > all_process_list[j]['Burst time']):
                    all_process_list[i] , all_process_list[j] = all_process_list[j] , all_process_list[i]
        all_process_list[i]['Completion time'] = last_process_completion_time + all_process_list[i]['Burst time']
        last_process_completion_time = all_process_list[i]['Completion time']
        all_process_list[i]['Turnaround time'] = all_process_list[i]['Completion time'] - all_process_list[i]['Arrival time']
        all_process_list[i]['Waiting time'] = all_process_list[i]['Turnaround time'] - all_process_list[i]['Burst time']
        total_waiting_time += all_process_list[i]['Waiting time']

    average_waiting_time = total_waiting_time / x
    return average_waiting_time


