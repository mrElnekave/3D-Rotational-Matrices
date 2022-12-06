import rubato as rb
from point_rotator import rotate_pt
import math

# donut variables
thickness = 10  # a is the thickness of the donut
radius = 15  # c is the radius of the donut
angle_of_tube = 360  # How much of the tube is visible (in degrees)
angle_of_donut = 360  # How much of the donut is visible (in degrees)


roll = 0  # spin around x-axis counter-clockwise (on screen its another up-down motion)
pitch = 0  # spin around z-axis
yaw = 0  # spin around y-axis counter-clockwise rotation (on screen it looks like ur just moving up)


# generate donut
deg_to_rad = math.pi / 180
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

def donut_surf():
    z_buffer = [-float("inf")] * (dims[0] * dims[1])
    surf.fill(rb.Color.white)

    # rotates the points centered on the origin, then draws them
    for point in shape:
        x, y, z = rotate_pt(*point, roll, pitch, yaw)
        if z_buffer[x + dims[0] * y] < z:
            z_buffer[x + dims[0] * y] = z
            color = rb.Color.mix(
                rb.Color.yellow, rb.Color.red, rb.Math.map(z, -thickness - radius, thickness + radius, 0, 1), "linear"
            )
            surf.set_pixel((x, y), color, False)

    return surf