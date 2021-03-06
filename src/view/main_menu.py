import arcade

import src.const as C

from src.audio import Audio
from src.lib import global_scale
import src.save_data as save_data

from src.view.map import MapView


class MainMenu(arcade.View):
    """
    MainMenu View

    ...

    Methods
    -------
    on_show()
        Show the main menu
    on_draw()
        Draw the main menu
    on_mouse_press(x: float, y: float, button: int, modifiers: int)
        Listen to mouse press event
    """

    def __init__(self):
        # Inherit parent class
        super().__init__()

        # Load sounds
        self.audio = Audio()

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(C.MENU_BACKGROUND_COLOR)

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        arcade.draw_text(
            "Main Menu - Click to play",
            C.SCREEN_WIDTH / 2,
            C.SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=C.MENU_FONT_SIZE * global_scale(),
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        save_data.GameData.read_data()
        self.window.show_view(MapView())
