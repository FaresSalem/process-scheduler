#! /usr/bin/env python
#  -*- coding: utf-8 -*-    # Defining Python Source Code Encodings
'''
    #! /usr/bin/env python
    This is a shebang, it tells the program loader that this script
    is executed with python, so you don't have to type python before running
    the .py file.
    In Unix-like operating systems, when a text file has a shebang, it is 
    interpreted as an executable file
'''
########################## IMPORTS ###########################
import sys
import matplotlib
matplotlib.use("TkAgg")     #  specifiy the backend, "TkAgg" that we wish to use with Matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from random import seed, randint

from Scheduler_Functions import *

try:
    from tkinter import *
except ImportError:
    from Tkinter import * 

try:
    import tkinter.ttk as ttk
    py3 = 1
except ImportError:
    import ttk
    py3 = 0
####################### End of IMPORTS #######################

########################### GUI Initiating Functions ###########################
def create_window():
    global root, top
    root = Tk()              # creating a tkinter window, Tk is a class
    set_Tk_var()             # setting variables used in the gui
    top = MainFrame(root)    # building the gui, so it's like MainFrame is inheriting the Tk class 

    Initiate_GanttChart()
    subplot.set_ylim(0, 10)
    subplot.set_xlim(0, 100)
    subplot.set_yticks([5])
    subplot.set_yticklabels([0])
    
    top.TextBox_OP.configure(state='normal')
    top.TextBox_OP.delete('1.0', 'end')
    top.TextBox_OP.insert('1.0', "Welcome to our scheduler simulator :D, please choose an algorithm from above.")
    top.TextBox_OP.configure(state='disabled')
    
    root.mainloop()           # infinite main loop

def set_Tk_var():
    global selected_algorithm # Radiobutton Variable for selected scheduling algorithm
    global processes_count    # Number of processes input by user from spinbox 
    global AvgTime            # Average Time
    
    selected_algorithm = StringVar()
    selected_algorithm.set("0")
    
    AvgTime = StringVar()
    AvgTime.set('0.0')
    
    processes_count = StringVar()
    processes_count.set('1')
    
    global bool
    bool = IntVar()
    bool.set(0)

######################## End of GUI Initiating Functions #######################


#########################     Simulator Functions     ##########################
processes_list = list()
def Preparing_Simulation():
    print(selected_algorithm.get())
    global processes_list
    Processes_Count = int(processes_count.get())
    
    if selected_algorithm.get() == 'FCFS':
        Arrival_Times, Burst_Times = Ask_For_and_Get_Input('FCFS')
        average_time, processes_list = FCFS(Processes_Count, Arrival_Times, Burst_Times)
        print(processes_list)
        
    elif selected_algorithm.get() == 'P_P':
        Arrival_Times, Burst_Times, Priorities = Ask_For_and_Get_Input('P_P')
        average_time, processes_list = P_P(Processes_Count, Arrival_Times, Burst_Times, Priorities)
        print(processes_list)
        
    elif selected_algorithm.get() == 'P_NP':       
        Arrival_Times, Burst_Times, Priorities = Ask_For_and_Get_Input('P_NP')
        average_time, processes_list = P_NP(Processes_Count, Arrival_Times, Burst_Times, Priorities)
        print(processes_list)
        
    elif selected_algorithm.get() == 'SJF': 
        Arrival_Times, Burst_Times = Ask_For_and_Get_Input('SJF')
        average_time, processes_list = SJF(Processes_Count, Arrival_Times, Burst_Times)
        print(processes_list)

    elif selected_algorithm.get() == 'SRTF': 
        Arrival_Times, Burst_Times = Ask_For_and_Get_Input('SRTF')
        average_time, processes_list = SJF_Preemptive(Processes_Count, Arrival_Times, Burst_Times)
        print(processes_list)

    elif selected_algorithm.get() == 'RR':
        Arrival_Times, Burst_Times, Quantum = Ask_For_and_Get_Input('RR')
        average_time, processes_list = RoundRobin(Processes_Count, Arrival_Times, Burst_Times, Quantum)
        print(processes_list)
    AvgTime.set("{}".format(average_time))


def Ask_For_and_Get_Input(algorithm):
    Processes_Count = int(processes_count.get())
    if algorithm == 'FCFS' or algorithm == 'SJF' or algorithm == 'SRTF':
        Arrival_Times = list()
        Burst_Times = list()
        for i in range(Processes_Count):
            # Prepare text boxes
            top.TextBox_OP.configure(state='normal')
            top.TextBox_OP.delete('1.0', 'end')
            top.TextBox_OP.insert('1.0', "In the Box below, Please enter the Arrival Time of process {}, then press Enter : ".format(i))
            top.TextBox_OP.configure(state='disabled')
            top.TextBox_OP.wait_variable(bool)  # wait foor user to press enter in a local event loop 
            # add input text to Arrival_Times list
            Arrival_Times.append(top.TextBox_IP.get('1.0', 'end').replace('\n', ''))
            top.TextBox_IP.configure(state='normal')
            top.TextBox_IP.delete('1.0', 'end')            
            
        for i in range(Processes_Count):
            # Prepare text boxes
            top.TextBox_OP.configure(state='normal')
            top.TextBox_OP.delete('1.0', 'end')
            top.TextBox_OP.insert('1.0', "In the Box below, Please enter the Burst Time of process {}, then press Enter : ".format(i))
            top.TextBox_OP.configure(state='disabled')
            top.TextBox_OP.wait_variable(bool)  # wait foor user to press enter in a local loop 
            # add input text to Arrival_Times list
            Burst_Times.append(top.TextBox_IP.get('1.0', 'end').replace('\n', ''))
            top.TextBox_IP.configure(state='normal')
            top.TextBox_IP.delete('1.0', 'end')            

        top.TextBox_OP.configure(state='normal')
        top.TextBox_OP.delete('1.0', 'end')
        top.TextBox_OP.insert('1.0', "Please click on the button Run Simulation")
        top.TextBox_OP.configure(state='disabled')
        for i in range(Processes_Count):
            Arrival_Times[i] = int(Arrival_Times[i])
            Burst_Times[i] = int(Burst_Times[i])
        
        return Arrival_Times, Burst_Times
        
    elif algorithm == 'P_P' or algorithm == 'P_NP':
        Arrival_Times = list()
        Burst_Times = list()
        Priorities = list()
        for i in range(Processes_Count):
            # Prepare text boxes
            top.TextBox_OP.configure(state='normal')
            top.TextBox_OP.delete('1.0', 'end')
            top.TextBox_OP.insert('1.0', "In the Box below, Please enter the Arrival Time of process {}, then press Enter : ".format(i))
            top.TextBox_OP.configure(state='disabled')
            top.TextBox_OP.wait_variable(bool)  # wait foor user to press enter in a local event loop 
            # add input text to Arrival_Times list
            Arrival_Times.append(top.TextBox_IP.get('1.0', 'end').replace('\n', ''))
            top.TextBox_IP.configure(state='normal')
            top.TextBox_IP.delete('1.0', 'end')            
            
        for i in range(Processes_Count):
            # Prepare text boxes
            top.TextBox_OP.configure(state='normal')
            top.TextBox_OP.delete('1.0', 'end')
            top.TextBox_OP.insert('1.0', "In the Box below, Please enter the Burst Time of process {}, then press Enter : ".format(i))
            top.TextBox_OP.configure(state='disabled')
            top.TextBox_OP.wait_variable(bool)  # wait foor user to press enter in a local loop 
            # add input text to Arrival_Times list
            Burst_Times.append(top.TextBox_IP.get('1.0', 'end').replace('\n', ''))
            top.TextBox_IP.configure(state='normal')
            top.TextBox_IP.delete('1.0', 'end')          
            
        for i in range(Processes_Count):
            # Prepare text boxes
            top.TextBox_OP.configure(state='normal')
            top.TextBox_OP.delete('1.0', 'end')
            top.TextBox_OP.insert('1.0', "In the Box below, Please enter the Priority of process {} (zero is highest), then press Enter : ".format(i))
            top.TextBox_OP.configure(state='disabled')
            top.TextBox_OP.wait_variable(bool)  # wait foor user to press enter in a local event loop 
            # add input text to Arrival_Times list
            Priorities.append(top.TextBox_IP.get('1.0', 'end').replace('\n', ''))
            top.TextBox_IP.configure(state='normal')
            top.TextBox_IP.delete('1.0', 'end')                  

        top.TextBox_OP.configure(state='normal')
        top.TextBox_OP.delete('1.0', 'end')
        top.TextBox_OP.insert('1.0', "Please click on the button Run Simulation")
        top.TextBox_OP.configure(state='disabled')
        for i in range(Processes_Count):
            Arrival_Times[i] = int(Arrival_Times[i])
            Burst_Times[i] = int(Burst_Times[i])
            Priorities[i] = int(Priorities[i])
            
        return Arrival_Times, Burst_Times, Priorities
               
    elif algorithm == 'RR':
        Arrival_Times = list()
        Burst_Times = list()
        for i in range(Processes_Count):
            # Prepare text boxes
            top.TextBox_OP.configure(state='normal')
            top.TextBox_OP.delete('1.0', 'end')
            top.TextBox_OP.insert('1.0', "In the Box below, Please enter the Arrival Time of process {}, then press Enter : ".format(i))
            top.TextBox_OP.configure(state='disabled')
            top.TextBox_OP.wait_variable(bool)  # wait foor user to press enter in a local event loop 
            # add input text to Arrival_Times list
            Arrival_Times.append(top.TextBox_IP.get('1.0', 'end').replace('\n', ''))
            top.TextBox_IP.configure(state='normal')
            top.TextBox_IP.delete('1.0', 'end')            
            
        for i in range(Processes_Count):
            # Prepare text boxes
            top.TextBox_OP.configure(state='normal')
            top.TextBox_OP.delete('1.0', 'end')
            top.TextBox_OP.insert('1.0', "In the Box below, Please enter the Burst Time of process {}, then press Enter : ".format(i))
            top.TextBox_OP.configure(state='disabled')
            top.TextBox_OP.wait_variable(bool)  # wait foor user to press enter in a local loop 
            # add input text to Burst_Times list
            Burst_Times.append(top.TextBox_IP.get('1.0', 'end').replace('\n', ''))
            top.TextBox_IP.configure(state='normal')
            top.TextBox_IP.delete('1.0', 'end')            
        
        # Prepare text boxes
        top.TextBox_OP.configure(state='normal')
        top.TextBox_OP.delete('1.0', 'end')
        top.TextBox_OP.insert('1.0', "In the Box below, Please enter the Quantum, then press Enter : ")
        top.TextBox_OP.configure(state='disabled')
        top.TextBox_OP.wait_variable(bool)  # wait foor user to press enter in a local loop 
        # Save entered Quantum
        Quantum = top.TextBox_IP.get('1.0', 'end').replace('\n', '')
        Quantum = int(Quantum)
        top.TextBox_IP.configure(state='normal')
        top.TextBox_IP.delete('1.0', 'end')    
        
        top.TextBox_OP.configure(state='normal')
        top.TextBox_OP.delete('1.0', 'end')
        top.TextBox_OP.insert('1.0', "Please click on the button Run Simulation")
        top.TextBox_OP.configure(state='disabled')
        for i in range(Processes_Count):
            Arrival_Times[i] = int(Arrival_Times[i])
            Burst_Times[i] = int(Burst_Times[i])
        
        return Arrival_Times, Burst_Times, Quantum

def Initiate_GanttChart():
    global subplot, gantt_chart
    gantt_chart = plt.Figure()      # add an empty chart by default
    subplot = gantt_chart.add_subplot(111)
    canvas = FigureCanvasTkAgg(gantt_chart, root)
    canvas.get_tk_widget().place(relx=0.337, rely=0.054, relheight=0.795, relwidth=0.64)
    subplot.set_ylabel('Process ID')
    subplot.set_xlabel('Time')
    toolbarFrame = Frame(root)
    toolbarFrame.place(relx=0.337, rely=0.054, relheight=0.05, relwidth=0.64)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    toolbar.update()
    
def Draw_GanttChart(processes_list):
    IDs = range(len(processes_list))    
    Start_and_Duration = list()    #  list of list of tuples
    temp = list()
    Processes_Count = int(processes_count.get())
    
    for i in range(Processes_Count):
        #  number of horizontal bars to be drawn = number of start or end times = (number of keys - 1) / 2
        for j in range(int((len(processes_list[i]) - 1) / 2)):  
            start_time = processes_list[i]['Start time {}'.format(j + 1)]
            duration   = processes_list[i]['End time {}'.format(j + 1)] - processes_list[i]['Start time {}'.format(j + 1)]
            temp.append((start_time , duration))
        Start_and_Duration.append(temp)
        temp = []    
    print(Start_and_Duration)
    
    # Start Drawing :D
    Initiate_GanttChart()
    # y_height = Processes_Count * 4
    # subplot.set_ylim(0, y_height)
    
    # y_ticks =  [y_height/(i+1) + 5 for i in range(Processes_Count)]
    # y_ticks =  [int(y_ticks[i] / 3) for i in range(Processes_Count)]
    
    # subplot.set_ylim(0, range(Processes_Count))
    subplot.set_yticks(range(Processes_Count))  # set ticks at heights = [0
                                # number of ticks equal number of processes, should be drawn at equal distances from each other 
    subplot.set_yticklabels(range(1,Processes_Count+1))
    
    x = max(max(Start_and_Duration))
    subplot.set_xlim(0, x[0] + x[1] + 10)  #last end time of processes

    # subplot.set_ylim(0, len(processes_list) - 1)
    # subplot.set_ylim(0, 10)
    # subplot.set_yticks([5])
    
    colors = ['red', 'blue', 'green', 'purple', 'black', 'grey', 'cyan', 'magenta']

    for i in range(len(Start_and_Duration)):
        seed(randint(0,100))
        color = colors[randint(0, 7)]
        subplot.broken_barh(Start_and_Duration[i], (i,0.5), facecolors =color)
        #start at zero and for 10 units, start at 30 and for 10 units, start at y = 2.5 and for 5 units
    
    # subplot.set_yticklabels([processes_list['Process ID']]) # Processes IDs


#####################      End of Simulator Functions       ####################


##############################  Buttons Functions  #############################
''' Functions related to the defined buttons in the GUI,
    There are six radiobuttons, one Run_Simulation button and an Exit button,
    There's also a function that is called when you press the <Return> key on your keyboard    
'''
def Run_Simulation(b):
    top.TextBox_OP.configure(state='normal')
    top.TextBox_OP.delete('1.0', 'end')
    top.TextBox_OP.insert('1.0', "To restart a new simulation, re-choose an algorithm again")
    top.TextBox_OP.configure(state='disabled')
    global processes_list,average_time
    Draw_GanttChart(processes_list)

    
def Return_button_pressed(b):
    # set the tkinter variable to anything to get out of the wait_variable() local loop
    bool.set(0)

def Radiobutton_FCFS(b):
    selected_algorithm.set("FCFS")
    Preparing_Simulation()
    
def Radiobutton_P_P(b):
    selected_algorithm.set("P_P")
    Preparing_Simulation()
    
def Radiobutton_P_NP(b):
    selected_algorithm.set("P_NP")
    Preparing_Simulation()
    
def Radiobutton_SJF(b):
    selected_algorithm.set("SJF")
    Preparing_Simulation()
    
def Radiobutton_SRTF(b):
    selected_algorithm.set("SRTF")
    Preparing_Simulation()
    
def Radiobutton_RR(b):
    selected_algorithm.set("RR")
    Preparing_Simulation()

def Exit(b):        
    # called when Exit button is pressed to just Exit :D
    root.destroy()

#######################    End of Buttons Functions    #########################


###########################     MainFrame Class      ###########################
class MainFrame:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font11 = "-family {Segoe UI} -size 12 -weight normal -slant " "roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=[('selected', _compcolor), ('active',_ana2color)])

        top.geometry("802x557+250+104")
        top.minsize(120, 1)
        top.maxsize(2970, 881)
        top.resizable(0, 0)
        top.title("Scheduler Simulator حلو وبالسمسم")
        top.configure(background="#000655", highlightbackground="#d9d9d9", highlightcolor="black", cursor="top_left_arrow")

        ################### Labels, Label Frames & Canvases ####################
        
        # Scheduling Algorithm Label Frame
        self.Labelframe1 = LabelFrame(top)
        self.Labelframe1.place(relx=0.013, rely=0.108, relheight=0.279, relwidth=0.264)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(text='''Scheduling Algorithm''', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        
        # Number of Processes Label Frame
        self.Labelframe2 = LabelFrame(top)
        self.Labelframe2.place(relx=0.013, rely=0.018, relheight=0.081, relwidth=0.264)
        self.Labelframe2.configure(relief='groove')
        self.Labelframe2.configure(foreground="black")
        self.Labelframe2.configure(text='''Number of Processes''', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")

        # Processes Information Label Frame
        self.Labelframe3 = LabelFrame(top)
        self.Labelframe3.place(relx=0.012, rely=0.395, relheight=0.458, relwidth=0.262)
        self.Labelframe3.configure(relief='groove')
        self.Labelframe3.configure(foreground="black")
        self.Labelframe3.configure(text='''Processes Information''', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
         
        # Gantt Chart Label Frame
        self.Labelframe4 = LabelFrame(top)         
        self.Labelframe4.place(relx=0.324, rely=0.018, relheight=0.853, relwidth=0.661)
        self.Labelframe4.configure(relief='groove')
        self.Labelframe4.configure(foreground="black")
        self.Labelframe4.configure(text='''Gantt Chart''', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        
        # Average Waiting Time Label Frame
        self.Labelframe5 = LabelFrame(top)          
        self.Labelframe5.place(relx=0.324, rely=0.88, relheight=0.099, relwidth=0.187)
        self.Labelframe5.configure(relief='groove')
        self.Labelframe5.configure(foreground="black")
        self.Labelframe5.configure(text='''Average Waiting Time''', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        
        # Average Waiting Time Label
        self.AvgTime_Label = Label(self.Labelframe5)
        self.AvgTime_Label.place(relx=0.067, rely=0.364, height=31, width=130, bordermode='ignore')
        self.AvgTime_Label.configure(background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        # Import Average Time from scheduler functions to (AvgTime) variable 
        self.AvgTime_Label.configure(textvariable=AvgTime)     
                                             
        ################ End of Labels, Label Frames & Canvases ################   


        ######################## Buttons & Radiobuttons ########################
        
        # Run Simulation Button
        self.Run_Button = Button(top)
        self.Run_Button.place(relx=0.087, rely=0.88, height=54, width=97)
        self.Run_Button.configure(activebackground="#ececec", activeforeground="#000000", background="#d9d9d9", disabledforeground="#a3a3a3")
        self.Run_Button.configure(foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Run Simulation''')
        self.Run_Button.bind('<Button-1>', Run_Simulation)
        
        # Exit Button
        self.Exit_Button = Button(top)
        self.Exit_Button.place(relx=0.865, rely=0.88, height=54, width=97)
        self.Exit_Button.configure(activebackground="#ececec", activeforeground="#000000", background="#d9d9d9", disabledforeground="#a3a3a3")
        self.Exit_Button.configure(foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Exit''')
        self.Exit_Button.bind('<Button-1>',Exit)
        
        # First Come, First Serve Radiobutton
        self.Radiobutton1 = Radiobutton(self.Labelframe1)
        self.Radiobutton1.place(relx=0.043, rely=0.129, relheight=0.168, relwidth=0.7, bordermode='ignore')
        self.Radiobutton1.configure(activebackground="#d9d9d9", activeforeground="#000000", background="#d9d9d9", disabledforeground="#a3a3a3")
        self.Radiobutton1.configure(foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left')
        self.Radiobutton1.configure(text='''First Come, First Serve''', variable=selected_algorithm, value="FCFS")
        self.Radiobutton1.bind('<ButtonRelease-1>', Radiobutton_FCFS)
        
        # Priority (Preemptive) Radiobutton
        self.Radiobutton2 = Radiobutton(self.Labelframe1)
        self.Radiobutton2.place(relx=0.048, rely=0.258, relheight=0.161, relwidth=0.657, bordermode='ignore')
        self.Radiobutton2.configure(activebackground="#d9d9d9", activeforeground="#000000", background="#d9d9d9", disabledforeground="#a3a3a3")
        self.Radiobutton2.configure(foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left')
        self.Radiobutton2.configure(text='''Priority (Preemptive)''', variable=selected_algorithm, value="P_P")
        self.Radiobutton2.bind('<ButtonRelease-1>', Radiobutton_P_P)
        
        # Priority (Non-Preemptive) Radiobutton
        self.Radiobutton3 = Radiobutton(self.Labelframe1)
        self.Radiobutton3.place(relx=0.043, rely=0.387, relheight=0.161, relwidth=0.8, bordermode='ignore')
        self.Radiobutton3.configure(activebackground="#d9d9d9", activeforeground="#000000", background="#d9d9d9", disabledforeground="#a3a3a3")
        self.Radiobutton3.configure(foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left')
        self.Radiobutton3.configure(text='''Priority (Non-Preemptive)''', variable=selected_algorithm, value="P_NP")
        self.Radiobutton3.bind('<ButtonRelease-1>', Radiobutton_P_NP)
        
        # Shortest Job First Radiobutton
        self.Radiobutton4 = Radiobutton(self.Labelframe1)
        self.Radiobutton4.place(relx=0.048, rely=0.516, relheight=0.161, relwidth=0.562, bordermode='ignore')
        self.Radiobutton4.configure(activebackground="#d9d9d9", activeforeground="#000000", background="#d9d9d9", disabledforeground="#a3a3a3")
        self.Radiobutton4.configure(foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left')
        self.Radiobutton4.configure(text='''Shortest Job First''', variable=selected_algorithm, value="SJF")
        self.Radiobutton4.bind('<ButtonRelease-1>', Radiobutton_SJF)
        
        # Shortest Remaining Time First Radiobutton
        self.Radiobutton5 = Radiobutton(self.Labelframe1)
        self.Radiobutton5.place(relx=0.043, rely=0.645, relheight=0.161, relwidth=0.895, bordermode='ignore')
        self.Radiobutton5.configure(activebackground="#d9d9d9", activeforeground="#000000", background="#d9d9d9", disabledforeground="#a3a3a3")
        self.Radiobutton5.configure(foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left')
        self.Radiobutton5.configure(text='''Shortest Remaining Time First''', variable=selected_algorithm, value="SRTF")
        self.Radiobutton5.bind('<ButtonRelease-1>', Radiobutton_SRTF)
        
        # Round-Robin Radiobutton
        self.Radiobutton6 = Radiobutton(self.Labelframe1)
        self.Radiobutton6.place(relx=0.048, rely=0.774, relheight=0.161, relwidth=0.471, bordermode='ignore')
        self.Radiobutton6.configure(activebackground="#d9d9d9", activeforeground="#000000", background="#d9d9d9", disabledforeground="#a3a3a3")
        self.Radiobutton6.configure(foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left')
        self.Radiobutton6.configure(text='''Round-Robin''', variable=selected_algorithm, value="RR")
        self.Radiobutton6.bind('<ButtonRelease-1>', Radiobutton_RR)
        
        ##################### End of Buttons & Radiobuttons ####################


        # Number of Processes Spinbox, Input from User
        self.Spinbox = Spinbox(self.Labelframe2, from_=1.0, to=100.0)
        self.Spinbox.place(relx=0.143, rely=0.444, relheight=0.422, relwidth=0.69, bordermode='ignore')
        self.Spinbox.configure(activebackground="#f9f9f9", background="white", buttonbackground="#d9d9d9", disabledforeground="#a3a3a3", font="TkDefaultFont")
        self.Spinbox.configure(foreground="black", highlightbackground="black", highlightcolor="black", insertbackground="black")
        self.Spinbox.configure(selectbackground="#c4c4c4", selectforeground="black")
        # Save the input from user to (processes_count) variable, to be passed to scheduler functions
        self.Spinbox.configure(textvariable=processes_count)

        # Processes Information Text Box, Shows output to user, What to enter now.
        self.TextBox_OP = Text(self.Labelframe3)
        self.TextBox_OP.place(relx=0.029, rely=0.01, relheight=0.25, relwidth=0.952)
        self.TextBox_OP.configure(background="white", foreground="black", font="-family {Segoe UI} -size 10")
        self.TextBox_OP.configure(highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black")
        self.TextBox_OP.configure(selectbackground="#c4c4c4", selectforeground="black", state='disabled', undo="1", wrap="word")
        
        # Processes Information Text Box, to be passed as text to scheduler functions to iterate through
        self.TextBox_IP = Text(self.Labelframe3)
        self.TextBox_IP.place(relx=0.029, rely=0.275, relheight=0.682, relwidth=0.952)
        self.TextBox_IP.configure(background="white", foreground="black", font="-family {Segoe UI} -size 11")
        self.TextBox_IP.configure(highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black")
        self.TextBox_IP.configure(selectbackground="#c4c4c4", selectforeground="black", undo="1", wrap="word")
        self.TextBox_IP.bind("<Return>", Return_button_pressed)
        # self.TextBox_IP.bind("<Control-Key-a>", )  add select all binding, to be implemented
        # self.TextBox_IP.bind("<Control-Key-A>", )
        
        # Separator
        self.Separator = ttk.Separator(top)
        self.Separator.place(relx=0.299, rely=0.018, relheight=0.969)
        self.Separator.configure(orient="vertical")
        

#########################      EOF MainFrame Class     #########################

        
if __name__ == '__main__':
    create_window()





