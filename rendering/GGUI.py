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
        render_pos[i] = (Stars[i].pos/conf.height)*1
        render_v[i] = Stars[i].v
        render_f[i] = Stars[i].pos/conf.height + Stars[i].f/conf.height

def draw_Force_Vectors(scene):
    force = ti.Vector.field(3, ti.f32, shape=(2))
    for i in range(1, conf.n):
        force[0] = render_pos[i]
        force[1] = render_f[i]
        scene.lines(force, width=1, color=(1,0,0))

