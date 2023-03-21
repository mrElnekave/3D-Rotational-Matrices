import math

def rotate_pt(x, y, z, roll, pitch, yaw):
    cosp, sinp = math.cos(pitch), math.sin(pitch)
    cosy, siny = math.cos(yaw), math.sin(yaw)
    cosr, sinr = math.cos(roll), math.sin(roll)

    rx = cosp * cosy * x + (cosp * siny * sinr - sinp * cosr) * y + (sinp * sinr + cosp * siny * cosr) * z
    ry = sinp * cosy * x + (cosp * cosr + sinp * siny * sinr) * y + (sinp * siny * cosr - cosp * sinr) * z
    rz = (cosy * sinr) * y + (cosy * cosr) * z - siny * x

    return int(rx), int(ry), int(rz)