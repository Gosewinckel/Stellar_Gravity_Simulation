import taichi as ti
import taichi.math as tm
import config as conf
from computation import Star
import numpy as np

n = conf.n

Stars = Star.Star.field(shape = n)
F_p = ti.Vector.field(3, dtype=float, shape=n)
F_n = ti.Vector.field(3, dtype=float, shape=n)
Forces = ti.Vector.field(3, dtype=float, shape=(n, n))


def rand_initialise_masses():
    gen = np.random.default_rng()
    for i in range(n):
        if i == 0:
            mass = gen.integers(low=1*10**7, high=1*10**11, size=1)
            Stars[i].m = mass[0]
            Stars[i].pos = [conf.width/2, conf.height/2, conf.depth/2]
            Stars[i].v = [0, 0, 0]
            continue
        mass = gen.integers(low=conf.M_min, high=conf.M_max, size=1)
        Stars[i].m = mass[0]
        point = gen.integers(low=0, high=conf.height, size=3)
        Stars[i].pos = point
        v_mag = gen.integers(low=conf.V_min, high=conf.V_max, size=1)
        v = gen.integers(low=-1000000, high=1000001, size=3)
        u = v/tm.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        Stars[i].v = v_mag*u

#calculate change in conditions
@ti.kernel
def gravity_step():

    #update positions with forces from prev step
    for i in range(n):
        Stars[i].pos += Stars[i].v + (Stars[i].f/Stars[i].m)*((conf.dt**2)*0.5)
        
    for i in Stars:
        force = ti.Vector([0.0,0.0,0.0])
        for j in range(conf.n):
            if i == j:
                continue

            #calculate new vector
            vector_ij = Stars[j].pos - Stars[i].pos
            v_mag = tm.sqrt(vector_ij[0]**2 + vector_ij[1]**2 + vector_ij[2]**2)
            unit_ij = vector_ij/v_mag

            #calculate new force
            force += F_grav(Stars[i].m, Stars[j].m, v_mag, unit_ij)

        #calculate new velocity
        Stars[i].f = force
        Stars[i].v += (Stars[i].f + F_p[i])/Stars[i].m * (conf.dt*0.5)
        F_p[i] = Stars[i].f
        



@ti.func
def F_grav(m1, m2, r, u):
    return conf.G*((m1*m2)/r**2) * u


