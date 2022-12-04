import rubato as rb
from rubato import Vector
from rubato import Color
from rotation_kachow import get_xyz
from math import cos, sin, pi


# target 54 * 54
a = 10 # a is the radius of the tube
c = 15 # c is the radius of the torus

rb.init(res=[(a+c)*2*10]*2, maximize=True)



class SurfaceZ(rb.Surface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset_zbuffer()
    
    def reset_zbuffer(self):
        self.zbuffer = [[-rb.Math.INF for _ in range(self.width)] for _ in range(self.height)]

    def set_pixel(self, pos: Vector | tuple[float, float], color: Color = Color.black, blending: bool = True, z: float = 0):

        if self.zbuffer[int(pos[1])][int(pos[0])] < z:
            self.zbuffer[int(pos[1])][int(pos[0])] = z
            super().set_pixel(pos, color, blending)
    

roll = pi/5 # spin around x-axis counter-clockwise (on screen its another up-down motion)
pitch = 0 # spin around z-axis
yaw = 0 # spin around y-axis counter-clockwise rotation (on screen it looks like ur just moving up)


# define rotation functions

quarter_torus = []

def gen_torus():
    for v in range(0, 360, 4):  # goes around the tube interval of 3 if you want it to be w/out holes
        for u in range(0, 180, 2):  # goes around the torus
            v_ = v * pi / 180
            u_ = u * pi / 180
            x = (c + a * cos(v_)) * cos(u_)
            y = (c + a * cos(v_)) * sin(u_)
            z = a * sin(v_)
            quarter_torus.append((x, y, z))
gen_torus()

surf = SurfaceZ((a + c) * 2, (a + c) * 2, (10, 10))

def custom_draw():  
    global roll, pitch, yaw
    roll += 0.0704
    pitch += 0.0352
    surf.reset_zbuffer()
    surf.fill(rb.Color.night)

    for point in quarter_torus:
        x, y, z = get_xyz(*point, roll, pitch, yaw)
        _x, _y, _z = int(x), int(y), int(z)
        color = rb.Color.mix(rb.Color.yellow, rb.Color.red, rb.Math.map(_z, -a-c, a+c, 0, 1), "linear")
        surf.set_pixel((_x, _y), color, z=_z, blending=False)

        _x, _y, _z = -int(x), -int(y), -int(z)
        color = rb.Color.mix(rb.Color.yellow, rb.Color.red, rb.Math.map(_z, -a-c, a+c, 0, 1), "linear")
        surf.set_pixel((_x, _y), color, z=_z, blending=False)

            
    rb.Draw.surface(surf)


# def custom_update():
#     global roll, pitch, yaw
#     if rb.Input.key_pressed("a"):
#         pitch += 0.01
#     if rb.Input.key_pressed("d"):
#         pitch -= 0.01

#     if rb.Input.key_pressed("w"):
#         roll -= 0.01
#     if rb.Input.key_pressed("s"):
#         roll += 0.01
#     if rb.Input.key_pressed("q"):
#         yaw += 0.01
#     if rb.Input.key_pressed("e"):
#         yaw -= 0.01
    

rb.Game.draw = custom_draw

rb.begin()
