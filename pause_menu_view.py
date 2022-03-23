import arcade
import constants as C
from gamedata import GameData


class PauseMenuView(arcade.View):
    """
    PauseMenuView View

    ...

    Methods
    -------
    on_show()
        Show the pause menu view
    on_draw()
        Draw the pause menu view
    on_mouse_press(x: float, y: float, button: int, modifiers: int)
        Listen to mouse press event
    on_key_press(key: int, modifiers: int)
        Listen to keyboard press event
    """

    def __init__(self, game_view, map_view, current_level):
        # Inherit parent class
        super().__init__()

        self.game_view = game_view
        self.map_view = map_view
        self.current_level = current_level

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(C.MENU_BACKGROUND_COLOR)

    def on_draw(self):
        """Draw the menu"""
        self.clear()

        arcade.draw_text(
            "Paused | Q: quit game | M: leave level | SPACE: back to game",
            C.SCREEN_WIDTH / 2,
            C.SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=C.MENU_FONT_SIZE,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        self.window.show_view(self.game_view)

    def on_key_press(self, key, _modifiers):
        """Handle keyboard key press"""
        if key == arcade.key.Q:
            arcade.exit()
        elif key == arcade.key.M:
            self.window.show_view(self.map_view)
            self.save_data()
        elif key == arcade.key.SPACE:
            self.window.show_view(self.game_view)

    def save_data(self):
        GameData.update_highscore(self.current_level)
        GameData.deposit_gold()
