from computation import Star, nbody
from computation.nbody import gravity_step, Stars, rand_initialise_masses
import taichi as ti
import config as conf


render_pos = ti.Vector.field(3, ti.f32, shape=conf.n)
render_v = ti.Vector.field(3, ti.f32, shape=conf.n)
render_f = ti.Vector.field(3, ti.f32, shape=conf.n)

@ti.kernel
def update_render_data():
    for i in range(conf.n):
        render_pos[i] = Stars[i].pos
        render_v[i] = Stars[i].v
        render_f[i] = Stars[i].f

