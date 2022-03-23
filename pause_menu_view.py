import arcade
import constants as C


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

    def __init__(self, game_view):
        # Inherit parent class
        super().__init__()

        self.game_view = game_view

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(C.MENU_BACKGROUND_COLOR)

    def on_draw(self):
        """Draw the menu"""
        self.clear()

        arcade.draw_text(
            "Game Paused - ESC to exit | Any key to resume",
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
        if key == arcade.key.ESCAPE:
            arcade.exit()
        else:
            self.window.show_view(self.game_view)
