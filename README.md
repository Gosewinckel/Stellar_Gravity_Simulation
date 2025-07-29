I have made changes to this file post submission deadline as it only occured to me after sleeping that I did not at all explain what this project actually does. Anything that has been added after the submission time will be underneath an *edit note.
 
 # Galactic Centre Simulation

 This projects is a GPU accelerated n-body, Newtonian gravity simulation. It is build using Taichi in Python.


 
 
 edit*
 This program simulates the behaviour of stellar objects at the centre of a galaxy. At the centre of the simulation there is a supermassive black hole and the user can input how many stars they would like to simulate. The stars will all, be located randomly within a 1 parsec radial distance to the black hole. Stars start with random mass and velocity within a reasonable range of what would be found in a system like this.

 ![Demo](./Jul-29-2025 00-44-21.gif)

# Requirements

 - Python >=3.7, <=3.11 
 - taichi
 - numpy

 - install numpy and taichi with
```sh
  pip install -r requirements.txt
```
  you will have to have installed a version of python within the above range

 # Installation and Usage

 ### Clone the repo
```sh
git clone https://github.com/Gosewinckel/Stellar_Gravity_Simulation
cd Stellar_Gravity_Simulation
```

 ### Create a virtual environment in python 3.11
 set up a virtual environment in python 3.11
```sh
python3.11 -m venv taichi-env
```
 then activate it 
 mac/linux:
```sh
source taichi-env/bin/activate
```

 ### Run the simulation
```sh
python main.py
```

edit* 
the simulation itself is GPU optimised and can quite easily run 10000 stars however the startup is not resulting in longer startup times for larger numbers of stars.

 # Assumptions and Approximations
 I have made a lot of assumptions and approximations in the development of this simulation so that a desktop can handle the processing, I will list them here.
 - Newtonian universe
 - Frictionless universe
 - increments of time are 0.165 years at dt=1
 - Used Verlet integration to calculate differential equations
 - Stars immediately appear with random properties




edit*
# How it works
In config.py there is a set of initial conditions which determine the range stars can be generated in. The program initialises the number of stars that the user has chosen with mass, velocity and position within the bounds of the initial conditions, it also creates one supermassive black hole. The force is calculated by summing the force vector between a star and every other object in the sim, this is calculated using Newtons equation of gravity F=Gmm'/r^2 and the equations of motion. The equations of motion are solved using Verlet integration. Each force calculation is calculated concurrently on the GPU in order to make massive numbers of stars possible and run well.



edit*
# Limits and changes
There are obvious limits to runing a simulation like this on a personal computer but I will list the main ones here
- calculations get less accurate as objects get close to one another. Because integral steps are finite, if an object gets close to the black hole its force calculation will skyrocket and will not be balanced because by the next iteration it will already be sent far away from the acting body, this is why stars get flung out of the simulated galaxy. I have tried to balance this by adding an event horizon so that when stars get too close to the black hole they are effectively swallowed by it.
- Initial conditions are random. While stars start within a reasonable range there needs to be far more fine tuning done in order to make this a realistic physical system. Velocity and mass should be higher closer to the black hole and velocity should decay exponentially as the stars start further away. This is in order to create more stable orbits in the system instead of having som much chaos. I was working on the function orbit_initialise_masses() which was a GPU accelerated initialising function that creates these conditions but unfortunately I could not get it working by the deadline.
- I would like the simulation to display far more information such as time passed, velocity trains and force vectors in order to give a really clear demonstration of the physics involved but again I unfortunately did not have the time to implement these before the deadline.
