import arcade
from const.window import *


# TODO: Refactor constants into single dict, `GAME_GUI`?
GAME_BACKGROUND_COLOR = arcade.csscolor.DARK_GREEN

GUI = {
    "Weapon": {
        "center_x": (SCREEN_WIDTH / 5) + 500,
        "center_y": SCREEN_HEIGHT - 90
    }
}
