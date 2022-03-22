import arcade
import mapview
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_FONT_SIZE, MENU_BACKGROUND_COLOR

CENTER_POINTS = [[700, 450], [900, 450]]


class MainMenu(arcade.View):
    """Class that manages the 'menu' view."""

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(MENU_BACKGROUND_COLOR)

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        arcade.draw_text(
            "Main Menu - Click to play",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=MENU_FONT_SIZE,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        self.window.show_view(mapview.MapView())


###Egypt - Pyramid
# China
# Moscow
# Brazil
# London
# Africa
# ##USA
