import rubato as rb
from math import cos, sin, pi

rb.init(res=(300, 300), maximize=True)


scene = rb.Scene()

# define rotation functions

def get_x(x, y, z, psi, theta, phi):
    return cos(theta) * x  +  (sin(theta) * sin(psi)) * y  +  (sin(theta) * cos(psi)) * z
    # return cos(theta) * cos(theta) + sin(theta) * cos(psi) * -sin(theta) * x  +  \
    #     (sin(theta) * sin(psi)) * y  +  \
    #         (cos(theta) * sin(theta) + sin(theta) * cos(psi) * cos(theta)) * z

def get_y(x, y, z, psi, theta, phi):
    return sin(theta) * sin(phi) * x  +  \
        (cos(psi) * cos(phi) + cos(theta) * sin(psi) * sin(phi)) * y  +  \
            (-cos(phi) * sin(psi) + -cos(theta) * cos(psi) * sin(phi)) * z
    # return -sin(psi) * -sin(theta) * x  +  \
    #     (cos(psi)) * y  +  \
    #         (-sin(psi) * cos(theta)) * z

def get_z(x, y, z, psi, theta, phi):
    return -sin(theta) * cos(phi) * x  +  \
        (cos(psi) * sin(phi) + cos(theta) * cos(phi) * sin(psi)) * y  +  \
            (-sin(psi) * sin(phi) + cos(theta) * cos(psi) * cos(phi)) * z  
    # return -sin(theta) * cos(theta) + cos(theta) * cos(psi) * -sin(theta) * x  +  \
    #     (cos(theta) * sin(psi)) * y  +  \
    #         (-sin(theta) * sin(theta) + cos(theta) * cos(psi) * cos(theta)) * z



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
    # psi += 0.01
    # theta += 0.01
    # phi += 0.01

    # theta must be capped 0 < theta < pi
    
    for x in range(-width, width):
        for y in range(-height, height):
            # I have to calculate for front of cube

            # since y-axis is up, x-axis is right, and z-axis is out of screen
            x = get_x(x, y, depth, psi, theta, phi)
            y = get_y(x, y, depth, psi, theta, phi)
            z = get_z(x, y, depth, psi, theta, phi)

            rb.Draw.queue_rect(rb.Vector(x, y),1,1, rb.Color.cyan, z_index=int(z))

            # and back of cube
            # y-axis is up, x-axis is right, and z-axis is out of screen
            # x = get_x(x, y, depth, psi, theta, phi)
            # y = get_y(x, y, depth, psi, theta, phi)
            # z = get_z(x, y, depth, psi, theta, phi)
            # rb.Draw.queue_pixel(rb.Vector(x, y), rb.Color(255, 0, 0), z_index=int(z))
    rb.Draw.queue_circle(center, radius=2, border=None, fill=rb.Color(0, 0, 255), z_index=10000)
    rb.Draw.queue_line(center, center+rb.Vector.right() * 20, rb.Color(255, 0, 0), z_index=10000)
    rb.Draw.queue_line(center, center+rb.Vector.up() * 20, rb.Color(0, 255, 0), z_index=10000)

scene.draw = custom_draw

def custom_update():
    global psi, theta, phi
    if rb.Input.key_pressed("space"):
        theta += 0.01

scene.update = custom_update

rb.begin()
print("Get x: ", get_x(-1, 2, 3, 0, 0, 0))
print("Get y: ", get_y(-1, 2, 3, 0, 0, 0))
print("Get z: ", get_z(-1, 2, 3, 0, 0, 0))

# python venv commmand
# python exists at: C:\Users\klavl\.pyenv\pyenv-win\versions\3.11.0\python.exe
# venv exists at: C:\Users\klavl\Documents\GitHub\Math-2B\venv