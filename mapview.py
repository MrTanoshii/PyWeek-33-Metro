
import constants as C
import gameview
import arcade
from player import Player


class MapView(arcade.View):
    """ Class Managing the Map View"""

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.cursor_sprite = None
        self.cursor_list = None

        self.background = None

        self.monument_list = None

        self.level = 0
        self.normal_scale = .2
        self.highlight_scale = .5
        self.highlight = False

    def setup(self):
        """ Set up everything with the game """

        # self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.monument_list = arcade.SpriteList()
        self.cursor_list = arcade.SpriteList()
        # Create the sprite lists
        self.background = arcade.load_texture(
            "resources/images/map/pixel_map.png")
        self.cursor_sprite = arcade.Sprite(
            "resources/images/goat_cursor.png", 0.05)

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
            self.monument_list.append(monument)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            C.SCREEN_WIDTH, C.SCREEN_HEIGHT,
                                            self.background)
        self.monument_list.draw()
        self.cursor_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_sprite.center_x = x+20
        self.cursor_sprite.center_y = y-20

    def on_update(self, delta_time):

        hit_list = arcade.check_for_collision_with_list(
            self.cursor_sprite, self.monument_list)

        if len(hit_list):
            for i, monument in enumerate(self.monument_list):
                if i != self.monument_list.index(hit_list[0]):
                    monument.scale = self.normal_scale
                else:
                    monument.scale = self.highlight_scale
                    self.highlight = True
        elif self.highlight:
            for monument in self.monument_list:
                monument.scale = self.normal_scale
            self.highlight = False

    def on_mouse_press(self, x, y, button, modifiers):

        if C.DEBUG:
            print(x, y)
        target = arcade.check_for_collision_with_list(self.cursor_sprite, self.monument_list)
        Player.current_level = target[0].level
        game = gameview.GameView()
        game.setup()
        self.window.show_view(game)

# Make center points as dictionary and call out other views mostly

    def on_show(self):
        self.setup()
