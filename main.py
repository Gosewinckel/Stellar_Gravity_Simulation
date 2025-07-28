import taichi as ti
ti.init(arch=ti.gpu)

import taichi.math as tm
from computation import Star, nbody
from computation.nbody import Stars, rand_initialise_masses, orbit_initialise_masses, gravity_step
from rendering import GGUI
import config as conf
import time


def main():

    #get user input
    check = True
    while check == True:
        num = input("Number of stars to simulate: ")
        try:
            num = int(num);
            check = False
        except:
            print("pick a valid integer")

    conf.n = num

    window = ti.ui.Window("test", (conf.x, conf.y))
    canvas = window.get_canvas()
    scene = ti.ui.Scene()
    camera = ti.ui.Camera()
    
    camera.position(1.5,1.5,-1.5)
    move_speed = 0.05
    cam_pos=ti.Vector([5,2,2])
    can_look=ti.Vector([0.0,0.0,0.0])

    rand_initialise_masses()

    TARGET_FPS = 60
    FRAME_DURATION = 1/TARGET_FPS
    time_passed = 0

    temp_pos = ti.Vector.field(3, dtype=ti.f32, shape=1)

    #run GUI
    while window.running:
        frame_start = time.time()
        camera.track_user_inputs(window, movement_speed=0.03, hold_key=ti.ui.LMB)
        GGUI.update_render_data()
        gravity_step()

        with window.GUI.sub_window("Controls", 0.85, 0.01, 0.1, 0.1):
            window.GUI.text("exit: q")
            window.GUI.text("movement: wasd")
            window.GUI.text("camera: left mouse button")

        if window.is_pressed("q"):
            window.running = False

        with window.GUI.sub_window(f"dt = {conf.dt}", 0.85, 0.12, 0.06, 0.06):
            if window.GUI.button("-"):
                conf.dt[None] -= 0.1
            if window.GUI.button("+"):
                conf.dt[None] += 0.1

        scene.set_camera(camera)

        temp_pos[0] = GGUI.render_pos[0]

        ##draw particles
        scene.particles(GGUI.render_pos, color=(10,10,10), radius=0.001)
        scene.particles(temp_pos, color=(5, 0, 10), radius=0.005)

        #GGUI.draw_Force_Vectors(scene)
        canvas.scene(scene)
        window.show()

        #ensure not running at higher frames
        elapsed = time.time() - frame_start
        sleep_time = FRAME_DURATION - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)


if __name__ == "__main__":
    main()

