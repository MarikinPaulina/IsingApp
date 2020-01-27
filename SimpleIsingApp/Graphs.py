import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from SimpleIsingApp import Simulation

root=tk.Tk()


class PlotsFrame(tk.Frame):
    def __init__(self, master, last, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.last = last
        self.i = 0

        self.fig, self.axes = plt.subplots(2, 1, figsize=(6, 3), dpi=100, sharex=True, frameon=False)
        FigureCanvasTkAgg(self.fig, master=master). \
            get_tk_widget().pack(side=tk.BOTTOM, fill="both", expand=True)
        self.plots = {}
        self.labels = ['E', 'B']
        for i, ax in enumerate(self.axes):
            ax.set_ylabel(self.labels[i])
            ax.set_autoscale_on(True)
            plot, = ax.plot([], [], '.-')
            self.plots[self.labels[i]] = plot

        self.axes[-1].set_xlabel('t')

        self.time = []
        self.data = {'E': [],
                     'B': []}

    def update(self, ising):
        for i, ax in enumerate(self.axes):
            ax.clear()
            ax.set_ylabel(self.labels[i])
        self.time.append(self.i)
        self.data['E'].append(ising.energy)
        self.data['B'].append(ising.magnetization)
        self.i += 1
        self.data['E'] = self.data['E'][-self.last:]
        self.data['B'] = self.data['B'][-self.last:]
        self.time = self.time[-self.last:]
        self.axes[0].plot(self.time, self.data['E'], marker='o', linestyle='solid', color="green")
        self.axes[1].plot(self.time, self.data['B'], marker='o', linestyle='solid', color="red")


class SpinsGrid(tk.Frame):
    def __init__(self, master, ising, *args,**kwargs):
        tk.Frame.__init__(self, master, *args,**kwargs)

        self.figure, self.ax = plt.subplots(1, 1, figsize=(3, 3), frameon=False)
        FigureCanvasTkAgg(self.figure, master=master). \
            get_tk_widget().grid(row=0, column=0, sticky='nsew')
        self.imshow = self.ax.imshow(ising.spins_board,
                                     vmin=-1,   # default: spins_board.min(),
                                     vmax=1,    # default: spins_board.max(),
                                     )

    def update(self, ising):
        self.imshow.set_data(ising.spins_board)
        self.figure.canvas.draw()


class Main(tk.Frame):
    def __init__(self, master=None, *args,**kwargs):
        tk.Frame.__init__(self, master, *args,**kwargs)

        last = 100
        self.working = False

        self.Time = []
        self.N = 32
        self.top_container = tk.Frame(self)
        self.top_container.pack(side="top", fill="both", expand=True)

        self.ising = Simulation.Ising(32)
        self.spins_grid = SpinsGrid(self.top_container, self.ising)
        self.spins_grid.grid(row=0, column=1, sticky="nsew")

        self.plotsFrame=PlotsFrame(self, last)
        plt.ion()

        control_module = tk.Frame(self.top_container, width=400, height=400)
        control_module.grid(row=0, column=1, sticky="nsew")
        f2 = tk.Frame(control_module, width=400, height=400)
        f2.pack(side=tk.TOP, fill=tk.X)

        # Ustawienie tekstow parametrow razem z wypisaniem obecnych wartowsci
        temp = "Temp: " + str("%.2f" % (self.ising.T))
        self.templabel = tk.Label(f2, text=temp).grid(row=0, column=0, sticky=tk.W, padx=20, pady=20)
        Mag = "Outside_Mag: " + str("%.2f" % (self.ising.outM))
        self.maglabel = tk.Label(f2, text=Mag).grid(row=1, column=0, sticky=tk.W, padx=20, pady=20)
        N = "N: " + str(self.N)
        self.Nlabel = tk.Label(f2, text=N).grid(row=2, column=0, sticky=tk.W, padx=20, pady=20)

        self.e1 = tk.Entry(f2)
        self.e2 = tk.Entry(f2)
        self.e3 = tk.Entry(f2)
        self.e1.grid(row=0, column=1, padx=40, pady=20)
        self.e2.grid(row=1, column=1, padx=40, pady=20)
        self.e3.grid(row=2, column=1, padx=40, pady=20)

        # ErrorLabel, w przypadku wpisania zlej wartosci
        self.errortext = ""
        self.errorlabel = tk.Label(control_module, text=self.errortext).pack(side=tk.TOP, fill=tk.X, padx=20, pady=0)

        # Przyciski
        self.setbutton = tk.Button(control_module, text="Set New Parameters", command=lambda: self.set_new_parameters())
        self.setbutton.pack(side=tk.TOP, fill=tk.X, padx=20, pady=20)
        self.plotbutton = tk.Button(control_module, text="Plot", command=lambda: self.click())
        self.plotbutton.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

    def click(self):   
        if not self.working:
            self.working=True
            self.after(0,self.update_plot)
        else:
            self.working=False

    def set_new_parameters(self):
        #if isinstance(self.e1.cget("text"),int):
        #    self.errorlabel['text']=self.e1.cget("text")
        print(type(self.e1.cget("text")))
        #else:
        self.errortext="NOPE"

    def update_plot(self):
        if self.working:
            # actual simulation step
            self.ising.step()
            # updating grid figure
            self.spins_grid.update(self.ising)
            # updating plots
            self.plotsFrame.update(self.ising)

            self.after(0,self.update_plot)
                   
def main_entrypoint():
    #Main(root).pack(side="top",fill="both",expand=True)
    # root.after(0,Main(root).grid(row=1,column=1,sticky="nsew"))
    Main(root).pack()
    root.mainloop()
    #app=Main(master=root)
    #app.mainloop()


if __name__=='__main__':
    main_entrypoint()
