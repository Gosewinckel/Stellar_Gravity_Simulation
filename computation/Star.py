import taichi as ti
import taichi.math as tm

Star = ti.types.struct(pos=tm.vec3, radius=ti.f32, m=ti.u64, v=tm.vec3, f=tm.vec3)
