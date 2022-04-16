import arcade

import src.const as C
from src.audio import Audio
from src.sprite.bullet import Bullet
from src.sprite.enemy import Enemy
from src.save_data import GameData
from src.lib import global_scale
from src.tracker import Tracker


class GameOverView(arcade.View):
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
        self.sfx_meow = None

        self.game_view = game_view
        self.map_view = map_view
        self.current_level = current_level

        self.btn_dict_ = [
            {"img_name": "btn_back_to_map.png",
             "name": "back_to_map",
             "center_x": C.SCREEN_WIDTH * .5 // 1,
             "center_y": C.SCREEN_HEIGHT * .65 // 1,
             },
            {"img_name": "btn_main_menu.png",
             "name": "main_menu",
             "center_x": C.SCREEN_WIDTH * .5 // 1,
             "center_y": C.SCREEN_HEIGHT * .50 // 1,
             },
            {"img_name": "btn_quit_game.png",
             "name": "quit_game",
             "center_x": C.SCREEN_WIDTH * .5 // 1,
             "center_y": C.SCREEN_HEIGHT * .35 // 1,
             },
        ]
        # Find & set pause menu bgm
        view = None
        for view_dict in C.VIEW_LIST:
            if view_dict["name"] == "Pause":
                view = view_dict
        for _i, bgm in enumerate(Audio.bgm_list):
            if bgm["view_name"] == view["name"]:
                self.bgm = bgm["sound"]
                break
        # Find & set click sfx
        for _i, sfx in enumerate(Audio.sfx_list):
            if sfx["file_name"] == "ui/" + C.AUDIO.SOUND["ui_click"]["name"]:
                self.sfx_click = sfx["sound"]
                break

        # Find & set meow sfx
        for _i, sfx in enumerate(Audio.sfx_list):
            if sfx["file_name"] == "ui/" + C.AUDIO.SOUND["ui_meow"]["name"]:
                self.sfx_meow = sfx["sound"]
                break

        # Start bgm
        self.bgm_stream = Audio.play_sound(self.bgm, True)

    def setup(self):
        """ Set up everything with the pause view """

        # Create the sprites
        self.background = arcade.load_texture(
            "src/resources/images/pause_view/game_over_screen.png")
        self.cursor_sprite = arcade.Sprite(
            "src/resources/images/goat_cursor.png", 1)

        # Create the buttons sprite list
        self.btn_list = arcade.SpriteList(is_static=True)
        for btn_dict in self.btn_dict_:
            button = arcade.Sprite(
                filename="src/resources/images/pause_view/" + btn_dict["img_name"],
                scale=self.normal_scale)
            button.name = btn_dict["name"]
            button.center_x = btn_dict["center_x"]
            button.center_y = btn_dict["center_y"]
            self.btn_list.append(button)

    def on_show(self):
        """Called when switching to this view."""
        self.setup()

    def on_draw(self):
        """Draw the menu"""
        self.clear()

        # Draw the bg image
        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x=0,
            bottom_left_y=0,
            width=arcade.get_window().width,
            height=arcade.get_window().height,
            texture=self.background)

        # Draw the score
        arcade.draw_text(
            text=f"Score : {Tracker.score}",
            start_x=C.SCREEN_WIDTH * .05,
            start_y=C.SCREEN_HEIGHT * .95,
            color=arcade.color.BLACK,
            font_name="Kenney High",
            font_size=50 * global_scale(),
            anchor_x="left",
            anchor_y="top",
        )
        # Draw gold
        arcade.draw_text(
            text=f"Gold : {Tracker.gold}",
            start_x=C.SCREEN_WIDTH * .05,
            start_y=C.SCREEN_HEIGHT * .86,
            color=arcade.color.BLACK,
            font_name="Kenney High",
            font_size=50 * global_scale(),
            anchor_x="left",
            anchor_y="top",
        )
        # Draw kills
        arcade.draw_text(
            text=f"Kills : {Tracker.kills}",
            start_x=C.SCREEN_WIDTH * .05,
            start_y=C.SCREEN_HEIGHT * .78,
            color=arcade.color.BLACK,
            font_name="Kenney High",
            font_size=50 * global_scale(),
            anchor_x="left",
            anchor_y="top",
        )

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

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""

        hit_btn = arcade.check_for_collision_with_list(
            self.cursor_sprite, self.btn_list)
        if hit_btn:

            # Play click sfx
            Audio.play_sound(self.sfx_click)

            if hit_btn[0].name == "quit_game":
                self.quit_game()
            elif hit_btn[0].name == "back_to_map":
                self.to_map()
            elif hit_btn[0].name == "main_menu":
                # TODO: Add main menu
                self.to_map()

        # If hit the cat
        _scale = global_scale()
        if 20 * _scale < _x < 120 * _scale and 270 * _scale < _y < 370 * _scale:
            Audio.play_sound(self.sfx_meow)
            Tracker.trigger_easter_egg()

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

        # Reset bullets
        Bullet.friendly_bullet_list = arcade.SpriteList()
        Bullet.enemy_bullet_list = arcade.SpriteList()

        # Reset enemies
        Enemy.enemy_list = arcade.SpriteList()
