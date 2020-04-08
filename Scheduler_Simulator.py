#! /usr/bin/env python  
#  -*- coding: utf-8 -*-    # Defining Python Source Code Encodings
'''
    The first line is a shebang, it tells the program loader that this script
    is executed with python, so you don't have to type python before running
    the .py file.
    In Unix-like operating systems, when a text file has a shebang, it is 
    interpreted as an executable file
'''
########################## IMPORTS ###########################
import sys
import os
import subprocess

import Scheduler_Functions

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

def create_window():
    global root, top
    root = Tk()              # creating a tkinter window
    set_Tk_var()             # setting variables used in the gui
    top = MainFrame(root)    # building the gui
    root.mainloop()          # infinite loop


def destroy_window():        # called when Exit button is pressed to just Exit :D
    root.destroy()
        
def Exit(b):
    destroy_window()

def enter_button_pressed(b):
    # set the tkinter variable to anything to get out of the wait_variable() local loop
    bool.set(0)
    
    
def set_Tk_var():
    global selected_algorithm # Radiobutton Variable for selected scheduling algorithm
    global processes_count    # Number of processes input by user from spinbox 
    global AvgTime            # Average Time
    
    selected_algorithm = StringVar()
    selected_algorithm.set("FCFS")  # FCFS scheduling algorithm is selected by default
    
    AvgTime = StringVar()
    AvgTime.set('0.0')
    
    processes_count = StringVar()
    processes_count.set('1')
    
    global bool
    bool = IntVar()
    bool.set(0)


def Run_Simulation(b):
    print("Run Simulation Clicked") 
    sys.stdout.flush()
    print(selected_algorithm.get())
    
    # testing SJF 
    if selected_algorithm.get() == 'SJF':
        Ask_For_and_Get_Input('SJF')
        # Extract_Processes_Information('SJF')  # will return arrival_time & burst_time
        # SJF(processes_count, )
    
    ''' uncomment when scheduling functions are finished
        pass number of processes and processes information to functions
    
    if selected_algorithm.get() == 'FCFS':
        Ask_For_and_Get_Input('FCFS')
        Extract_Processes_Information('FCFS')
        FCFS(processes_count, )
    elif selected_algorithm.get() == 'P_P':
        Ask_For_and_Get_Input('P_P')
        Extract_Processes_Information('P_P')
        P_P(processes_count, )
    elif selected_algorithm.get() == 'P_NP':
        Ask_For_and_Get_Input('P_NP')
        Extract_Processes_Information('P_NP')
        P_NP(processes_count, )
    elif selected_algorithm.get() == 'SJF':
        Ask_For_and_Get_Input('SJF')
        Extract_Processes_Information('SJF')  # will return arrival_time & burst_time
        SJF(processes_count, )
    elif selected_algorithm.get() == 'SRTF':
        Ask_For_and_Get_Input('SRTF')
        Extract_Processes_Information('SRTF')
        SRTF(processes_count, )
    elif selected_algorithm.get() == 'RR':
        Ask_For_and_Get_Input('RR')
        Extract_Processes_Information('RR')
        RR(processes_count, )
    '''

def Ask_For_and_Get_Input(algorithm):
   
    # testing SJF
    if algorithm == 'SJF':
        Arrival_Times = list()
        Burst_Times = list()
        for i in range(int(processes_count.get())):
            # Prepare text boxes
            top.TextBox_OP.configure(state='normal')
            top.TextBox_OP.delete('1.0', 'end')
            top.TextBox_OP.insert('1.0', "In the Box below, Please enter the Arrival Time of process {}, then press Enter : ".format(i+1))
            top.TextBox_OP.configure(state='disabled')
            top.TextBox_IP.configure(state='normal')
            top.TextBox_IP.delete('1.0', 'end')            
            top.TextBox_OP.wait_variable(bool)  # wait foor user to press enter in a local loop 
            
            # add input text to Arrival_Times list
            Arrival_Times.append(top.TextBox_IP.get('1.0', 'end').replace('\n', ''))
            
            
        for i in range(int(processes_count.get())):
            # Prepare text boxes
            top.TextBox_OP.configure(state='normal')
            top.TextBox_OP.delete('1.0', 'end')
            top.TextBox_OP.insert('1.0', "In the Box below, Please enter the Burst Time of process {}, then press Enter : ".format(i+1))
            top.TextBox_OP.configure(state='disabled')
            top.TextBox_IP.configure(state='normal')
            top.TextBox_IP.delete('1.0', 'end')            
            top.TextBox_OP.wait_variable(bool)  # wait foor user to press enter in a local loop 
            
            # add input text to Arrival_Times list
            Burst_Times.append(top.TextBox_IP.get('1.0', 'end').replace('\n', ''))
        
        # for i in range(int(processes_count.get())):
            # print(Arrival_Times[i])

        # for i in range(int(processes_count.get())):
            # print(Burst_Times[i])

    '''
    if algorithm == 'FCFS':
        
    elif algorithm == 'P_P':
       
    elif algorithm == 'P_NP':
       
    elif algorithm == 'SJF':
        
    elif algorithm == 'SRTF':
 
    elif algorithm == 'RR':
       
    '''
    # return ...


####################### MainFrame Class #######################
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

        top.geometry("802x557+1692+104")
        top.minsize(120, 1)
        top.maxsize(2970, 881)
        top.resizable(0, 0)
        top.title("Scheduler Simulator حلو وبالسمسم")
        top.configure(background="#000655")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        top.configure(cursor="top_left_arrow")


        ################## Labels, Label Frames & Canvases ##################
        
        # Scheduling Algorithm Label Frame
        self.Labelframe1 = LabelFrame(top)
        self.Labelframe1.place(relx=0.012, rely=0.018, relheight=0.278, relwidth=0.262)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''Scheduling Algorithm''')
        self.Labelframe1.configure(background="#d9d9d9")
        self.Labelframe1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1.configure(highlightcolor="black")
        
        # Number of Processes Label Frame
        self.Labelframe2 = LabelFrame(top)
        self.Labelframe2.place(relx=0.012, rely=0.305, relheight=0.081, relwidth=0.262)
        self.Labelframe2.configure(relief='groove')
        self.Labelframe2.configure(foreground="black")
        self.Labelframe2.configure(text='''Number of Processes''')
        self.Labelframe2.configure(background="#d9d9d9")
        self.Labelframe2.configure(highlightbackground="#d9d9d9")
        self.Labelframe2.configure(highlightcolor="black")

        # Processes Information Label Frame
        self.Labelframe3 = LabelFrame(top)
        self.Labelframe3.place(relx=0.012, rely=0.395, relheight=0.458, relwidth=0.262)
        self.Labelframe3.configure(relief='groove')
        self.Labelframe3.configure(foreground="black")
        self.Labelframe3.configure(text='''Processes Information''')
        self.Labelframe3.configure(background="#d9d9d9")
        self.Labelframe3.configure(highlightbackground="#d9d9d9")
        self.Labelframe3.configure(highlightcolor="black")
         
        # Gantt Chart Label Frame
        self.Labelframe4 = LabelFrame(top)         
        self.Labelframe4.place(relx=0.324, rely=0.018, relheight=0.853, relwidth=0.661)
        self.Labelframe4.configure(relief='groove')
        self.Labelframe4.configure(foreground="black")
        self.Labelframe4.configure(text='''Gantt Chart''')
        self.Labelframe4.configure(background="#d9d9d9")
        self.Labelframe4.configure(highlightbackground="#d9d9d9")
        self.Labelframe4.configure(highlightcolor="black")
        
        # Show Gantt Chart on this Canvas
        self.Canvas = Canvas(top)                    
        self.Canvas.place(relx=0.337, rely=0.054, relheight=0.795, relwidth=0.64)
        self.Canvas.configure(background="#ffffff")
        self.Canvas.configure(borderwidth="5")
        self.Canvas.configure(highlightbackground="#d9d9d9")
        self.Canvas.configure(highlightcolor="black")
        self.Canvas.configure(insertbackground="black")
        self.Canvas.configure(relief="groove")
        self.Canvas.configure(selectbackground="#c4c4c4")
        self.Canvas.configure(selectforeground="black")

        # Average Waiting Time Label Frame
        self.Labelframe5 = LabelFrame(top)          
        self.Labelframe5.place(relx=0.324, rely=0.88, relheight=0.099, relwidth=0.187)
        self.Labelframe5.configure(relief='groove')
        self.Labelframe5.configure(foreground="black")
        self.Labelframe5.configure(text='''Average Waiting Time''')
        self.Labelframe5.configure(background="#d9d9d9")
        self.Labelframe5.configure(highlightbackground="#d9d9d9")
        self.Labelframe5.configure(highlightcolor="black")
        
        # Average Waiting Time Label
        self.AvgTime_Label = Label(self.Labelframe5)
        self.AvgTime_Label.place(relx=0.067, rely=0.364, height=31, width=130, bordermode='ignore')
        self.AvgTime_Label.configure(background="#ffffff")
        self.AvgTime_Label.configure(disabledforeground="#a3a3a3")
        self.AvgTime_Label.configure(foreground="#000000")
        # Import Average Time from scheduler functions to (AvgTime) variable 
        self.AvgTime_Label.configure(textvariable=AvgTime)     
                                             
        ################## End of Labels, Label Frames & Canvases ##################   


        ########################## Buttons & Radiobuttons #########################
        
        # Run Simulation Button
        self.Run_Button = Button(top)
        self.Run_Button.place(relx=0.087, rely=0.88, height=54, width=97)
        self.Run_Button.configure(activebackground="#ececec")
        self.Run_Button.configure(activeforeground="#000000")
        self.Run_Button.configure(background="#d9d9d9")
        self.Run_Button.configure(disabledforeground="#a3a3a3")
        self.Run_Button.configure(foreground="#000000")
        self.Run_Button.configure(highlightbackground="#d9d9d9")
        self.Run_Button.configure(highlightcolor="black")
        self.Run_Button.configure(pady="0")
        self.Run_Button.configure(text='''Run Simulation''')
        self.Run_Button.bind('<Button-1>', lambda b1:Run_Simulation(b1))
        
        # Exit Button
        self.Exit_Button = Button(top)
        self.Exit_Button.place(relx=0.865, rely=0.88, height=54, width=97)
        self.Exit_Button.configure(activebackground="#ececec")
        self.Exit_Button.configure(activeforeground="#000000")
        self.Exit_Button.configure(background="#d9d9d9")
        self.Exit_Button.configure(disabledforeground="#a3a3a3")
        self.Exit_Button.configure(foreground="#000000")
        self.Exit_Button.configure(highlightbackground="#d9d9d9")
        self.Exit_Button.configure(highlightcolor="black")
        self.Exit_Button.configure(pady="0")
        self.Exit_Button.configure(text='''Exit''')
        self.Exit_Button.bind('<Button-1>', lambda b1:Exit(b1))
        
        # First Come, First Serve Radiobutton
        self.Radiobutton1 = Radiobutton(self.Labelframe1)
        self.Radiobutton1.place(relx=0.043, rely=0.129, relheight=0.168, relwidth=0.7, bordermode='ignore')
        self.Radiobutton1.configure(activebackground="#d9d9d9")
        self.Radiobutton1.configure(activeforeground="#000000")
        self.Radiobutton1.configure(background="#d9d9d9")
        self.Radiobutton1.configure(disabledforeground="#a3a3a3")
        self.Radiobutton1.configure(foreground="#000000")
        self.Radiobutton1.configure(highlightbackground="#d9d9d9")
        self.Radiobutton1.configure(highlightcolor="black")
        self.Radiobutton1.configure(justify='left')
        self.Radiobutton1.configure(offrelief="groove")
        self.Radiobutton1.configure(selectcolor="#ffffff")
        self.Radiobutton1.configure(text='''First Come, First Serve''')
        self.Radiobutton1.configure(variable=selected_algorithm)
        self.Radiobutton1.configure(value="FCFS")
        
        # Priority (Preemptive) Radiobutton
        self.Radiobutton2 = Radiobutton(self.Labelframe1)
        self.Radiobutton2.place(relx=0.048, rely=0.258, relheight=0.161, relwidth=0.657, bordermode='ignore')
        self.Radiobutton2.configure(activebackground="#d9d9d9")
        self.Radiobutton2.configure(activeforeground="#000000")
        self.Radiobutton2.configure(background="#d9d9d9")
        self.Radiobutton2.configure(disabledforeground="#a3a3a3")
        self.Radiobutton2.configure(foreground="#000000")
        self.Radiobutton2.configure(highlightbackground="#d9d9d9")
        self.Radiobutton2.configure(highlightcolor="black")
        self.Radiobutton2.configure(justify='left')
        self.Radiobutton2.configure(text='''Priority (Preemptive)''')
        self.Radiobutton2.configure(variable=selected_algorithm)
        self.Radiobutton2.configure(value="P_P")
        
        # Priority (Non-Preemptive) Radiobutton
        self.Radiobutton3 = Radiobutton(self.Labelframe1)
        self.Radiobutton3.place(relx=0.043, rely=0.387, relheight=0.161, relwidth=0.8, bordermode='ignore')
        self.Radiobutton3.configure(activebackground="#d9d9d9")
        self.Radiobutton3.configure(activeforeground="#000000")
        self.Radiobutton3.configure(background="#d9d9d9")
        self.Radiobutton3.configure(disabledforeground="#a3a3a3")
        self.Radiobutton3.configure(foreground="#000000")
        self.Radiobutton3.configure(highlightbackground="#d9d9d9")
        self.Radiobutton3.configure(highlightcolor="black")
        self.Radiobutton3.configure(justify='left')
        self.Radiobutton3.configure(text='''Priority (Non-Preemptive)''')
        self.Radiobutton3.configure(variable=selected_algorithm)
        self.Radiobutton3.configure(value="P_NP")
        
        # Shortest Job First Radiobutton
        self.Radiobutton4 = Radiobutton(self.Labelframe1)
        self.Radiobutton4.place(relx=0.048, rely=0.516, relheight=0.161, relwidth=0.562, bordermode='ignore')
        self.Radiobutton4.configure(activebackground="#d9d9d9")
        self.Radiobutton4.configure(activeforeground="#000000")
        self.Radiobutton4.configure(background="#d9d9d9")
        self.Radiobutton4.configure(disabledforeground="#a3a3a3")
        self.Radiobutton4.configure(foreground="#000000")
        self.Radiobutton4.configure(highlightbackground="#d9d9d9")
        self.Radiobutton4.configure(highlightcolor="black")
        self.Radiobutton4.configure(justify='left')
        self.Radiobutton4.configure(text='''Shortest Job First''')
        self.Radiobutton4.configure(variable=selected_algorithm)
        self.Radiobutton4.configure(value="SJF")
        
        # Shortest Remaining Time First Radiobutton
        self.Radiobutton5 = Radiobutton(self.Labelframe1)
        self.Radiobutton5.place(relx=0.043, rely=0.645, relheight=0.161, relwidth=0.895, bordermode='ignore')
        self.Radiobutton5.configure(activebackground="#d9d9d9")
        self.Radiobutton5.configure(activeforeground="#000000")
        self.Radiobutton5.configure(background="#d9d9d9")
        self.Radiobutton5.configure(disabledforeground="#a3a3a3")
        self.Radiobutton5.configure(foreground="#000000")
        self.Radiobutton5.configure(highlightbackground="#d9d9d9")
        self.Radiobutton5.configure(highlightcolor="black")
        self.Radiobutton5.configure(justify='left')
        self.Radiobutton5.configure(text='''Shortest Remaining Time First''')
        self.Radiobutton5.configure(variable=selected_algorithm)
        self.Radiobutton5.configure(value="SRTF")
        
        # Round-Robin Radiobutton
        self.Radiobutton6 = Radiobutton(self.Labelframe1)
        self.Radiobutton6.place(relx=0.048, rely=0.774, relheight=0.161, relwidth=0.471, bordermode='ignore')
        self.Radiobutton6.configure(activebackground="#d9d9d9")
        self.Radiobutton6.configure(activeforeground="#000000")
        self.Radiobutton6.configure(background="#d9d9d9")
        self.Radiobutton6.configure(disabledforeground="#a3a3a3")
        self.Radiobutton6.configure(foreground="#000000")
        self.Radiobutton6.configure(highlightbackground="#d9d9d9")
        self.Radiobutton6.configure(highlightcolor="black")
        self.Radiobutton6.configure(justify='left')
        self.Radiobutton6.configure(text='''Round-Robin''')
        self.Radiobutton6.configure(variable=selected_algorithm)
        self.Radiobutton6.configure(value="RR")
        
        ###################### End of Buttons & Radiobuttons #####################


        # Number of Processes Spinbox, Input from User
        self.Spinbox = Spinbox(self.Labelframe2, from_=1.0, to=100.0)
        self.Spinbox.place(relx=0.143, rely=0.444, relheight=0.422, relwidth=0.69, bordermode='ignore')
        self.Spinbox.configure(activebackground="#f9f9f9")
        self.Spinbox.configure(background="white")
        self.Spinbox.configure(buttonbackground="#d9d9d9")
        self.Spinbox.configure(disabledforeground="#a3a3a3")
        self.Spinbox.configure(font="TkDefaultFont")
        self.Spinbox.configure(foreground="black")
        self.Spinbox.configure(highlightbackground="black")
        self.Spinbox.configure(highlightcolor="black")
        self.Spinbox.configure(insertbackground="black")
        self.Spinbox.configure(selectbackground="#c4c4c4")
        self.Spinbox.configure(selectforeground="black")
        # Save the input from user to (processes_count) variable, to be passed to scheduler functions
        self.Spinbox.configure(textvariable=processes_count)

        # Processes Information Text Box, Shows output to user, What to enter now.
        self.TextBox_OP = Text(self.Labelframe3)
        self.TextBox_OP.place(relx=0.029, rely=0.01, relheight=0.25, relwidth=0.952)
        self.TextBox_OP.configure(background="white")
        self.TextBox_OP.configure(font="-family {Segoe UI} -size 10")
        self.TextBox_OP.configure(foreground="black")
        self.TextBox_OP.configure(highlightbackground="#d9d9d9")
        self.TextBox_OP.configure(highlightcolor="black")
        self.TextBox_OP.configure(insertbackground="black")
        self.TextBox_OP.configure(selectbackground="#c4c4c4")
        self.TextBox_OP.configure(selectforeground="black")
        self.TextBox_OP.configure(state='disabled')
        self.TextBox_OP.configure(undo="1")
        self.TextBox_OP.configure(wrap="word")
        
        # Processes Information Text Box, to be passed as text to scheduler functions to iterate through
        self.TextBox_IP = Text(self.Labelframe3)
        self.TextBox_IP.place(relx=0.029, rely=0.275, relheight=0.682, relwidth=0.952)
        self.TextBox_IP.configure(background="white")
        self.TextBox_IP.configure(font="-family {Segoe UI} -size 11")
        self.TextBox_IP.configure(foreground="black")
        self.TextBox_IP.configure(highlightbackground="#d9d9d9")
        self.TextBox_IP.configure(highlightcolor="black")
        self.TextBox_IP.configure(insertbackground="black")
        self.TextBox_IP.configure(selectbackground="#c4c4c4")
        self.TextBox_IP.configure(selectforeground="black")
        self.TextBox_IP.configure(undo="1")
        self.TextBox_IP.configure(wrap="word")
        self.TextBox_IP.bind("<Return>", enter_button_pressed)
        # self.TextBox_IP.bind("<Control-Key-a>", )  add select all binding, to be implemented
        # self.TextBox_IP.bind("<Control-Key-A>", )

        
        # Separator
        self.Separator = ttk.Separator(top)
        self.Separator.place(relx=0.299, rely=0.018, relheight=0.969)
        self.Separator.configure(orient="vertical")
        

####################### EOF MainFrame Class #######################

        
if __name__ == '__main__':
    create_window()





