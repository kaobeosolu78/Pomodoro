import tkinter as tk
from tkinter import ttk
import time as t
from playsound import playsound
import pickle
from historical_poms import pom_history
import datetime

# Attempt at replicating a pomodoro timer in code.

# func for loading pickled objects
def load_obj(datatype):
    with open("{}".format(datatype) + '.pkl', 'rb') as f:
        return pickle.load(f)

# main class for mechanics
class pomgui(tk.Tk):
    def __init__(self):
        pass

    # the timer method, when called increments time down one and changes the gui label
    def timer(self,time=None):
        if time == None: time = self.time
        if time:
            if self.pause_val == True:self.time = time
            else:
                self.time = time - 1
                self.tot_time += 1

            # subtracts one from time and converts to min;sec
            mins,secs = divmod(self.time,60)
            totmins,totsecs = divmod(self.tot_time,60)
            # changes label
            self.tot_time_label["text"] = "{:02d}:{:02d}".format(totmins,totsecs)
            self.time_label["text"] = "{:02d}:{:02d}".format(mins,secs)
            self.update_idletasks()
            self.after(1000, lambda: self.timer())
        else:
            self.wait.set(self.wait.get()+1)
            return

    # initiates the timer, one iteration is a full 'pomodore'
    def begin_pom(self,repeat=1):
        # remove unneeded button
        try:self.startbutton.grid_forget()
        except:pass
        # conditional that ends if more than 8 pomodores have passed
        if self.iteration < repeat*int(self.options["iterations"]):

            # conditional to switch the length of the break
            if self.iteration > repeat*int(self.options["break_iterations"]):
                self.breaktime = "long"
            ## order for the pomodore
            self.t_label["text"] = "Current Work Time Remaining:"
            # calls work timer
            self.work_on_work()
            # pauses loop while timer is going
            self.wait = tk.IntVar(0)
            self.wait_variable(self.wait)
            playsound("work.mp3")
            self.t_label["text"] = "Current Rest Time Remaining:"
            # calls break timer
            self.take_break()
            self.wait_variable(self.wait)
            playsound("break.mp3")
            # increment iterator
            self.iteration += 1
            self.iter_label["text"] = self.iteration
            self.after(1,lambda: self.begin_pom(repeat))
        else:
            self.pause("pause")
            q_win = tk.Toplevel(self)
            q_win.title("Quit?")
            ttk.Label(q_win, text="Would You Like to Quit or Continue Working?").grid(row=0,column=0)
            ttk.Button(q_win, text="Quit", command=lambda:(self.quit(),q_win.destroy())).grid(row=1,column=0)
            ttk.Button(q_win, text="Continue", command=lambda:(self.pause("unpause"),self.begin_pom(2),q_win.destroy())).grid(row=1,column=1)

    # handles break length
    def take_break(self):
        if self.breaktime == "short":
            self.timer(60*int(self.options["breaktime_s"]))
        elif self.breaktime == "long":
            self.timer(60*int(self.options["breaktime_l"]))

    # handles work time
    def work_on_work(self):
        self.timer(60*int(self.options["worktime"]))

    def quit(self):
        def submit(self,assns,listb,entry):
            if listb.curselection() != ():self.history.add_new(datetime.date.today(),(assns[listb.curselection()[0]],self.iteration,self.tot_time))
            elif entry:self.history.add_new(datetime.date.today(),(entry,self.iteration,self.tot_time))
            (self.destroy(),exit())


        if self.tot_time == 0:(self.destroy(),exit())

        self.history.add_new(datetime.date.today(),("homework",3,50))##
        temp_win = tk.Toplevel(self)
        temp_win.title("Assignment Name")
        ttk.Label(temp_win,text="Enter The Assignment Name or Choose Existing Assignment:").grid(row=0,column=0)
        lb = tk.Listbox(temp_win)
        lb.grid(row=1,column=0)
        assns = []
        [(lb.insert(tk.END,assn),assns.append(assn)) for assn in self.history.get_assns()]
        en = ttk.Entry(temp_win)
        en.grid(row=2,column=0)
        ttk.Button(temp_win,text="Submit",command=lambda:submit(self,assns,lb,en.get())).grid(row=3,column=0)

    def pause(self,status):
        if status == "pause":
            self.pause_val = True
            self.pausebutton["text"] = "Resume Timer"
            self.pausebutton["command"] = lambda: self.pause("unpause")
        elif status == "unpause":
            self.pause_val = False
            self.pausebutton["text"] = "Pause Timer"
            self.pausebutton["command"] = lambda: self.pause("pause")


# class options gui
class start(pomgui):
    def __init__(self):
        # loads options if available else sets default
        try:
            self.options = load_obj("options")
        except:
            self.options = {"worktime":25,"breaktime_l":20,"breaktime_s":5,"iterations":8,"break_iterations":4}
            pickle_out = open("options.pkl", 'wb')
            pickle.dump(self.options, pickle_out, pickle.HIGHEST_PROTOCOL)
            pickle_out.close()
        # load/create work history file
        try:
            self.history = load_obj("history")
        except:
            self.history = pom_history()
            pickle_out = open("history.pkl", 'wb')
            pickle.dump(self.history, pickle_out, pickle.HIGHEST_PROTOCOL)
            pickle_out.close()
        # initialize main window
        tk.Tk.__init__(self)
        self.grid()
        # self.geometry("800x350+200+200")
        self.title("Pomodoro")
        self.iteration, self.breaktime = 1, "short"
        ttk.Label(self, text="Pomodoro Iteration:").grid(row=0, column=0,sticky="W")

        # adds labels and buttons for mainwin #
        # labels
        self.t_label = ttk.Label(self, text="Current Work Time Remaining:")
        self.t_label.grid(row=2, column=0,sticky="W")
        self.tot_time_label = ttk.Label(self,text="00:00")
        self.tot_time_label.grid(row=3,column=1,pady=2)

        ttk.Label(self,text="Total Time:").grid(row=3,column=0,sticky="W")
        self.tot_time = 0
        self.time_label = ttk.Label(self, text="")
        self.time_label.grid(row=2, column=1,pady=3)

        self.iter_label = ttk.Label(self, text=self.iteration)
        self.iter_label.grid(row=0, column=1,pady=3)

        # buttons
        ttk.Button(self,text="Quit",command=lambda:(self.pause("pause"),self.quit())).grid(row=4,column=0)
        self.startbutton = ttk.Button(self,text="Start Timer",command=self.begin_pom)
        self.startbutton.grid(row=4,column=1)
        self.pausebutton = ttk.Button(self,text="Pause Timer",command=lambda: self.pause("pause"))
        self.pausebutton.grid(row=4,column=2)
        self.pause_val = False

        # adds option menu
        menubar = tk.Menu(self)
        optionmenu = tk.Menu(menubar, tearoff=0)
        optionmenu.add_command(label="Modify Times", command= self.mod_times)
        optionmenu.add_command(label="Modify Iteration Count", command= self.mod_iter)
        menubar.add_cascade(label="Options", menu=optionmenu)

        # adds history menu
        histmenu = tk.Menu(menubar,tearoff=0)
        histmenu.add_command(label="Clear History",command=self.clear_hist)
        histmenu.add_command(label="Display History",command=self.history.display_assns)
        menubar.add_cascade(label="History",menu=histmenu)
        tk.Tk.config(self, menu=menubar) ############ maybe hook up with school program, historical data menu and formatting


    # menu for modifying total iteration count and break iterations
    def mod_iter(self):
        def set_times(self,ti,sbi,opt_win):
            self.options["iterations"] = ti
            self.options["break_iterations"] = sbi
            pickle_out = open("options.pkl", 'wb')
            pickle.dump(self.options, pickle_out, pickle.HIGHEST_PROTOCOL)
            pickle_out.close()
            opt_win.destroy()

        opt_win = tk.Toplevel(self)
        opt_win.title("Iteration Settings")
        (ttk.Label(opt_win,text="Total Number of Iterations:").grid(row=0,column=0),ttk.Label(opt_win,text="Iterations Before Shortened Break:").grid(row=1,column=0))
        ti,sbi = tk.Entry(opt_win),tk.Entry(opt_win)
        (ti.grid(row=0,column=1),sbi.grid(row=1,column=1))
        (ti.insert(tk.END,self.options["iterations"]),sbi.insert(tk.END,self.options["break_iterations"]))
        ttk.Button(opt_win,text="Submit",command=lambda: set_times(self,ti.get(),sbi.get(),opt_win)).grid(row=2,column=0)
        ttk.Button(opt_win,text="Reset to Defaults", command=lambda: set_times(self,8,4,opt_win)).grid(row=2,column=1)


    # modify times menu
    def mod_times(self):
        # submits the desired time options and exits menu
        def set_times(self,wt,btl,bts,opt_win):
            # sets the options
            self.options["worktime"] = wt
            self.options["breaktime_l"] = btl
            self.options["breaktime_s"] = bts
            # saves the options as a pkl file
            pickle_out = open("options.pkl", 'wb')
            pickle.dump(self.options, pickle_out, pickle.HIGHEST_PROTOCOL)
            pickle_out.close()
            # close out window
            opt_win.destroy()
            return
        # initiates time option win
        opt_win = tk.Toplevel(self)
        opt_win.title("Time Settings")
        # adds labels and entryboxes which are autofilled
        (ttk.Label(opt_win,text="Work Time:").grid(row=0,column=0),ttk.Label(opt_win,text="Break Time(Long):").grid(row=1,column=0),ttk.Label(opt_win,text="Break Time(Short):").grid(row=2,column=0))
        wt,btl,bts=tk.Entry(opt_win),tk.Entry(opt_win),tk.Entry(opt_win)
        (wt.grid(row=0,column=1),btl.grid(row=1,column=1),bts.grid(row=2,column=1))
        (wt.insert(tk.END,self.options["worktime"]),btl.insert(tk.END,self.options["breaktime_l"]),bts.insert(tk.END,self.options["breaktime_s"]))
        # buttons which call function to submit
        ttk.Button(opt_win,text="Submit",command=lambda: set_times(self,wt.get(),btl.get(),bts.get(),opt_win)).grid(row=3,column=0)
        ttk.Button(opt_win,text="Reset to Defaults",command=lambda: set_times(self,25,20,5,opt_win)).grid(row=3,column=1)

    def clear_hist(self):
        self.history = {}
        pickle_out = open("history.pkl", 'wb')
        pickle.dump(self.history, pickle_out, pickle.HIGHEST_PROTOCOL)
        pickle_out.close()

gui = start()
gui.mainloop()