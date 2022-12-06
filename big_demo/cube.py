import rubato as rb
from point_rotator import rotate_pt


# cube variables
cube_half_width = 10
cube_half_height = 10
cube_half_depth = 10


roll = 0  # spin around x-axis counter-clockwise (on screen its another up-down motion)
pitch = 0  # spin around z-axis
yaw = 0  # spin around y-axis counter-clockwise rotation (on screen it looks like ur just moving up)


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

def cube_surf():
    # rotates the cube and draws it
    surf_cube.fill(rb.Color.white)
    z_buffer = [-float("inf")] * (dims_cube[0] * dims_cube[1])
    for color, face in (face_up, face_down, face_left, face_right, face_front, face_back):
        for point in face:
            x, y, z = rotate_pt(*point, roll, pitch, yaw)
            if z_buffer[x + dims_cube[0] * y] < z:
                z_buffer[x + dims_cube[0] * y] = z
                surf_cube.set_pixel((x, y), color, False)
    
    return surf_cube