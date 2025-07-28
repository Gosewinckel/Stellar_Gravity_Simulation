import taichi as ti
import taichi.math as tm
import config as conf
from computation import Star
import numpy as np

n = conf.n

Stars = Star.Star.field(shape = n)
F_p = ti.Vector.field(3, dtype=float, shape=n)
F_n = ti.Vector.field(3, dtype=float, shape=n)
B_max = ti.u64
B_max = 1*10**11
B_min = ti.u64
B_min = 1*10**7


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

@ti.kernel
def orbit_initialise_masses():
    for i in Stars:

        #generate black hole
        if i == 0:
            m = ti.random(dtype=float)
            Stars[i].m = ti.u64(9*10**10) * m + ti.u64(1*10**7)
            Stars[i].pos = [conf.width/2, conf.height/2, conf.depth/2]
            Stars[i].v = [0,0,0]
            continue
        
        #generate vector
        x = (206265 - 2000) * ti.random(dtype=float) + 2000 + conf.width/2
        y = (206265 - 2000) * ti.random(dtype=float) + 2000 + conf.height/2
        z = (206265 - 2000) * ti.random(dtype=float) + 2000 + conf.depth/2
        Stars[i].pos = [x,y,z]
        for j in range(3):
            rand = ti.random(ti.i32)
            if rand % 2 == 0:
                continue
            else:
                Stars[i].pos[j] -= conf.width/2

        #find appropriate velocity for closeness to black hole
        dist = ti.sqrt((Stars[i].pos[0] - Stars[0].pos[0])**2 + (Stars[i].pos[1] - Stars[0].pos[1])**2 + (Stars[i].pos[2] - Stars[0].pos[2])**2)
        v_total = 35.04*2.71**(dist - 2000/0.0127778)
        v_vec1 = ti.random(dtype=float)
        v_vec2 = ti.random(dtype=float)
        v_vec3 = ti.random(dtype=float)
      
        v_norm = ti.sqrt(v_vec1**2 + v_vec2**2 + v_vec3**2)

        v_vec1 /= v_norm
        v_vec2 /= v_norm
        v_vec3 /= v_norm
        Stars[i].v = [v_vec1, v_vec2, v_vec3] * v_total
        Stars[i].m = 1



#calculate change in conditions
@ti.kernel
def gravity_step():
    r_s = (2 * conf.G * Stars[0].m)/conf.C**2 
    #update positions with forces from prev step
    for i in range(n):
        if Stars[i].m == 0:
            continue
        Stars[i].pos += Stars[i].v*conf.dt[None] + (Stars[i].f/Stars[i].m)*((conf.dt[None]**2)*0.5)
        if i == 0:
            continue
        r = tm.sqrt((Stars[i].pos[0] - Stars[0].pos[0])**2 + (Stars[i].pos[1] - Stars[0].pos[1])**2 + (Stars[i].pos[2] - Stars[0].pos[2])**2)
        if r <= r_s:
            Stars[i].m = 0;
            Stars[i].pos = Stars[0].pos
            Stars[i].v = [0,0,0]
        
    for i in Stars:
        if Stars[i].m == 0:
            continue
        force = ti.Vector([0.0,0.0,0.0])
        for j in range(conf.n):
            if Stars[j].m == 0:
                continue
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
        Stars[i].v += ((Stars[i].f + F_p[i])/Stars[i].m) * (conf.dt[None]*0.5)
        F_p[i] = Stars[i].f
        



@ti.func
def F_grav(m1, m2, r, u):
    return conf.G*((m1*m2)/r**2) * u


