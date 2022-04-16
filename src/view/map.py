
import arcade

import src.const as C

from src.audio import Audio
from src.lib import global_scale
import src.save_data as save_data

from src.sprite.player import Player

from src.view.game import GameView
from src.view.shop import ShopView
from src.view.story import StoryView
from src.view.quit import QuitView


class MapView(arcade.View):
    """
    MapView View

    ...

    Attributes
    ----------
    current_level : int
        Hold the current level

    Methods
    -------
    setup()
        Set up the map view and initialize the variables
    load_monuments()
        Load the monuments
    on_draw()
        Draw the map view
    on_mouse_motion(x: float, y: float, dx: float, dy: float)
        Listen to mouse motion event
    on_key_press(key: int, modifiers: int)
        Listen to keyboard press event
    on_update(delta_time: float)
        Update the map view
    on_mouse_press(x: float, y: float, button: int, modifiers: int)
        Listen to mouse press event
    on_show()
        Show the map view
    """

    # Level class attribute
    current_level = 0
    monument_list = []
    step_list = []

    def __init__(self):
        # Inherit parent class
        super().__init__()

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.cursor_sprite = None
        self.cursor_list = None

        self.background = None

        self.level = 0

        self.game_view = None

        # Monuments
        self.normal_scale = .2 * global_scale()
        self.highlight_scale = .3 * global_scale()
        self.highlight = False

        # Steps
        self.normal_scale_step = C.STEP_CONFS["story_scale"] * global_scale()
        self.highlight_scale_step = C.STEP_CONFS["story_scale_big"] * \
            global_scale()
        self.highlight_step = False

        """ Map sprites """
        self.shop_sprite = None
        self.gold_sprite = None
        # Find & set map bgm
        view = None
        for view_dict in C.VIEW_LIST:
            if view_dict["name"] == "Map":
                view = view_dict
        for _i, bgm in enumerate(Audio.bgm_list):
            if bgm["view_name"] == view["name"]:
                self.bgm = bgm["sound"]
                break

        # Start bgm
        self.bgm_stream = Audio.play_sound(self.bgm, True)

    def setup(self):
        """ Set up everything with the game """

        Player.player_list = arcade.SpriteList()

        # self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        MapView.monument_list = arcade.SpriteList(is_static=True)
        MapView.step_list = arcade.SpriteList(is_static=True)

        self.cursor_list = arcade.SpriteList()
        # Create the sprite lists
        self.background = arcade.load_texture(
            "src/resources/images/map/pixel_map.png")
        self.cursor_sprite = arcade.Sprite(
            "src/resources/images/goat_cursor.png", 1)

        # setup map sprites
        # Initializing a global Shop Sprite URL - https://www.iconsdb.com/white-icons/shop-icon.html
        self.shop_sprite = arcade.Sprite(
            "src/resources/images/map/temp_shop.png", 0.2 * global_scale())
        self.gold_sprite = arcade.Sprite(
            "src/resources/images/map/gold-bar.png", 0.6 * global_scale())

        # Sprite Locations
        self.gold_sprite.position = (
            1200 * global_scale(), 680 * global_scale())
        self.shop_sprite.position = (
            int(C.SCREEN_WIDTH * .96), int(C.SCREEN_HEIGHT * .87))

        self.cursor_list.append(self.cursor_sprite)
        self.load_monuments()
        self.load_steps()

    def load_monuments(self):
        """Loads map monuments onto map"""
        for mon_dict in C.MAP_MONUMENTS_LIST:
            monument = arcade.Sprite(
                "src/resources/images/map/" + mon_dict["img_name"],
                self.normal_scale)
            monument.level = mon_dict["level"]
            monument.name = mon_dict["name"]
            monument.center_x = mon_dict["center_x"] * global_scale()
            monument.center_y = mon_dict["center_y"] * global_scale()

            if save_data.GameData.level_data[str(monument.level)]["passed"] == 0 \
                and save_data.GameData.level_data[str(monument.level)][
                    "locked"] == 0:
                monument.color = (255, 255, 64)
                monument.unlocked = True
            elif save_data.GameData.level_data[str(monument.level)]["passed"] == 0 \
                and save_data.GameData.level_data[str(monument.level)][
                    "locked"] == 1:
                monument.color = (255, 64, 64)
                monument.unlocked = False
            else:
                monument.color = (255, 255, 255)
                monument.unlocked = True

            # Find & set click sfx
            for _i, sfx in enumerate(Audio.sfx_ui_list):
                if sfx["ui_name"] == monument.name:
                    monument.sfx_click = sfx["sound"]
                    break

            MapView.monument_list.append(monument)

    @classmethod
    def load_steps(cls):
        """Loads map monuments onto map"""
        confs = C.STEP_CONFS
        level = 0
        passed = True
        for step_dict in C.MAP_STEP_LIST:
            if step_dict["type"] == "step":
                step = arcade.Sprite(
                    "src/resources/images/map/step.png",
                    confs["step_scale"] * global_scale())
                step.type = step_dict["type"]
                step.level = None
                step.center_x = step_dict["center_x"] * global_scale()
                step.center_y = step_dict["center_y"] * global_scale()
                if passed:
                    step.color = (64, 200, 64)
                else:
                    step.color = (200, 64, 64)
            else:
                step = arcade.Sprite(
                    "src/resources/images/map/step.png",
                    confs["story_scale"] * global_scale())
                step.level = level
                level += 1
                step.type = step_dict["type"]
                step.center_x = step_dict["center_x"] * global_scale()
                step.center_y = step_dict["center_y"] * global_scale()

                # locked
                if save_data.GameData.story[str(step.level)] == 0:
                    step.color = (255, 64, 64)
                    step.unlocked = False
                    step.passed = False
                    passed = False
                # un-locked
                elif save_data.GameData.story[str(step.level)] == 1:
                    step.color = (255, 255, 64)
                    step.unlocked = True
                    passed = False
                # passed
                elif save_data.GameData.story[str(step.level)] == 2:
                    step.color = (64, 255, 64)
                    step.unlocked = True
                    step.passed = True
                    passed = True
                    _unlocked = True
                # Find & set click sfx
                # TODO: Set sfx for steps
                for _i, sfx in enumerate(Audio.sfx_ui_list):
                    if sfx["ui_name"] == "EGYPT":
                        step.sfx_click = sfx["sound"]
                        break

            MapView.step_list.append(step)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        arcade.draw_lrwh_rectangle_textured(
            bottom_left_x=0,
            bottom_left_y=0,
            width=arcade.get_window().width,
            height=arcade.get_window().height,
            texture=self.background)

        self.gold_sprite.draw()
        # GUI - Gold
        arcade.draw_text(
            save_data.GameData.gold,
            self.gold_sprite.position[0] * .99,
            self.gold_sprite.position[1] * 1.005,
            arcade.color.BLACK,
            font_name="Kenney High",
            bold=True,
            font_size=30 * global_scale(),
            anchor_x="left",
            anchor_y="center",
        )

        for step in MapView.step_list:
            step.draw()
        for monument in MapView.monument_list:
            monument.draw()
        self.shop_sprite.draw(pixelated=True)
        self.cursor_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_sprite.center_x = x + \
            C.MAP["Cursor"]["offset_x"] * global_scale()
        self.cursor_sprite.center_y = y + \
            C.MAP["Cursor"]["offset_y"] * global_scale()

        # Check if shops hit cursor (Simply because less number of checking)
        if self.shop_sprite.collides_with_sprite(self.cursor_sprite):
            self.shop_sprite.color = (0, 255, 0)
            self.shop_sprite.scale = .24 * global_scale()
        else:
            self.shop_sprite.color = (255, 255, 255)
            self.shop_sprite.scale = .2 * global_scale()

    def on_key_press(self, symbol, modifiers):
        """ Listen to keyboard press event """

        if symbol == arcade.key.ESCAPE:
            self.window.show_view(QuitView(self))

    def on_update(self, delta_time):

        hit_list_monument = arcade.check_for_collision_with_list(
            self.cursor_sprite, MapView.monument_list)

        if len(hit_list_monument):
            for i, monument in enumerate(MapView.monument_list):
                if i != MapView.monument_list.index(hit_list_monument[0]):
                    monument.scale = self.normal_scale
                else:
                    monument.scale = self.highlight_scale
                    self.highlight = True
        elif self.highlight:
            for monument in MapView.monument_list:
                monument.scale = self.normal_scale
            self.highlight = False

        hit_list_step = arcade.check_for_collision_with_list(
            self.cursor_sprite, MapView.step_list)

        if len(hit_list_step):
            for i, step in enumerate(MapView.step_list):
                if step.level is not None:
                    if i != MapView.step_list.index(hit_list_step[0]):
                        step.scale = self.normal_scale_step
                    else:
                        step.scale = self.highlight_scale_step
                        self.highlight_step = True
        elif self.highlight_step:
            for step in MapView.step_list:
                if step.level is not None:
                    step.scale = self.normal_scale_step
            self.highlight_step = False

        # Restart bgm
        if self.bgm_stream is None:
            self.bgm_stream = Audio.play_sound(self.bgm, True)

        MapView.update_monument_list()

    def on_mouse_press(self, x, y, button, modifiers):

        if C.DEBUG.ALL or C.DEBUG.MAP:
            print(x, y)
        hit_monument = arcade.check_for_collision_with_list(
            self.cursor_sprite, MapView.monument_list)
        hit_step = arcade.check_for_collision_with_list(
            self.cursor_sprite, MapView.step_list)
        if hit_monument:
            if hit_monument[0].unlocked:
                MapView.current_level = hit_monument[0].level

                # Play monument click sfx
                Audio.play_sound(hit_monument[0].sfx_click)

                # Stop bgm
                Audio.stop_sound(self.bgm_stream)
                self.bgm_stream = None

                self.game_view = GameView(self)
                self.game_view.setup()
                self.window.show_view(self.game_view)

        elif hit_step and (hit_step[0].level is not None):
            if hit_step[0].unlocked:
                story_level = hit_step[0].level
                # Play monument click sfx
                Audio.play_sound(hit_step[0].sfx_click)

                # Stop bgm
                Audio.stop_sound(self.bgm_stream)
                self.bgm_stream = None

                # Story opening
                self.window.show_view(StoryView(self, story_level))

        # Check if shops hit cursor (Simply because less number of checking)
        elif self.shop_sprite.collides_with_sprite(self.cursor_sprite):
            self.window.show_view(ShopView(self))

    def open_story(self):
        self.window.show_view(StoryView(self, MapView.current_level))

    def on_show(self):
        self.setup()

    @classmethod
    def update_monument_list(cls):
        for i, monument in enumerate(cls.monument_list):
            if save_data.GameData.level_data[str(i + 1)]["passed"] == 0 \
                    and save_data.GameData.level_data[str(i + 1)]["locked"] == 0:
                monument.color = (255, 255, 64)
                monument.unlocked = True
            elif save_data.GameData.level_data[str(i + 1)]["passed"] == 0 \
                    and save_data.GameData.level_data[str(i + 1)]["locked"] == 1:
                monument.color = (255, 64, 64)
                monument.unlocked = False
            else:
                monument.color = (255, 255, 255)
                monument.unlocked = True

    @classmethod
    def update_step_list(cls):
        cls.step_list = arcade.SpriteList(is_static=True)
        cls.load_steps()
