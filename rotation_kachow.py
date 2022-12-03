from math import cos, sin, pi


def get_x(x, y, z, roll, pitch, yaw):
    return cos(pitch) * cos(yaw) * x  +  (-sin(pitch) * cos(roll) + cos(pitch) * sin(yaw) * sin(roll)) * y  +  (-sin(pitch) * -sin(roll) + cos(pitch) * sin(yaw) * cos(roll)) * z
def get_y(x, y, z, roll, pitch, yaw):
    return sin(pitch) * cos(yaw) * x  +  (cos(pitch) * cos(roll) + sin(pitch) * sin(yaw) * sin(roll)) * y  +  (cos(pitch) * -sin(roll) + sin(pitch) * sin(yaw) * cos(roll)) * z
def get_z(x, y, z, roll, pitch, yaw):
    return -sin(yaw) * x  +  (cos(yaw) * sin(roll)) * y  +  (cos(yaw) * cos(roll)) * z

def get_xyz(x, y, z, roll, pitch, yaw):
    return get_x(x, y, z, roll, pitch, yaw), get_y(x, y, z, roll, pitch, yaw), get_z(x, y, z, roll, pitch, yaw)
