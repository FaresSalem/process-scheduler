#the original code was contributed 
# Shubham Singh(SHUBHAMSINGH10) GeeksForGeeks website 
# edited by muhammedkamal
# this program for implementation for periority scheduling  


def PQ_NP(totalprocess,arrivaltime,bursttime,priority):
    one_process_dictionary = {
    'Process ID'        : 0,
    'Arrival time'      : 0,
    'Waiting time'      : 0,
    'Turnaround time'   : 0,
    'Completion time'   : 0,
    'Start time '       : 0
}
    proc = [] 
    for i in range(totalprocess): 
        l = [] 
        for j in range(totalprocess-1): 
            l.append(0) 
        proc.append(l) 
    all_processes_list = [one_process_dictionary] * totalprocess
    for i in range(totalprocess):  
        proc[i][0] = all_processes_list[i]['Arrival time'] = arrivaltime[i]  
        proc[i][1] = bursttime[i]  
        proc[i][2] = priority[i]  
        proc[i][3] = all_processes_list[i]['Process ID'] = i + 1
    # Using inbuilt sort function  
    proc = sorted (proc, key = lambda x:x[2]) 
    proc = sorted (proc) 
    
    # Calling function findgc for 
        # Declare waiting time and 
# turnaround time array  
    wt = [0] * totalprocess
    tat = [0] * totalprocess

    wavg = 0
    tavg = 0

    # Function call to find waiting time array  
    # declaring service array that stores 
    # cumulative burst time  
    service = [0] * totalprocess

    # Initilising initial elements  
    # of the arrays  
    service[0] = 0
    all_processes_list[0]['Waiting time']= wt[0] = 0

    for i in range(1, totalprocess):  
        service[i] = proc[i - 1][1] + service[i - 1]  
        all_processes_list[i]['Waiting time'] =wt[i] = service[i] - proc[i][0] + 1

        # If waiting time is negative, 
        # change it o zero  
        if(wt[i] < 0) :      
            all_processes_list[i]['Waiting time'] =wt[i] = 0  
    
    # Function call to find turnaround time  
    # Filling turnaroundtime array  
    for i in range(totalprocess): 
        all_processes_list[i]['Turnaround time'] =tat[i] = proc[i][1] + wt[i]   

    stime = [0] * totalprocess
    ctime = [0] * totalprocess
    all_processes_list[0]['Start time']=stime[0] = 1
    all_processes_list[0]['Completion time']=ctime[0] = stime[0] + tat[0] 
    
    # calculating starting and ending time  
    for i in range(1, totalprocess):  
        all_processes_list[i]['Start time']=stime[i] = ctime[i - 1]  
        all_processes_list[i]['Completion time']=ctime[i] = stime[i] + tat[i] - wt[i]  


    # display the process details  
    for i in range(totalprocess): 
        wavg += wt[i]  
        tavg += tat[i]  
    
    wavg=wavg / totalprocess
    tavg=tavg / totalprocess

    #this was for the testing master farosa 
    """ print(proc[i][3], "\t\t", stime[i],  
                        "\t\t", end = " ") 
        print(ctime[i], "\t\t", tat[i], "\t\t\t", wt[i])  

    
    # display the average waiting time  
    # and average turn around time  
    print("Average waiting time is : ", end = " ") 
    print(wavg) 
    print("average turnaround time : " , end = " ") 
    print(tavg) """
    return all_processes_list, wavg, tavg


#this was just a testing mester farosa :)
""" if __name__ == "__main__":
    totalprocess = 5
    arrivaltime = [1, 2, 3, 4, 5] 
    bursttime = [3, 5, 1, 7, 4] 
    priority = [3, 4, 1, 7, 8]
    PQ_NP(totalprocess,arrivaltime,bursttime,priority) """  
          
  
  
     
  
