import rubato as rb
from math import cos, sin, pi
import os.path
import sys
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent)
from point_rotator import rotate_pt

rb.init(res=(300, 300), maximize=True)


# define cube vertices
width = 40
height = 40
depth = 50

center = rb.Vector(0, 0)

roll = 0 # spin around x-axis counter-clockwise (on screen its another up-down motion)
pitch = 0 # spin around z-axis
yaw = 0 # spin around y-axis counter-clockwise rotation (on screen it looks like ur just moving up)


scene = rb.Scene()

# define rotation functions

torus = []

def gen_torus():
    a = 50   # a is the radius of the tube
    c = 80   # c is the radius of the torus
    for v in range(0, 360, 10):  # goes around the tube
        for u in range(0, 360, 4):  # goes around the torus
            v_ = v * pi / 180
            u_ = u * pi / 180
            x = (c + a * cos(v_)) * cos(u_)
            y = (c + a * cos(v_)) * sin(u_)
            z = a * sin(v_)
            torus.append((x, y, z))
gen_torus()
def custom_draw():  
    for point in torus:
        x, y, z = rotate_pt(*point, roll, pitch, yaw)
        rb.Draw.queue_rect(rb.Vector(x, y), 6, 6, fill=rb.Color.blue, z_index=int(z), border=None)


scene.draw = custom_draw

text_go = rb.wrap(text:=rb.Text("Testing z rotation", anchor=(0, 1)), pos=(0, 100))


def custom_update():
    global roll, pitch, yaw
    if rb.Input.key_pressed("a"):
        text.text = "Testing z rotation"
        pitch += 0.01
    if rb.Input.key_pressed("d"):
        pitch -= 0.01
        text.text = "Testing z rotation"

    if rb.Input.key_pressed("w"):
        roll -= 0.01
        text.text = "Testing x rotation"
    if rb.Input.key_pressed("s"):
        roll += 0.01
        text.text = "Testing x rotation"
    if rb.Input.key_pressed("q"):
        yaw += 0.01
        text.text = "Testing y rotation"
    if rb.Input.key_pressed("e"):
        yaw -= 0.01
        text.text = "Testing y rotation"
    

scene.update = custom_update

scene.add_ui(text_go)


rb.begin()
