import rubato as rb
from math import cos, sin, pi

rb.init(res=(300, 300), maximize=True)


scene = rb.Scene()

# define rotation functions

def get_x(x, y, z, psi, theta, phi):
    return cos(theta) * x + \
            sin(theta) * sin(psi) * y + \
                sin(theta) * cos(psi) * z

def get_y(x, y, z, psi, theta, phi):
    return sin(theta) * sin(phi) * x + \
            (cos(psi) * cos(phi) - cos(theta) * sin(psi) * sin(phi)) * y + \
                (-cos(phi) * sin(psi) - cos(theta) * cos(psi) * sin(phi)) * z

def get_z(x, y, z, psi, theta, phi):
    return -sin(theta) * cos(phi) * x + \
            (cos(psi) * sin(phi) + cos(theta) * cos(psi) * cos(phi)) * y + \
                (-sin(psi) * sin(phi) + cos(theta) * cos(psi) * cos(phi)) * z


def calculate_X(x, y, z, roll, pitch, yaw):
  return y * sin(roll) * sin(pitch) * cos(yaw) - z * cos(roll) * sin(pitch) * cos(yaw) + \
         y * cos(roll) * sin(yaw) + z * sin(roll) * sin(yaw) + x * cos(pitch) * cos(yaw)


def calculate_Y(x, y, z, roll, pitch, yaw):
  return y * cos(roll) * cos(yaw) + z * sin(roll) * cos(yaw) - \
         y * sin(roll) * sin(pitch) * sin(yaw) + z * cos(roll) * sin(pitch) * sin(yaw) - \
         x * cos(pitch) * sin(yaw)


def calculate_Z(x, y, z, roll, pitch, yaw):
  return z * cos(roll) * cos(pitch) - y * sin(roll) * cos(pitch) + x * sin(pitch)

# define cube vertices
width = 50
height = 50
depth = 50

psi, theta, phi = 0, 0, 0

center = rb.Vector(0, 0)

def custom_draw():
    global psi, theta, phi
    psi += 0.01
    theta += 0.01
    phi += 0.01
    
    for x in range(-width, width):
        for y in range(-height, height):
            # I have to calculate for front of cube

            # since y-axis is up, x-axis is right, and z-axis is out of screen
            x = calculate_X(x, y, depth, psi, theta, phi)
            y = calculate_Y(x, y, depth, psi, theta, phi)
            z = calculate_Z(x, y, depth, psi, theta, phi)
            rb.Draw.queue_pixel(rb.Vector(x, y), rb.Color(255, 0, 0), z_index=int(z))

            # and back of cube
            # y-axis is up, x-axis is right, and z-axis is out of screen
            # x = get_x(x, y, depth, psi, theta, phi)
            # y = get_y(x, y, depth, psi, theta, phi)
            # z = get_z(x, y, depth, psi, theta, phi)
            # rb.Draw.queue_pixel(rb.Vector(x, y), rb.Color(255, 0, 0), z_index=int(z))


scene.draw = custom_draw

rb.begin()

# python venv commmand
# python exists at: C:\Users\klavl\.pyenv\pyenv-win\versions\3.11.0\python.exe
# venv exists at: C:\Users\klavl\Documents\GitHub\Math-2B\venv