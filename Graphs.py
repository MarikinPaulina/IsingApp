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

root=tk.Tk()

class Update(object):
    def getTemp(self): return random.randint(0,50)
    def getEnergy(self): return random.randint(50,100)
    def getMagnification(self): return random.randint(100,150)
    
    
class Energy_Frame(tk.Frame):
    def __init__(self,*args,**kwargs):
        tk.Frame.__init__(self,*args,**kwargs)
        self.creat_w()
    
    def creat_w(self):
        self.Energy=[]
        self.Time=[]
        self.figure_energy = plt.Figure(figsize=(3,3), dpi=100,frameon=False)
        self.ax_energy = self.figure_energy.add_subplot(111)
        self.canvas_energy = FigureCanvasTkAgg(self.figure_energy,master=root)     
        self.ax_energy.set_title('Energy in time')
        self.ax_energy.plot(self.Time,self.Energy,marker='', linestyle='solid')
        self.canvas_energy.get_tk_widget().grid(row=0,column=0,sticky="nsew")
       
class Temp_Frame(tk.Frame):
    def __init__(self,*args,**kwargs):
        tk.Frame.__init__(self,*args,**kwargs)
        self.creat_w()
    
    def creat_w(self):
        self.Temp=[]
        self.Time=[]
        self.figure_temp = plt.Figure(figsize=(3,3), dpi=100,frameon=False)
        self.ax_temp = self.figure_temp.add_subplot(111)
        self.canvas_temp= FigureCanvasTkAgg(self.figure_temp,master=root)     
        self.ax_temp.set_title('Temp in time')
        self.ax_temp.plot(self.Time,self.Temp,marker='', linestyle='solid')
        self.canvas_temp.get_tk_widget().grid(row=1,column=0,sticky="nsew")
        
class Mag_Frame(tk.Frame):
    def __init__(self,*args,**kwargs):
        tk.Frame.__init__(self,*args,**kwargs)
        self.creat_w()
    
    def creat_w(self):
        self.Mag=[]
        self.Time=[]
        self.figure_mag = plt.Figure(figsize=(3,3), dpi=100,frameon=False)
        self.ax_mag = self.figure_mag.add_subplot(111)
        self.canvas_mag= FigureCanvasTkAgg(self.figure_mag,master=root)     
        self.ax_mag.set_title('Mag in time')
        self.ax_mag.plot(self.Time,self.Mag,marker='', linestyle='solid')
        self.canvas_mag.get_tk_widget().grid(row=0,column=1,sticky="nsew")
        
class Main(tk.Frame):
    def __init__(self,*args,**kwargs):
        tk.Frame.__init__(self,*args,**kwargs)
        self.creat_w()
    
    def creat_w(self):
        self.last=10
        self.working=False
        
        self.upd=Update()
        
        self.Time=[]
        self.i=0
        
        self.Main_container=tk.Frame(self)
        self.Main_container.pack(side="top",fill="both",expand=True)
        self.Main_container.grid_rowconfigure(0,weight=1)
        self.Main_container.grid_columnconfigure(0,weight=1)
        
        
        self.f_Energy=Energy_Frame(self.Main_container,self)
        self.f_Energy.grid(row=0,column=0,sticky="nsew")
        self.Energy=[]
        self.f_Temp=Temp_Frame(self.Main_container,self)
        self.f_Temp.grid(row=1,column=0,sticky="nsew")
        self.Temp=[]
        self.f_Mag=Mag_Frame(self.Main_container,self)
        self.f_Mag.grid(row=2,column=0,sticky="nsew")
        self.Mag=[]
        
        #self.toolbar=NavigationToolbar2Tk(self.canvas,root)
        #self.toolbar.update()
        
        f1 = tk.Frame(self.Main_container,self,width=400,height=400)
        f1.grid(row=0, column=0,sticky="nsew")
        tk.Label(f1, text="Red", bg="red", fg="white").pack(fill=tk.BOTH)
        tk.Label(f1, text="Green", bg="green", fg="black").pack(fill=tk.BOTH)
        tk.Label(f1, text="Blue", bg="blue", fg="white").pack(fill=tk.BOTH)
        
        f2 = tk.Frame(self.Main_container,self,width=400,height=400)
        f2.grid(row=1, column=1,sticky="nsew")
        tk.Label(f2, text="First").grid(row=0, sticky=tk.W)
        tk.Label(f2, text="Second").grid(row=1, sticky=tk.W)

        e1 = tk.Entry(f2)
        e2 = tk.Entry(f2)
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        plt.ion()
        
        f3 = tk.Frame(self.Main_container,self,width=400,height=400)
        f3.grid(row=2, column=2,sticky="nsew")
        self.plotbutton=tk.Button(f3, text="plot", command=lambda: self.click())
        self.plotbutton.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        
    def click(self):   
        if self.working==False:
            self.working=True
            self.Main_container.after(0,self.update_plot)
            print("Start")
            
        else:
            self.working=False
            print("Stop")
       
        
    def update_plot(self):
        if self.working==True:
            self.f_Energy.ax_energy.clear()
            self.f_Energy.Energy.append(self.upd.getEnergy())
            self.f_Temp.ax_temp.clear()
            self.f_Temp.Temp.append(self.upd.getTemp())
            self.f_Mag.ax_mag.clear()
            self.f_Mag.Mag.append(self.upd.getEnergy())
            self.Time.append(self.i)
            self.i+=1
            En=self.f_Energy.Energy[-self.last:]
            Tm=self.f_Temp.Temp[-self.last:]
            Mg=self.f_Mag.Mag[-self.last:]
            T=self.Time[-self.last:]
            self.f_Energy.ax_energy.plot(T,En,marker='o', linestyle='solid',color="green")
            self.f_Energy.ax_energy.set_title('Energy in time')
            self.f_Energy.canvas_energy.draw()
            self.f_Temp.ax_temp.plot(T,Tm,marker='o', linestyle='solid',color="blue")
            self.f_Temp.ax_temp.set_title('Temp in time')
            self.f_Temp.canvas_temp.draw()
            self.f_Mag.ax_mag.plot(T,Mg,marker='o', linestyle='solid',color="red")
            self.f_Mag.ax_mag.set_title('Temp in time')
            self.f_Mag.canvas_mag.draw()
            
            self.after(0,self.update_plot)
                   
    

#Main(root).pack(side="top",fill="both",expand=True)
root.after(0,Main(root).grid(row=1,column=1,sticky="nsew"))
root.mainloop()
#app=Main(master=root)
#app.mainloop() 