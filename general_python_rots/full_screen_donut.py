"""
Prototype mathematics in rubato
"""

import rubato as rb
import os.path
import sys, math
parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent)
from point_rotator import rotate_pt


thickness = 10  # a is the thickness of the donut
radius = 15  # c is the radius of the donut
angle_of_tube = 360  # How much of the tube is visible (in degrees)
angle_of_donut = 360  # How much of the donut is visible (in degrees)

rb.init(res=(500, 500), maximize=True, target_fps=60)
rb.Game.show_fps = True


roll_donut = 0  # spin around x-axis counter-clockwise (on screen its another up-down motion)
pitch_donut = 0  # spin around z-axis
yaw_donut = 0  # spin around y-axis counter-clockwise rotation (on screen it looks like ur just moving up)

deg_to_rad = math.pi / 180

shape_donut: list[tuple[float, float, float]] = []

# calculates the points on a donut with no rotation centered on the origin
for v in range(0, angle_of_tube, 3):  # goes around the tube interval of 3 if you want it to be w/out holes
    for u in range(0, angle_of_donut, 2):  # goes around the torus
        v_ = v * deg_to_rad
        u_ = u * deg_to_rad
        x = (radius + thickness * math.cos(v_)) * math.cos(u_)
        y = (radius + thickness * math.cos(v_)) * math.sin(u_)
        z = thickness * math.sin(v_)
        shape_donut.append((x, y, z))

dims_donut = (thickness + radius) * 2, (thickness + radius) * 2
surf_donut = rb.Surface(*dims_donut, (10, 10))


def custom_update():
    global roll_donut, pitch_donut, yaw_donut
    roll_donut += 0.0704
    pitch_donut += 0.0352
    # Updates the roll and yaw in radians


def custom_draw():
    z_buffer_donut = [-float("inf")] * (dims_donut[0] * dims_donut[1])
    surf_donut.fill(rb.Color.night)

    # rotates the points centered on the origin, then draws them
    for point in shape_donut:
        x, y, z = rotate_pt(*point, roll_donut, pitch_donut, yaw_donut)
        if z_buffer_donut[x + dims_donut[0] * y] < z:
            z_buffer_donut[x + dims_donut[0] * y] = z
            color = rb.Color.mix(
                rb.Color.yellow, rb.Color.red, rb.Math.map(z, -thickness - radius, thickness + radius, 0, 1), "linear"
            )
            surf_donut.set_pixel((x, y), color, False)

    rb.Draw.queue_surface(surf_donut)


rb.Game.update = custom_update
rb.Game.draw = custom_draw
rb.begin()
