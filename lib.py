import math
import arcade
import const.constants as C


def calculate_angle(origin_x, origin_y, target_x, target_y):
    """Calculates the angle between 2 points, result is in radians"""
    denom = origin_x - target_x
    if denom == 0:
        denom = 0.00001
    angle = math.degrees(math.atan((origin_y - target_y) /
                                   (denom)))
    return angle


def global_scale() -> float:
    return arcade.get_window().width / 1280
