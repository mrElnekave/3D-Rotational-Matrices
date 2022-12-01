import rubato as rb
from math import cos, sin, pi

rb.init(res=(300, 300), maximize=True)


# define cube vertices
width = 50
height = 50
depth = 50

center = rb.Vector(0, 0)

point = (0, 30, 0)
roll = 0 # spin around x-axis counter-clockwise (on screen its another up-down motion)
pitch = 0 # spin around z-axis
yaw = 0 # spin around y-axis counter-clockwise rotation (on screen it looks like ur just moving up)


scene = rb.Scene()

# define rotation functions

def get_x(x, y, z, roll, pitch, yaw):
    return cos(pitch) * cos(yaw) * x  +  (-sin(pitch) * cos(roll) + cos(pitch) * sin(yaw) * sin(roll)) * y  +  (-sin(pitch) * -sin(roll) + cos(pitch) * sin(yaw) * cos(roll)) * z

def get_y(x, y, z, roll, pitch, yaw):
    return sin(pitch) * cos(yaw) * x  +  (cos(pitch) * cos(roll) + sin(pitch) * sin(yaw) * sin(roll)) * y  +  (cos(pitch) * -sin(roll) + sin(pitch) * sin(yaw) * cos(roll)) * z

def get_z(x, y, z, roll, pitch, yaw):
    return -sin(yaw) * x  +  (cos(yaw) * sin(roll)) * y  +  (cos(yaw) * cos(roll)) * z

def get_xyz(x, y, z, roll, pitch, yaw):
    return get_x(x, y, z, roll, pitch, yaw), get_y(x, y, z, roll, pitch, yaw), get_z(x, y, z, roll, pitch, yaw)

# gimbal circles
circle_z_plane: list[tuple] = []
def circle(xc, yc, radius, cicle_list):
        x = radius
        y = 0
        err = -x
        while x >= y:
            cicle_list.append((xc + x, yc + y, 0))
            cicle_list.append((xc + y, yc + x, 0))
            cicle_list.append((xc - y, yc + x, 0))
            cicle_list.append((xc - x, yc + y, 0))
            cicle_list.append((xc - x, yc - y, 0))
            cicle_list.append((xc - y, yc - x, 0))
            cicle_list.append((xc + y, yc - x, 0))
            cicle_list.append((xc + x, yc - y, 0))
            y += 1
            err += 2 * y + 1
            if err >= 0:
                x -= 1
                err -= 2 * x + 1
circle_z_plane = []

circle(0, 0, 30, circle_z_plane)

points = [(0, 30, 0), (0, -30, 0), (30, 0, 0), (-30, 0, 0), (0, 0, 30), (0, 0, -30)]
def draw_circle_z():
    first = True
    for c_point in circle_z_plane:
        x, y, z = get_xyz(*c_point, roll, pitch, yaw)
        pos = rb.Vector(x, y)
        if first:
            rb.Draw.queue_circle(pos, 2, rb.Color.red, fill=rb.Color.black.lighter(int(rb.Math.map(z, -30, 30, 10, 250))))
            first = False
        rb.Draw.queue_pixel(pos, color=rb.Color.red, z_index=int(z))

def custom_draw():  
    draw_circle_z()
    for point in points:
        rb.Draw.queue_circle(center, radius=2, border=None, fill=rb.Color(0, 0, 255), z_index=0)
        x = get_x(*point, roll, pitch, yaw)
        y = get_y(*point, roll, pitch, yaw)
        z = get_z(*point, roll, pitch, yaw)
        color = rb.Color.black.lighter(int(rb.Math.map(z, -30, 30, 10, 250)))
        rb.Draw.queue_circle((x, y), fill=color, z_index=int(z))


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
pitch = pi
# print("Get x: ", get_x(-1, 2, 3, 0, 0, pi / 2))
# print("Get y: ", get_y(-1, 2, 3, 0, 0, pi / 2))
# print("Get z: ", get_z(-1, 2, 3, 0, 0, pi / 2))

print(f"x: {get_x(*point, roll, pitch, yaw)}, y: {get_y(*point, roll, pitch, yaw)}, z: {get_z(*point, roll, pitch, yaw)}")

# python venv commmand
# python exists at: C:\Users\klavl\.pyenv\pyenv-win\versions\3.11.0\python.exe
# venv exists at: C:\Users\klavl\Documents\GitHub\Math-2B\venv