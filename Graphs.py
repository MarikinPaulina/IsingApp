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
    def __init__(self, master, *args,**kwargs):
        tk.Frame.__init__(self, master, *args,**kwargs)
        self.plots_fig, self.plots_ax = plt.subplots(3, 1, figsize=(6, 3), dpi=100, frameon=False)
        self.canvas_energy = FigureCanvasTkAgg(self.figure_energy, master=self)
        self.ax_energy.set_title('Energy in time')
        self.ax_energy.plot([] ,[] ,marker='', linestyle='solid')
        self.canvas_energy.get_tk_widget().grid(row=0,column=0,sticky="nsew")


class Main(tk.Frame):
    def __init__(self, master=None, *args,**kwargs):
        tk.Frame.__init__(self, master, *args,**kwargs)

        self.ising = Simulation.Ising(6)
        self.grid_figure, self.grid_ax = plt.subplots(1, 1, figsize=(3, 3), frameon=False)
        FigureCanvasTkAgg(self.grid_figure, master=self).get_tk_widget().grid(row=0, column=0, sticky='nsew')
        self.imshow = self.grid_ax.imshow(self.ising.spins_board)

        self.last=100
        self.working=False
        
        self.upd=Update()
        
        self.Time=[]
        self.i=0

        # self.Main_container=tk.Frame(self)
        # self.Main_container.pack(side="top",fill="both",expand=True)
        # self.Main_container.grid_rowconfigure(0,weight=1)
        # self.Main_container.grid_columnconfigure(0,weight=1)
        #
        # self.f_Energy=Energy_Frame(self.Main_container,self)
        # self.f_Energy.grid(row=0,column=0,sticky="nsew")
        # self.Energy=[]
        
        # self.toolbar=NavigationToolbar2Tk(self.canvas,root)
        # self.toolbar.update()
        
        control_module = tk.Frame(self,width=400,height=400)
        control_module.grid(row=0, column=1, sticky="nsew")
        tk.Label(control_module, text="Red", bg="red", fg="white").pack(fill=tk.BOTH)
        tk.Label(control_module, text="Green", bg="green", fg="black").pack(fill=tk.BOTH)
        tk.Label(control_module, text="Blue", bg="blue", fg="white").pack(fill=tk.BOTH)
        #
        # f2 = tk.Frame(self.Main_container,self,width=400,height=400)
        # f2.grid(row=1, column=1,sticky="nsew")
        # tk.Label(f2, text="First").grid(row=0, sticky=tk.W)
        # tk.Label(f2, text="Second").grid(row=1, sticky=tk.W)
        #
        # e1 = tk.Entry(f2)
        # e2 = tk.Entry(f2)
        # e1.grid(row=0, column=1)
        # e2.grid(row=1, column=1)
        # plt.ion()

        # f3 = tk.Frame(self,width=400,height=400)
        # f3.grid(row=1, column=1,sticky="nsew")
        self.plotbutton=tk.Button(control_module, text="plot", command=lambda: self.click())
        self.plotbutton.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        
    def click(self):   
        if self.working==False:
            self.working=True
            self.after(0,self.update_plot)
            
        else:
            self.working=False
       
        
    def update_plot(self):
        if self.working:
            self.ising.step()
            self.imshow.set_data(self.ising.spins_board)
            self.grid_figure.canvas.draw()

            # self.f_Energy.ax_energy.clear()
            # self.f_Energy.Energy.append(self.upd.getEnergy())
            self.f_Temp.ax_temp.clear()
            self.f_Temp.Temp.append(self.upd.getTemp())
            self.f_Mag.ax_mag.clear()
            self.f_Mag.Mag.append(self.upd.getEnergy())
            self.Time.append(self.i)
            self.i+=1
            # En=self.f_Energy.Energy[-self.last:]
            Tm=self.f_Temp.Temp[-self.last:]
            Mg=self.f_Mag.Mag[-self.last:]
            T=self.Time[-self.last:]
            # self.f_Energy.ax_energy.plot(T,En,marker='o', linestyle='solid',color="green")
            # self.f_Energy.ax_energy.set_title('Energy in time')
            # self.f_Energy.canvas_energy.draw()
            self.f_Temp.ax_temp.plot(T,Tm,marker='o', linestyle='solid',color="blue")
            self.f_Temp.ax_temp.set_title('Temp in time')
            self.f_Temp.canvas_temp.draw()
            self.f_Mag.ax_mag.plot(T,Mg,marker='o', linestyle='solid',color="red")
            self.f_Mag.ax_mag.set_title('Temp in time')
            self.f_Mag.canvas_mag.draw()
            
            self.after(0,self.update_plot)
                   

if __name__=='__main__':
    #Main(root).pack(side="top",fill="both",expand=True)
    # root.after(0,Main(root).grid(row=1,column=1,sticky="nsew"))
    Main(root).pack()
    root.mainloop()
    #app=Main(master=root)
    #app.mainloop()

