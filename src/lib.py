import math

import arcade

import src.const as C


def calculate_angle(origin_x, origin_y, target_x, target_y):
    """Calculates the angle between 2 points, result is in radians"""
    small_value = 0.000001

    numer = origin_y - target_y
    denom = origin_x - target_x

    if denom == 0:
        denom = small_value

    angle = math.degrees(math.atan(numer / denom))

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


def find_next_texture(delta_time: float,
                      current_texture: float,
                      texture_list: list[arcade.SpriteList],
                      animation_speed: float = 1) -> float:
    """ Return the next texture to be used """
    # Ensure multiple textures available
    if len(texture_list) > 1:
        # Consume time steps
        while delta_time >= C.TARGET_REFRESH_TIME:
            # Advance the texture
            current_texture += animation_speed * delta_time
            texture_list_max_index = len(texture_list) - 1

            # Stay within the texture list
            while current_texture >= texture_list_max_index:
                current_texture -= texture_list_max_index

            delta_time -= C.TARGET_REFRESH_TIME
        return current_texture
    return 0
