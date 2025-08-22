import taichi as ti

#conversions
Au = 1.5e11             #1 astronomical unit
Mo = 1e30               #half 1 solar mass
Ty = 5256000            #takes fastest known black hole orbiting star 10 years to orbit, this is 10 years /60 so that it equals 1 orbit every second when dt=1
Gi = 6.67e-11            #Newtons gravitational constant

G = (Gi*Mo*Ty**2)/Au**3
C = (3e8 * Ty)/Au

n = 1000000                 #number of solar objects - 1 (the first object is a black hole)

dt = ti.field(dtype=ti.f32, shape=())
dt[None] = 1            #incriments  of time for Verlet integration

width = 206265*2        #makes a box that surounds a sphere with radius=1parsec
height = 206265*2
depth = 206265*2

#window size
x = 2200
y = 1300

#range for mass in Mo
M_min = 1
M_max = 300

#range for velocity_total in Au/Ty 
V_min = 7
V_max = 700
