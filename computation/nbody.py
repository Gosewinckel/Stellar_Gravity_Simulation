import taichi as ti
import taichi.math as tm
import config as conf
from computation import Star
import numpy as np


conf.n

Stars = Star.Star.field(shape=conf.n)    #holds all star structs
F_p = ti.Vector.field(3, dtype = float, shape=conf.n)      #holds previous force vectors
#F_n = ti.Vector.field()
B_max = ti.u64
B_max = 1*10**11
B_min = ti.u64
B_min = 1*10**7

#create fields for stars and force vectors
def create_fields():
    Stars = Star.Star.field(shape=conf.n)
    F_p = ti.Vector.field(3, dtype=float, shape=conf.n)
    return Stars, F_p

#Initialise stars with random values
def rand_initialise_masses():
    gen = np.random.default_rng()
    for i in range(conf.n):
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

#Initialise stars with orbital trajectories
@ti.kernel
def orbit_initialise_masses():
    #generate black hole
    m = ti.random(dtype=float)
    Stars[0].m = ti.u64(9*10**10) * m + ti.u64(1*10**7)
    Stars[0].pos = [conf.width/2, conf.height/2, conf.depth/2]
    Stars[0].v = [0.0, 0.0, 0.0]


    r_s = (2 * conf.G * Stars[0].m)/conf.C**2 
    #generate stars
    for i in range(1, conf.n):
        #initialise positions
        pos_x = (ti.random(dtype=float))
        pos_y = (ti.random(dtype=float))
        pos_z = (ti.random(dtype=float))

        u = tm.sqrt(pos_x**2 + pos_y**2 + pos_z**2)
        pos_x /= u
        pos_y /= u
        pos_z /= u

        mag = ti.random(dtype=float) * ti.random(dtype=float) * conf.width/2 + r_s*30
        pos_x *= mag
        pos_y *= mag
        pos_z *= mag

        if ti.random(dtype=ti.i32) < 0:
            pos_x *= -1
        if ti.random(dtype=ti.i32) < 0:
            pos_y *= -1
        if ti.random(dtype=ti.i32) < 0:
            pos_z *= -1

        #final position
        Stars[i].pos = [pos_x + conf.width/2, pos_y + conf.height/2, pos_z + conf.depth/2]

        #initialise masses
        Stars[i].m = conf.M_max * ti.random(dtype=float) + conf.M_min

        #initialise trajectory
        #generate a random orthoganoal vector by finding the determinant of the force vector and a random vector
        F_v = Stars[0].pos - Stars[i].pos
        r_v = [ti.random(dtype=float), ti.random(dtype=float), ti.random(dtype=float)]
        #find determinant
        R_v = [(F_v[1]*r_v[2]) - (F_v[2]*r_v[1]), (F_v[0]*r_v[2]) - (F_v[2]*r_v[0]), (F_v[0]*r_v[1]) - (F_v[1]*r_v[0])]
        #normalise for unit vector
        R_norm = tm.sqrt(R_v[0]**2 + R_v[1]**2 + R_v[2]**2)
        R_v[0] /= R_norm
        R_v[1] /= R_norm
        R_v[2] /= R_norm

        #make trajectory more random the closer to the black hole the star is
        rand_scalar = 1/tm.sqrt(F_v[0]**2 + F_v[1]**2 + F_v[2]**2)
        rand_vector = [1.0, 1.0, 1.0]
        rand_vector[0] *= rand_scalar
        rand_vector[1] *= rand_scalar
        rand_vector[2] *= rand_scalar
        if ti.random(dtype=ti.i32) < 0:
            rand_vector[0] *= -1
        if ti.random(dtype=ti.i32) < 0:
            rand_vector[1] *= -1
        if ti.random(dtype=ti.i32) < 0:
            rand_vector[2] *= -1
        R_v[0] += rand_vector[0]
        R_v[1] += rand_vector[1]
        R_v[2] += rand_vector[2]

        Stars[i].v = R_v

        #set velocity to a stable orbit
        R_mag = ti.sqrt(F_v[0]**2 + F_v[1]**2 + F_v[2]**2)
        V_o = ti.sqrt((conf.G*Stars[0].m)/R_mag)
        Stars[i].v *= V_o



#calculate change in conditions
@ti.kernel
def gravity_step():
    r_s = (2 * conf.G * Stars[0].m)/conf.C**2 
    #update positions with forces from prev step
    for i in range(conf.n):
        if Stars[i].m == 0:
            continue
        Stars[i].pos += Stars[i].v*conf.dt[None] + (Stars[i].f/Stars[i].m)*((conf.dt[None]**2)*0.5)
        if i == 0:
            continue

        #stars get destroyed by tidal forces within 20x event horizon
        r = tm.sqrt((Stars[i].pos[0] - Stars[0].pos[0])**2 + (Stars[i].pos[1] - Stars[0].pos[1])**2 + (Stars[i].pos[2] - Stars[0].pos[2])**2)
        if r <= r_s * 20:
            Stars[0].m += Stars[i].m
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
        


#calculate force vector between two objects
@ti.func
def F_grav(m1, m2, r, u):
    return conf.G*((m1*m2)/r**2) * u


