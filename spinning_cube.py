import rubato as rb
from big_demo.point_rotator import rotate_pt
rb.init(res=(300, 300), maximize=True)


# define cube vertices
width = 40
height = 40
depth = 40

center = rb.Vector(0, 0)

roll = 0 # spin around x-axis counter-clockwise (on screen its another up-down motion)
pitch = 0 # spin around z-axis
yaw = 0 # spin around y-axis counter-clockwise rotation (on screen it looks like ur just moving up)


scene = rb.Scene()

# define rotation functions

def custom_draw():  
    for _x in range(-width, width, 10):
        for _y in range(-height, height, 10):
            amt = 20
            perms = ((_x, _y, depth, rb.Color.blue.lighter(amt)), 
            (_x, _y, -depth, rb.Color.blue.darker(amt)), 
            (_x, depth, _y, rb.Color.red.lighter(amt)), 
            (_x, -depth, _y, rb.Color.red.darker(amt)), 
            (depth, _x, _y, rb.Color.green.lighter(amt)), 
            (-depth, _x, _y, rb.Color.green.darker(amt)))
            for perm in perms:
                orientation, color = perm[:-1], perm[-1]
                x, y, z = rotate_pt(*orientation, roll, pitch, yaw)
                rb.Draw.queue_rect(rb.Vector(x, y), 3, 3, fill=color, z_index=int(z), border=None)


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
