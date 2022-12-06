"""
Prototype mathematics in rubato
"""

import rubato as rb
import math
from point_rotator import rotate_pt

# cube variables
cube_half_width = 10
cube_half_height = 10
cube_half_depth = 10

# donut variables
thickness = 10  # a is the thickness of the donut
radius = 15  # c is the radius of the donut
angle_of_tube = 360  # How much of the tube is visible (in degrees)
angle_of_donut = 360  # How much of the donut is visible (in degrees)

rb.init(res=(500, 500), maximize=True, target_fps=60)
rb.Game.show_fps = True

roll = 0  # spin around x-axis counter-clockwise (on screen its another up-down motion)
pitch = 0  # spin around z-axis
yaw = 0  # spin around y-axis counter-clockwise rotation (on screen it looks like ur just moving up)

deg_to_rad = math.pi / 180

# generate donut
shape: list[tuple[float, float, float]] = []
dims = (thickness + radius) * 2, (thickness + radius) * 2

# calculates the points on a donut with no rotation centered on the origin
for v in range(0, angle_of_tube, 4):  # goes around the tube interval of 3 if you want it to be w/out holes
    for u in range(0, angle_of_donut, 2):  # goes around the torus
        v_ = v * deg_to_rad
        u_ = u * deg_to_rad
        x = (radius + thickness * math.cos(v_)) * math.cos(u_)
        y = (radius + thickness * math.cos(v_)) * math.sin(u_)
        z = thickness * math.sin(v_)
        shape.append((x, y, z))

surf = rb.Surface(*dims, (4, 4))
# end of donut generation

# cube generation
face_up: tuple[rb.Color, list] = (rb.Color.blue, [])
face_down: tuple[rb.Color, list] = (rb.Color.blue.darker(10), [])
face_left: tuple[rb.Color, list] = (rb.Color.red, [])
face_right: tuple[rb.Color, list] = (rb.Color.red.darker(10), [])
face_front: tuple[rb.Color, list] = (rb.Color.green, [])
face_back: tuple[rb.Color, list] = (rb.Color.green.darker(10), [])
dims_cube = int(cube_half_width * 2 * 2**(1/2)) + 2, int(cube_half_height * 2 * 2**(1/2)) + 2

step = 1
for x in range(-cube_half_width * 2, cube_half_width * 2, step):
    for y in range(-cube_half_height * 2, cube_half_height * 2, step):
        _x = x / 2
        _y = y / 2
        face_up[1].append((_x, _y, cube_half_depth))
        face_down[1].append((_x, _y, -cube_half_depth))
        face_left[1].append((_x, -cube_half_width, _y))
        face_right[1].append((_x, cube_half_width, _y))
        face_front[1].append((-cube_half_width, _x, _y))
        face_back[1].append((cube_half_width, _x, _y))
surf_cube = rb.Surface(*dims_cube, (6, 6))
# end of cube generation

def custom_update():
    global roll, pitch, yaw
    roll += 0.0704
    pitch += 0.0352
    yaw += 0.0176
    # Updates the roll and yaw in radians


def custom_draw():
    offset = 125
    z_buffer = [-float("inf")] * (dims[0] * dims[1])
    surf.fill(rb.Color.white)

    # rotates the points centered on the origin, then draws them
    for point in shape:
        x, y, z = rotate_pt(*point, roll, pitch, 0) # yaw is 0 because we don't want to rotate wiggle the donut
        if z_buffer[x + dims[0] * y] < z:
            z_buffer[x + dims[0] * y] = z
            color = rb.Color.mix(
                rb.Color.yellow, rb.Color.red, rb.Math.map(z, -thickness - radius, thickness + radius, 0, 1), "linear"
            )
            surf.set_pixel((x, y), color, False)

    rb.Draw.queue_surface(surf, (offset, offset))

    # rotates the cube and draws it
    surf_cube.fill(rb.Color.white)
    z_buffer = [-float("inf")] * (dims_cube[0] * dims_cube[1])
    for color, face in (face_up, face_down, face_left, face_right, face_front, face_back):
        for point in face:
            x, y, z = rotate_pt(*point, roll, pitch, yaw)
            if z_buffer[x + dims_cube[0] * y] < z:
                z_buffer[x + dims_cube[0] * y] = z
                surf_cube.set_pixel((x, y), color, False)
    
    rb.Draw.queue_surface(surf_cube, (-offset, -offset))


rb.Game.update = custom_update
rb.Game.draw = custom_draw
rb.begin()
