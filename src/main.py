import arcade
import pyglet

import src.const as C

from src.view.main_menu import MainMenu


def main():
    """Main function"""
    if C.FULLSCREEN:
        window = arcade.Window(
            width=arcade.get_display_size()[0],
            height=arcade.get_display_size()[1],
            title=C.SCREEN_TITLE,
            fullscreen=True,
        )
    elif C.FULLSCREEN_WINDOWED:
        window = arcade.Window(
            width=arcade.get_display_size()[0],
            height=arcade.get_display_size()[1],
            title=C.SCREEN_TITLE,
            style="borderless"
        )
    else:
        window = arcade.Window(
            width=C.SCREEN_WIDTH,
            height=C.SCREEN_HEIGHT,
            title=C.SCREEN_TITLE,
            center_window=not C.CENTER_WINDOW,
            resizable=True
        )

    window.set_mouse_visible(C.CURSOR_VISIBLE)
    icon = pyglet.image.load('src/resources/images/goat_cursor.png')
    window.set_icon(icon)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
