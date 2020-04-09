# the original code was contributed
# Shubham Singh(SHUBHAMSINGH10) GeeksForGeeks website
# edited by muhammedkamal
# this program for implementation for periority scheduling


def PQ_NP(processes_count, arrival_times, burst_times, priority):
    one_process_dictionary = {
    'Process ID': 0,
    'Arrival time': 0,
    'Waiting time': 0,
    'Turnaround time': 0,
    'Completion time': 0,
    'Start time': 0,
    'priority': 0
}
    output_process_dictionary = {
    'Process ID'        : 0,
    'Start time'        : 0,
    'Completion time'   : 0
}
    all_processes_list = [one_process_dictionary] * processes_count
    output_processes_list = [output_process_dictionary] * processes_count
    # data entry
    for i in range(processes_count):
        if i > 0:
            all_processes_list[i] = all_processes_list[i-1].copy()
        output_processes_list[i]['Process ID']=all_processes_list[i]['Process ID'] = i+1
        all_processes_list[i]['Arrival time'] = arrival_times[i]
        all_processes_list[i]['Burst time'] = burst_times[i]
        all_processes_list[i]['priority'] = priority[i]
    # the process with min arrival time must be the first one in the list
    # if there are multiple process with min arrival time , the one with min priority must be the first
    for i in range(1,processes_count):
        if all_processes_list[0]['Arrival time'] > all_processes_list[i]['Arrival time']:
            all_processes_list[0] , all_processes_list[i] = all_processes_list[i] , all_processes_list[0]
        elif all_processes_list[0]['Arrival time'] == all_processes_list[i]['Arrival time']:
            if all_processes_list[0]['priority'] > all_processes_list[i]['priority']:
                all_processes_list[0], all_processes_list[i] = all_processes_list[i], all_processes_list[0]

    # since first process is special (because it never awaits) , so we do its calculation here not in loop like others
    output_processes_list[0]['Completion time'] =all_processes_list[0]['Completion time'] = all_processes_list[0]['Arrival time'] + all_processes_list[0]['Burst time']
    output_processes_list[0]['Start time'] =all_processes_list[0]['Start time']= all_processes_list[0]['Arrival time']
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
        output_processes_list[0]['Completion time'] =all_processes_list[i]['Completion time'] = last_process_completion_time + all_processes_list[i]['Burst time']
        output_processes_list[0]['Start time'] =all_processes_list[i]['Start time']=last_process_completion_time
        last_process_completion_time = all_processes_list[i]['Completion time']
        all_processes_list[i]['Turnaround time'] = all_processes_list[i]['Completion time'] - all_processes_list[i]['Arrival time']
        all_processes_list[i]['Waiting time'] = all_processes_list[i]['Turnaround time'] - all_processes_list[i]['Burst time']
        total_waiting_time += all_processes_list[i]['Waiting time']

    average_waiting_time = total_waiting_time / processes_count
    return average_waiting_time, output_processes_list


# this was just a testing mester farosa :)
if __name__ == "__main__":
     processes_count=5
     arrival_times =[1, 1, 3, 1, 5] 
     burst_times = [3, 5, 8, 7, 4]
     priority = [3, 4, 1, 2, 8]
     print(PQ_NP(processes_count,arrival_times,burst_times,priority))
  
  
     
  
