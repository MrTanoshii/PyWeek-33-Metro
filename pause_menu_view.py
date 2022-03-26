import arcade
import const.constants as C
from audio import Audio
from gamedata import GameData
from tracker import Tracker
import shopview
from lib import global_scale


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

        self.cursor_sprite = None
        self.background = None
        self.btn_list = None
        self.highlight = False
        self.normal_scale = 0.8
        self.highlight_scale = 1

        self.bgm_stream = None
        self.sfx_click = None

        self.game_view = game_view
        self.map_view = map_view
        self.current_level = current_level

        self.btn_dict_ = [
            {"img_name": "btn_resume.png",
             "name": "resume",
             "center_x": C.SCREEN_WIDTH * .75 // 1,
             "center_y": C.SCREEN_HEIGHT * .65 // 1,
             },
            {"img_name": "btn_back_to_map.png",
             "name": "back_to_map",
             "center_x": C.SCREEN_WIDTH * .75 // 1,
             "center_y": C.SCREEN_HEIGHT * .5 // 1,
             },
            {"img_name": "btn_main_menu.png",
             "name": "main_menu",
             "center_x": C.SCREEN_WIDTH * .75 // 1,
             "center_y": C.SCREEN_HEIGHT * .35 // 1,
             },
            {"img_name": "btn_quit_game.png",
             "name": "quit_game",
             "center_x": C.SCREEN_WIDTH * .75 // 1,
             "center_y": C.SCREEN_HEIGHT * .20 // 1,
             },
        ]
        # Find & set pause menu bgm
        view = None
        for view_dict in C.VIEW_LIST:
            if view_dict["name"] == "Pause":
                view = view_dict
        for i in range(0, len(Audio.bgm_list)):
            if Audio.bgm_list[i]["view_name"] == view["name"]:
                self.bgm = Audio.bgm_list[i]["sound"]
                break
        # Find & set click sfx
        for i in range(0, len(Audio.sfx_list)):
            if Audio.sfx_list[i]["file_name"] == "ui/" + C.AUDIO.SOUND["ui_click"]["name"]:
                self.sfx_click = Audio.sfx_list[i]["sound"]
                break

        # Start bgm
        self.bgm_stream = Audio.play_sound(self.bgm, True)

    def setup(self):
        """ Set up everything with the pause view """

        # Create the sprites
        self.background = arcade.load_texture(
            "resources/images/pause_view/screen_pause.png")
        self.cursor_sprite = arcade.Sprite(
            "resources/images/goat_cursor.png", 1)

        # Create the buttons sprite list
        self.btn_list = arcade.SpriteList(is_static=True)
        for btn_dict in self.btn_dict_:
            button = arcade.Sprite(
                filename="resources/images/pause_view/" + btn_dict["img_name"],
                scale=self.normal_scale * global_scale())
            button.name = btn_dict["name"]
            button.center_x = btn_dict["center_x"] * global_scale()
            button.center_y = btn_dict["center_y"] * global_scale()
            self.btn_list.append(button)

    def on_show(self):
        """Called when switching to this view."""
        self.setup()

    def on_draw(self):
        """Draw the menu"""
        self.clear()

        # Draw the bg image
        arcade.draw_lrwh_rectangle_textured(0, 0, C.SCREEN_WIDTH * global_scale(), C.SCREEN_HEIGHT * global_scale(), self.background)

        # Draw buttons
        self.btn_list.draw()

        # Draw the cursor
        self.cursor_sprite.draw()

    def on_update(self, delta_time: float):
        hit_list = arcade.check_for_collision_with_list(
            self.cursor_sprite, self.btn_list)

        if len(hit_list):
            for i, monument in enumerate(self.btn_list):
                if i != self.btn_list.index(hit_list[0]):
                    monument.scale = self.normal_scale
                else:
                    monument.scale = self.highlight_scale
                    self.highlight = True
        elif self.highlight:
            for monument in self.btn_list:
                monument.scale = self.normal_scale
            self.highlight = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_sprite.center_x = x + \
            C.MAP["Cursor"]["offset_x"] * global_scale()
        self.cursor_sprite.center_y = y + \
            C.MAP["Cursor"]["offset_y"] * global_scale()

        # # Check if shops hit cursor (Simply because less number of checking)
        # if self.shop_sprite.collides_with_sprite(self.cursor_sprite):
        #     self.shop_sprite.color = (0, 255, 0)
        #     self.shop_sprite.scale = .24 * global_scale()
        # else:
        #     self.shop_sprite.color = (255, 255, 255)
        #     self.shop_sprite.scale = .2 * global_scale()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""

        hit_btn = arcade.check_for_collision_with_list(
            self.cursor_sprite, self.btn_list)
        if hit_btn:

            # Play click sfx
            Audio.play_sound(self.sfx_click)

            if hit_btn[0].name == "resume":
                self.resume()
            elif hit_btn[0].name == "quit_game":
                self.quit_game()
            elif hit_btn[0].name == "back_to_map":
                self.to_map()
            elif hit_btn[0].name == "main_menu":
                # TODO: Add main menu
                self.to_map()

        # If hit the cat
        _scale = global_scale()
        if 20 * _scale < _x < 120 * _scale and 270 * _scale < _y < 370 * _scale:
            Audio.play_sound(self.sfx_click)
            # TODO: Add something special

    def on_key_press(self, key, _modifiers):
        """Handle keyboard key press"""
        if key == arcade.key.Q:
            self.quit_game()
        elif key == arcade.key.M:
            self.to_map()
        elif key == arcade.key.SPACE:
            self.resume()
        elif key == arcade.key.S:  # Added binding
            self.window.show_view(shopview.ShopView())

    def resume(self):
        Audio.stop_sound(self.bgm_stream)
        self.bgm_stream = None
        self.window.show_view(self.game_view)

    def quit_game(self):
        # Stop bgm
        Audio.stop_sound(self.bgm_stream)
        self.bgm_stream = None
        arcade.exit()

    def to_map(self):
        Audio.stop_sound(self.bgm_stream)
        self.bgm_stream = None
        self.window.show_view(self.map_view)
        self.exit_level()

    def exit_level(self):
        GameData.update_highscore(self.current_level)
        GameData.deposit_gold()
        Tracker.reset_trackers()
