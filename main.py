import taichi as ti
ti.init(arch=ti.gpu)

import taichi.math as tm
from computation import Star, nbody
from computation.nbody import Stars, rand_initialise_masses, gravity_step
from rendering import GGUI
import config as conf
import time


def main():
    window = ti.ui.Window("test", (conf.x, conf.y))
    canvas = window.get_canvas()
    scene = ti.ui.Scene()
    camera = ti.ui.Camera()
    camera.position(5,2,2)
    rand_initialise_masses()

    TARGET_FPS = 30
    FRAME_DURATION = 1/TARGET_FPS

    while window.running:
        frame_start = time.time()
        GGUI.update_render_data()
        gravity_step()
        scene.set_camera(camera)
        scene.particles(GGUI.render_pos, color=(255,255,255), radius=0.0035)
        canvas.scene(scene)
        window.show()
        elapsed = time.time() - frame_start
        sleep_time = FRAME_DURATION - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)


if __name__ == "__main__":
    main()

