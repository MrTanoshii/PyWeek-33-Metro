import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_FONT_SIZE, MENU_BACKGROUND_COLOR


class PauseMenuView(arcade.View):
    """Class that manages the 'menu' view."""

    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(MENU_BACKGROUND_COLOR)

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        arcade.draw_text(
            "Game Paused - ESC to exit | Any key to resume",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=MENU_FONT_SIZE,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        self.window.show_view(self.game_view)

    def on_key_press(self, key, modifiers):
        """Handle keyboard key press"""
        if key == arcade.key.ESCAPE:
            arcade.exit()
        else:
            self.window.show_view(self.game_view)
