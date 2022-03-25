import arcade
import const.constants as C
from mainmenu import MainMenu


def main():
    """Main function"""
    window = arcade.Window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT,
                           C.SCREEN_TITLE, C.FULLSCREEN, center_window=C.CENTER_WINDOW)
    window.set_mouse_visible(C.CURSOR_VISIBLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
