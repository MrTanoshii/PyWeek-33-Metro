import arcade
import mapview
import const.constants as C
from lib import global_scale
from audio import Audio
from gamedata import GameData


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
            (C.SCREEN_WIDTH / 2) * global_scale(),
            (C.SCREEN_HEIGHT / 2) * global_scale(),
            arcade.color.BLACK,
            font_size=C.MENU_FONT_SIZE * global_scale(),
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        GameData.read_data()
        self.window.show_view(mapview.MapView())
