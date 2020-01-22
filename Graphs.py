import tkinter as tk
import numpy as np
import random
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter.ttk as ttk
import sys
import threading
import time
import Simulation

root=tk.Tk()


class Update(object):
    def getTemp(self): return random.randint(0,50)
    def getEnergy(self): return random.randint(50,100)
    def getMagnification(self): return random.randint(100,150)
    
    
class PlotsFrame(tk.Frame):
    def __init__(self, master, last, *args,**kwargs):
        tk.Frame.__init__(self, master, *args,**kwargs)
        self.last = last
        self.i = 0

        self.fig, self.axes = plt.subplots(2, 1, figsize=(6, 3), dpi=100, sharex=True, frameon=False)
        FigureCanvasTkAgg(self.fig, master=master).\
            get_tk_widget().pack(side=tk.BOTTOM, fill="both", expand=True)

        self.plots = {}
        labels = ['E', 'B']
        for i, ax in enumerate(self.axes):
            ax.set_ylabel(labels[i])
            ax.set_autoscale_on(True)
            plot, = ax.plot([], [], '.-')
            self.plots[labels[i]] = plot
        self.axes[-1].set_xlabel('t')

        self.time = []
        self.data = {'E': [],
                     'B': []}

    def update(self, ising):
        self.time.append(self.i)
        self.data['E'].append(ising.energy)
        self.data['B'].append(ising.magnetic_field)
        self.i += 1

        self.data['E'] = self.data['E'][-self.last:]
        self.data['B'] = self.data['B'][-self.last:]
        self.time = self.time[-self.last:]


class Main(tk.Frame):
    def __init__(self, master=None, *args,**kwargs):
        tk.Frame.__init__(self, master, *args,**kwargs)

        last = 100
        self.working = False

        self.Time = []

        self.top_container = tk.Frame(self)
        self.top_container.pack(side="top", fill="both", expand=True)

        self.ising = Simulation.Ising(32)
        self.grid_figure, self.grid_ax = plt.subplots(1, 1, figsize=(3, 3), frameon=False)
        FigureCanvasTkAgg(self.grid_figure, master=self.top_container).\
            get_tk_widget().grid(row=0, column=0, sticky='nsew')
        self.grid_imshow = self.grid_ax.imshow(self.ising.spins_board)

        self.plotsFrame=PlotsFrame(self, last)
        plt.ion()
        
        control_module = tk.Frame(self.top_container, width=400, height=400)
        control_module.grid(row=0, column=1, sticky="nsew")
        tk.Label(control_module, text="Red", bg="red", fg="white").pack(fill=tk.BOTH)
        tk.Label(control_module, text="Green", bg="green", fg="black").pack(fill=tk.BOTH)
        tk.Label(control_module, text="Blue", bg="blue", fg="white").pack(fill=tk.BOTH)
        # tk.Label(control_module, text="First").grid(row=0, sticky=tk.W)
        # tk.Label(control_module, text="Second").grid(row=1, sticky=tk.W)
        # e1 = tk.Entry(control_module)
        # e2 = tk.Entry(control_module)
        # e1.grid(row=0, column=1)
        # e2.grid(row=1, column=1)
        self.plotbutton=tk.Button(control_module, text="plot", command=lambda: self.click())
        self.plotbutton.pack(side=tk.RIGHT, fill=tk.BOTH)

    def click(self):   
        if not self.working:
            self.working=True
            self.after(0,self.update_plot)
        else:
            self.working=False

    def update_plot(self):
        if self.working:
            # actual simulation step
            self.ising.step()
            # updating grid figure
            self.grid_imshow.set_data(self.ising.spins_board)
            self.grid_figure.canvas.draw()
            # updating plots
            self.plotsFrame.update(self.ising)

            # self.f_Energy.ax_energy.clear()
            # self.f_Energy.Energy.append(self.upd.getEnergy())
            # self.f_Temp.ax_temp.clear()
            # self.f_Temp.Temp.append(self.upd.getTemp())
            # self.f_Mag.ax_mag.clear()
            # self.f_Mag.Mag.append(self.upd.getEnergy())
            # self.Time.append(self.i)
            # self.i += 1
            # En = self.f_Energy.Energy[-self.last:]
            # En=self.f_Energy.Energy[-self.last:]
            # Tm = self.f_Temp.Temp[-self.last:]
            # Mg = self.f_Mag.Mag[-self.last:]
            # T = self.Time[-self.last:]
            # self.f_Energy.ax_energy.plot(T, En, marker='o', linestyle='solid', color="green")
            # self.f_Energy.ax_energy.set_title('Energy in time')
            # self.f_Energy.canvas_energy.draw()
            # self.f_Energy.ax_energy.plot(T,En,marker='o', linestyle='solid',color="green")
            # self.f_Energy.ax_energy.set_title('Energy in time')
            # self.f_Energy.canvas_energy.draw()
            # self.f_Temp.ax_temp.plot(T, Tm, marker='o', linestyle='solid', color="blue")
            # self.f_Temp.ax_temp.set_title('Temp in time')
            # self.f_Temp.canvas_temp.draw()


            self.after(0,self.update_plot)
                   

if __name__=='__main__':
    #Main(root).pack(side="top",fill="both",expand=True)
    # root.after(0,Main(root).grid(row=1,column=1,sticky="nsew"))
    Main(root).pack()
    root.mainloop()
    #app=Main(master=root)
    #app.mainloop()

