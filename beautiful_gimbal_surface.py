import rubato as rb
from rotation_kachow import get_xyz
from copy import copy

rb.init(res=(100, 100), window_size=(600, 600), name="Beautiful Gimbal Surface")


roll = 0 # spin around x-axis counter-clockwise (on screen its another up-down motion)
pitch = 0 # spin around z-axis
yaw = 0 # spin around y-axis counter-clockwise rotation (on screen it looks like ur just moving up)


scene = rb.Scene()

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
circle_x_plane = []
circle_y_plane = []

circle(0, 0, 40, circle_z_plane)
for point in circle_z_plane:
    x, y, _ = copy(point)
    circle_x_plane.append((0, x, y))
    x, y, _ = copy(point)
    circle_y_plane.append((x, 0, y))

points = [(0, 30, 0), (0, -30, 0), (30, 0, 0), (-30, 0, 0), (0, 0, 30), (0, 0, -30)]
def draw_circle_z():
    for c_point in circle_z_plane:
        x, y, z = get_xyz(*c_point, 0, pitch, 0)
        pos = rb.Vector(x, y)
        rb.Draw.queue_pixel(pos, color=rb.Color.blue, z_index=int(z))
def draw_circle_y():
    for c_point in circle_y_plane:
        x, y, z = get_xyz(*c_point, 0, pitch, yaw)
        pos = rb.Vector(x, y)
        rb.Draw.queue_pixel(pos, color=rb.Color.green, z_index=int(z))
def draw_circle_x():
    for c_point in circle_y_plane:
        x, y, z = get_xyz(*c_point, roll, pitch, yaw)
        pos = rb.Vector(x, y)
        rb.Draw.queue_pixel(pos, color=rb.Color.red, z_index=int(z))


font = rb.Font(size=6)

def custom_draw():  
    global roll, pitch, yaw

    rb.Draw.text(f"R: {roll:.2f}, P: {pitch:.2f}, Y: {yaw:.2f}", font=font, pos=rb.Vector(0, 45))

    draw_circle_z()
    draw_circle_y()
    draw_circle_x()
    for point in points:
        rb.Draw.queue_circle((0, 0), radius=2, border=None, fill=rb.Color(0, 0, 255), z_index=0)
        x, y, z = get_xyz(*point, roll, pitch, yaw)
        color = rb.Color.black.lighter(int(rb.Math.map(z, -30, 30, 10, 250)))
        rb.Draw.queue_circle((x, y), fill=color, z_index=int(z))


scene.draw = custom_draw
rb.Game.show_fps = True

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


# rb.begin()

# float x, y, z, _x;
#     y = 0;
#     z = 0;
#     for (x = -width; x < width; x+=.5) {
#         for (y = -width; y < width; y+=.5) {
#             _x = cos(psi) * cos(theta) * cos(phi) + -sin(psi) * sin(phi) * x  +  (cos(psi) * cos(theta) * -sin(phi) + -sin(psi) * cos(phi)) * y  +  (cos(psi) * sin(theta)) * z;
#             printf("x: %f, becomes %f\n", x, _x);
#         }
#     }

for x in range(-10, 10):
    for y in range(-10, 10):

        print(f"x {x} becomes {get_xyz(x, y, 10, roll, pitch, yaw)[0]}")

from math import cos, sin
psi, theta, phi = 0, 0, 0
x, y, z = 2, 2, 3
print(cos(psi) * cos(theta) * cos(phi) + -sin(psi) * sin(phi) * x  +  (cos(psi) * cos(theta) * -sin(phi) + -sin(psi) * cos(phi)) * y  +  (cos(psi) * sin(theta)) * z)


x = (cos(theta) * x + sin(theta) * sin(psi) * y + sin(theta) * cos(psi) * z)
y = ((sin(theta) * sin(phi) *x + (cos(psi) * cos(phi) - cos(theta) * sin(psi) * sin(phi)) * y + (cos(psi) * sin(phi) + cos(theta) * cos(phi) * sin(psi)) * z))
z = (-sin(theta) * cos(phi) * x + (cos(psi) * sin(phi) + cos(theta) * cos(phi) * sin(psi)) * y + (-sin(psi) * sin(phi) + cos(theta) * cos(psi) * cos(phi)) * z)