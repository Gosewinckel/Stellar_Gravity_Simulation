import taichi as ti
ti.init(arch=ti.cpu)

import taichi.math as tm
from computation import Star, nbody
from computation.nbody import Stars, rand_initialise_masses, gravity_step
from rendering import GGUI


def main():
    window = ti.ui.Window("test", (100, 100))
    canvas = window.get_canvas()
    scene = ti.ui.Scene()
    camera = ti.ui.Camera()
    camera.position(5,2,2)

    while window.running:
       GGUI.update_render_data()
       scene.set_camera(camera)
       scene.particles(GGUI.render_pos, color=(0,0,0), radius=0.1)
       canvas.scene(scene)
       window.show()


if __name__ == "__main__":
    main()

