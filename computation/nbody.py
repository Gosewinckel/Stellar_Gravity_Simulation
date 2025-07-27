import taichi as ti
import taichi.math as tm
import config as conf
from computation import Star

n = conf.n

Stars = Star.Star.field(shape = n)
Forces = ti.Vector.field(3, dtype=float, shape=(n, n))

@ti.kernel
def rand_initialise_masses():
    for i in ti.grouped(Stars):
       s = Star.Star()
       #make random based on normal distribution of stars
       s.m = 1000000000 
       s.pos = [ti.random()* conf.width, ti.random() * conf.height, ti.random() * conf.depth]
       s.v = [1, 1, 1]
       s.f = [0, 0, 0]
       Stars[i] = s

@ti.kernel
def gravity_step():
    for i, j in Forces:
        if i == j:
            continue
        Forces[i, j] = [0, 0, 0]
        vector_ij = Stars[j].pos - Stars[i].pos
        v_mag = tm.sqrt(vector_ij[0]**2 + vector_ij[1]**2 + vector_ij[2]**2)
        unit_ij = vector_ij/v_mag
        f_g = F_grav(Stars[i].m, Stars[j].m, v_mag, unit_ij)
        Forces[i, j] = f_g
        Stars[i].f = f_g
    
    #will be replaced by proper integration function
    for i in ti.grouped(Stars):
        Stars[i].v += (Stars[i].f/Stars[i].m)*conf.dt
        Stars[i].pos += Stars[i].v*conf.dt

@ti.func
def F_grav(m1, m2, r, u):
    return conf.G*((m1*m2)/r**2) * u
