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
    C.SCREEN_WIDTH = arcade.get_window().width
    C.SCREEN_HEIGHT = arcade.get_window().height
    return arcade.get_window().width / 1280


def draw_text(text: str, start_x: float, start_y: float, font_size: float = 30,
              color: tuple = arcade.color.BLACK, anchor_x: str = "center"):
    """ Wrapper for drawing text using arcade.draw_text() """
    arcade.draw_text(
        text,
        start_x * .99,
        start_y * 1.005,
        color,
        font_name="Kenney High",
        bold=True,
        font_size=font_size * global_scale(),
        anchor_x=anchor_x,
        anchor_y="center",
    )
