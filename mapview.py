import constants as C
import gameview
import arcade
from player import Player
from audio import Audio
from gamedata import GameData


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
        self.normal_scale = .2
        self.highlight_scale = .5
        self.highlight = False

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
        self.bgm_stream = Audio.play_sound(self.bgm)

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

        self.cursor_list.append(self.cursor_sprite)
        self.load_monuments()

    def load_monuments(self):
        """Loads map monuments onto map"""
        for mon_dict in C.MAP_MONUMENTS_LIST:
            monument = arcade.Sprite(
                "resources/images/map/" + mon_dict["img_name"],
                self.normal_scale)
            monument.level = mon_dict["level"]
            monument.center_x = mon_dict["center_x"]
            monument.center_y = mon_dict["center_y"]
      
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
                                            C.SCREEN_WIDTH, C.SCREEN_HEIGHT,
                                            self.background)
        # GUI - Gold
        arcade.draw_text(
            f"Gold : {GameData.gold}",
            C.SCREEN_WIDTH / 5,
            C.SCREEN_HEIGHT - 150,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

        MapView.monument_list.draw()
        self.cursor_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_sprite.center_x = x+20
        self.cursor_sprite.center_y = y-20

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

            game = gameview.GameView()
            game.setup()
            self.window.show_view(game)

# Make center points as dictionary and call out other views mostly

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
