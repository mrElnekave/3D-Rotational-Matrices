"""
Prototype mathematics in rubato
"""

import rubato as rb
import math
import random
from point_rotator import rotate_pt

thickness = 10  # a is the thickness of the donut
radius = 15  # c is the radius of the donut
angle_of_tube = 360  # How much of the tube is visible (in degrees)
angle_of_donut = 360  # How much of the donut is visible (in degrees)


roll_donut = 0  # spin around x-axis counter-clockwise (on screen its another up-down motion)
pitch_donut = 0  # spin around z-axis
yaw_donut = 0  # spin around y-axis counter-clockwise rotation (on screen it looks like ur just moving up)

deg_to_rad = math.pi / 180

coloring = {
    "bottom": rb.Color.from_hex("#dd8331"), 
    "glaze": rb.Color.from_hex("#fa8596"), 
    "random_burnt": rb.Color.from_hex("#63200d")
}

sprinkles = [
    rb.Color.from_hex("#ffb35c"),
    rb.Color.from_hex("#ffb0c1"),
    rb.Color.from_hex("#00c2d9"),
    rb.Color.from_hex("#f14545"),
    rb.Color.from_hex("#823dd1"),
]

shape_donut: list[tuple[tuple[float, float, float], rb.Color]] = []

# calculates the points on a donut with no rotation centered on the origin
for v in range(0, angle_of_tube, 3):  # goes around the tube interval of 3 if you want it to be w/out holes
    color = None
    if 70 <= v <= 110:
        color = rb.Color.mix(coloring["random_burnt"], coloring["bottom"], math.fabs(90 - v) / 20, "linear")
    elif 0 <= v <= 180:
        color = coloring["bottom"]
    else:
        color = coloring["glaze"]

    for u in range(0, angle_of_donut, 2):  # goes around the torus
        # if color == coloring["bottom"] and random.randint(0, 100) < 5:
        #     _color = coloring["random_burnt"]
        if color == coloring["glaze"] and random.randint(0, 100) < 5:
            _color = random.choice(sprinkles)
        else:
            _color = color
        v_ = v * deg_to_rad
        u_ = u * deg_to_rad
        x = (radius + thickness * math.cos(v_)) * math.cos(u_)
        y = (radius + thickness * math.cos(v_)) * math.sin(u_)
        z = thickness * math.sin(v_)
        shape_donut.append(((x, y, z), _color))

dims_donut = (thickness + radius) * 2, (thickness + radius) * 2
surf_donut = rb.Surface(*dims_donut, (4, 4))



def sprinkles_surf():
    z_buffer_donut = [-float("inf")] * (dims_donut[0] * dims_donut[1])
    surf_donut.fill(rb.Color.white)

    # rotates the points centered on the origin, then draws them
    for point, color in shape_donut:
        x, y, z = rotate_pt(*point, roll_donut, pitch_donut, yaw_donut)
        if z_buffer_donut[x + dims_donut[0] * y] < z:
            z_buffer_donut[x + dims_donut[0] * y] = z
            surf_donut.set_pixel((x, y), color, False)

    return surf_donut

