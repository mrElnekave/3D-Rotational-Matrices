import rubato as rb
from rotation_kachow import get_xyz
from math import cos, sin, pi
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
    a = 10
    c = 15
    for v in range(0, 360, 10):
        for u in range(0, 360, 2):
            x = (c + a * cos(v)) * cos(u)
            y = (c + a * cos(v)) * sin(u)
            z = a * sin(v)
            torus.append((x, y, z))
gen_torus()
def custom_draw():  
    for point in torus:
        x, y, z = get_xyz(*point, roll, pitch, yaw)
        rb.Draw.queue_rect(rb.Vector(x, y) * 4, 6, 6, fill=rb.Color.blue, z_index=int(z * 4), border=None)


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
