import arcade
import constants as C
from audio import Audio
from gamedata import GameData
from tracker import Tracker


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

        # Find & set pause menu bgm
        view = None
        for view_dict in C.VIEW_LIST:
            if view_dict["name"] == "Pause":
                view = view_dict
        for i in range(0, len(Audio.bgm_list)):
            if Audio.bgm_list[i]["view_name"] == view["name"]:
                self.bgm = Audio.bgm_list[i]["sound"]
                break

        # Start bgm
        self.bgm_stream = Audio.play_sound(self.bgm)

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

        # Stop bgm
        Audio.stop_sound(self.bgm_stream)

        self.window.show_view(self.game_view)

    def on_key_press(self, key, _modifiers):
        """Handle keyboard key press"""
        if key == arcade.key.Q:
            # Stop bgm
            Audio.stop_sound(self.bgm_stream)
            self.bgm_stream = None
            arcade.exit()
        elif key == arcade.key.M:
            Audio.stop_sound(self.bgm_stream)
            self.bgm_stream = None
            self.window.show_view(self.map_view)
            self.exit_level()
        elif key == arcade.key.SPACE:
            Audio.stop_sound(self.bgm_stream)
            self.bgm_stream = None
            self.window.show_view(self.game_view)

    def exit_level(self):
        GameData.update_highscore(self.current_level)
        GameData.deposit_gold()
        Tracker.reset_trackers()
