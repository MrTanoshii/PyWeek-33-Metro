import arcade

import src.const as C

from src.lib import global_scale


class QuitView(arcade.View):
    """
    Quit View

    ...

    Methods
    -------
    on_show()
        Called when switching to this view
    on_draw()
        Called when drawing the view
    on_mouse_press(x: float, y: float, button: int, modifiers: int)
        Listen to mouse press event
    """

    def __init__(self, previous_view: arcade.View):
        # Inherit parent class
        super().__init__()

        self.previous_view = previous_view

    def on_show(self):
        """ Called when switching to this view """

        arcade.set_background_color(C.MENU_BACKGROUND_COLOR)

    def on_draw(self):
        """ Called when drawing the view """

        self.clear()

        arcade.draw_text(
            "Quit the game?",
            C.SCREEN_WIDTH / 2,
            C.SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=C.MENU_FONT_SIZE * global_scale(),
            anchor_x="center",
        )

        arcade.draw_text(
            "ESC - Quit",
            C.SCREEN_WIDTH / 2,
            (C.SCREEN_HEIGHT / 2) - 100,
            arcade.color.BLACK,
            font_size=C.MENU_FONT_SIZE * global_scale(),
            anchor_x="center",
        )

        arcade.draw_text(
            "Enter - Resume",
            C.SCREEN_WIDTH / 2,
            (C.SCREEN_HEIGHT / 2) - 200,
            arcade.color.BLACK,
            font_size=C.MENU_FONT_SIZE * global_scale(),
            anchor_x="center",
        )

    def on_key_press(self, symbol, modifiers):
        """ Listen to keyboard press event """

        if symbol == arcade.key.ENTER:
            self.window.show_view(self.previous_view)
        elif symbol == arcade.key.ESCAPE:
            arcade.exit()
