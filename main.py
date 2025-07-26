import taichi as ti
import taichi.math as tm
from computation import Star, nbody
from computation.nbody import Stars, rand_initialise_masses, gravity_step

def main():

    rand_initialise_masses()    
    for i in range(5):
        gravity_step()


if __name__ == "__main__":
    main()

