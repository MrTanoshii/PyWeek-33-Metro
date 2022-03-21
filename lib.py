import math


def calculate_angle(origin_x, origin_y, target_x, target_y):
    """Calculates the angle between 2 points, result is in radians"""
    angle = math.degrees(math.atan((origin_y - target_y) /
                                   (origin_x - target_x)))
    return angle
