import const.constants as C
import gameview
import arcade
from player import Player
import shopview
from audio import Audio
from gamedata import GameData
from lib import global_scale
from story_view import StoryView


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
    on_update(delta_time: float)
        Update the map view
    on_mouse_press(x: float, y: float, button: int, modifiers: int)
        Listen to mouse press event
    on_show()
        Show the map view
    """

    # Level class attribute
    current_level = 0
    monument_list = None

    def __init__(self):
        # Inherit parent class
        super().__init__()

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.cursor_sprite = None
        self.cursor_list = None

        self.background = None

        self.level = 0
        self.normal_scale = .2 * global_scale()
        self.highlight_scale = .5 * global_scale()
        self.highlight = False

        """ Map sprites """
        self.shop_sprite = None
        self.gold_sprite = None
        # Find & set map bgm
        view = None
        for view_dict in C.VIEW_LIST:
            if view_dict["name"] == "Map":
                view = view_dict
        for i in range(0, len(Audio.bgm_list)):
            if Audio.bgm_list[i]["view_name"] == view["name"]:
                self.bgm = Audio.bgm_list[i]["sound"]
                break

        # Start bgm
        self.bgm_stream = Audio.play_sound(self.bgm, True)

    def setup(self):
        """ Set up everything with the game """

        Player.player_list = arcade.SpriteList()

        # self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        MapView.monument_list = arcade.SpriteList(is_static=True)

        self.cursor_list = arcade.SpriteList()
        # Create the sprite lists
        self.background = arcade.load_texture(
            "resources/images/map/pixel_map.png")
        self.cursor_sprite = arcade.Sprite(
            "resources/images/goat_cursor.png", 1)

        # setup map sprites
        # Initializing a global Shop Sprite URL - https://www.iconsdb.com/white-icons/shop-icon.html
        self.shop_sprite = arcade.Sprite(
            "resources/images/map/temp_shop.png", 0.2 * global_scale())
        # Initializing a global Shop Sprite URL - https://www.iconsdb.com/white-icons/shop-icon.html
        self.gold_sprite = arcade.Sprite(
            "resources/images/map/gold-bar.png", 0.6 * global_scale())

        # Sprite Locations
        self.gold_sprite.position = (
            1200 * global_scale(), 680 * global_scale())
        self.shop_sprite.position = (
            int(C.SCREEN_WIDTH * .96 * global_scale()), int(C.SCREEN_HEIGHT * .87 * global_scale()))

        self.cursor_list.append(self.cursor_sprite)
        self.load_monuments()

    def load_monuments(self):
        """Loads map monuments onto map"""
        for mon_dict in C.MAP_MONUMENTS_LIST:
            monument = arcade.Sprite(
                "resources/images/map/" + mon_dict["img_name"],
                self.normal_scale * global_scale())
            monument.level = mon_dict["level"]
            monument.name = mon_dict["name"]
            monument.center_x = mon_dict["center_x"] * global_scale()
            monument.center_y = mon_dict["center_y"] * global_scale()

            if GameData.level_data[str(monument.level)]["passed"] == 0 and GameData.level_data[str(monument.level)]["locked"] == 0:
                monument.color = (255, 255, 64)
                monument.unlocked = True
            elif GameData.level_data[str(monument.level)]["passed"] == 0 and GameData.level_data[str(monument.level)]["locked"] == 1:
                monument.color = (255, 64, 64)
                monument.unlocked = False
            else:
                monument.color = (255, 255, 255)
                monument.unlocked = True

            # Find & set click sfx
            for i in range(0, len(Audio.sfx_ui_list)):
                if Audio.sfx_ui_list[i]["ui_name"] == monument.name:
                    monument.sfx_click = Audio.sfx_ui_list[i]["sound"]
                    break

            MapView.monument_list.append(monument)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            C.SCREEN_WIDTH * global_scale(), C.SCREEN_HEIGHT * global_scale(),
                                            self.background)
        self.gold_sprite.draw()
        # GUI - Gold
        arcade.draw_text(
            GameData.gold,
            self.gold_sprite.position[0]*.99,
            self.gold_sprite.position[1]*1.005,
            arcade.color.BLACK,
            font_name="Kenney High",
            bold=True,
            font_size=30 * global_scale(),
            anchor_x="left",
            anchor_y="center",
        )

        # arcade.draw_text(
        #     f"SHOP",
        #     self.shop_sprite.position[0],
        #     self.shop_sprite.position[1]*.9,
        #     arcade.color.BLACK,
        #     font_size=20,
        #     anchor_x="center",
        # )

        MapView.monument_list.draw()
        self.shop_sprite.draw(pixelated=True)
        self.cursor_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.S:
            # Story opening
            self.open_story()

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

    def on_update(self, delta_time):

        hit_list = arcade.check_for_collision_with_list(
            self.cursor_sprite, MapView.monument_list)

        if len(hit_list):
            for i, monument in enumerate(MapView.monument_list):
                if i != MapView.monument_list.index(hit_list[0]):
                    monument.scale = self.normal_scale
                else:
                    monument.scale = self.highlight_scale
                    self.highlight = True
        elif self.highlight:
            for monument in MapView.monument_list:
                monument.scale = self.normal_scale
            self.highlight = False

        # Restart bgm
        if self.bgm_stream == None:
            self.bgm_stream = Audio.play_sound(self.bgm, True)

        # MapView.update_monument_list()

    def on_mouse_press(self, x, y, button, modifiers):

        if C.DEBUG.ALL or C.DEBUG.MAP:
            print(x, y)
        hit_monument = arcade.check_for_collision_with_list(
            self.cursor_sprite, MapView.monument_list)
        if hit_monument:
            if hit_monument[0].unlocked:
                MapView.current_level = hit_monument[0].level

                # Play monument click sfx
                Audio.play_sound(hit_monument[0].sfx_click)

                # Stop bgm
                Audio.stop_sound(self.bgm_stream)
                self.bgm_stream = None

                game = gameview.GameView(self)
                game.setup()
                self.window.show_view(game)

        # Check if shops hit cursor (Simply because less number of checking)
        if self.shop_sprite.collides_with_sprite(self.cursor_sprite):
            self.window.show_view(shopview.ShopView())

# Make center points as dictionary and call out other views mostly

    def open_story(self):
        self.window.show_view(StoryView(self, MapView.current_level))

    def on_show(self):
        self.setup()

    @classmethod
    def update_monument_list(cls):
        for i, monument in enumerate(cls.monument_list):
            if GameData.level_data[str(i+1)]["passed"] == 0 and GameData.level_data[str(i+1)]["locked"] == 0:
                monument.color = (255, 255, 64)
                monument.unlocked = True
            elif GameData.level_data[str(i+1)]["passed"] == 0 and GameData.level_data[str(i+1)]["locked"] == 1:
                monument.color = (255, 64, 64)
                monument.unlocked = False
            else:
                monument.color = (255, 255, 255)
                monument.unlocked = True
