## IsingApp
Small app in Python with simulation of Ising model on 
square lattice made for university project.
Simulation uses Metropolis-Hasting algorithm 
(Markov chain Monte Carlo method).

## Installation 

Program requires python at least 3.6 to run.
Install by typing: 
```
pip install git+https://github.com/MarikinPaulina/IsingApp
```
in terminal.
## Usage
To run simply type `SimpleIsingApp`

App is divided into three base sections. 
 - Upper left corner - spin lattice
 - Upper right corner - control panel
 - Lower segment - Energy and magnetisation plots
 
You can start/stop simulation by clicking `plot` button. 
To change temperature or outside magnetic field simply type 
new value in their respective fields and click `set new paramiters`. 
Temperature must be bigger then 0.

You can also change parameters of lattice namely its size 
and chose from few initial spin configuration. 
Those changes as well are apply by clicking `set new paramiters`.
Changing one (or both) of those resets not only lattice but also
properties plots.
Size, as one can guess, must be positive. 
Also, it shouldn't be too big, since simulation takes some time.
Values below 64 are completely save and don't affect performance.

---

## References

 - https://en.wikipedia.org/wiki/Ising_model
 - https://en.wikipedia.org/wiki/Metropolis-Hastings_algorithm
 - https://www.coursera.org/learn/statistical-mechanics