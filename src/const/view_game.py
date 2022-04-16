import arcade.csscolor

from .window import *


# TODO: Refactor constants into single dict, `GAME_GUI`?
GAME_BACKGROUND_COLOR = arcade.csscolor.DARK_GREEN

GUI = {
    "Weapon": {
        "center_x": SCREEN_WIDTH * .33,
        "center_y": SCREEN_HEIGHT * .95
    },
    "Crosshair": {
        "offset_x": 25,
        "offset_y": -25
    }
}
