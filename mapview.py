import constants as C
import gameview
import arcade


class MapView(arcade.View):
    """ Class Managing the Map View"""

    # def on_show(self):
    #     self.background = "resources/images/map.png"

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.cursor_sprite = None
        self.player_list = None

        self.background = None

        self.monument_list = None

        # arcade.set_background_color((170,218,255))

    def setup(self):
        """ Set up everything with the game """

        # self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.monument_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        # Create the sprite lists
        self.background = arcade.load_texture(
            "resources/images/pixel_map.png")
        self.cursor_sprite = arcade.Sprite(
            "resources/images/goat_cursor.png", 0.05)

        self.player_list.append(self.cursor_sprite)
        self.load_monuments()

    def load_monuments(self):
        """Loads map monuments onto map"""
        for mon_dict in C.MAP_MONUMENTS_LIST:
            monument = arcade.Sprite(
                "resources/images/" + mon_dict["img_name"],
                mon_dict["scale"])
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
        self.player_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for monument in self.monument_list:
            monument.scale = 0.5
        self.cursor_sprite.center_x = x+20
        self.cursor_sprite.center_y = y-20

    def on_update(self, delta_time):

        hit_list = arcade.check_for_collision_with_list(
            self.cursor_sprite, self.monument_list)

        for i in hit_list:
            i.scale = 0.7

        # self.monument_sprite.clear()

    def on_mouse_press(self, x, y, button, modifiers):
        p = self.cursor_sprite.collides_with_list(self.monument_list)
        for location in p:
            self.window.show_view(gameview.GameView())


# Make center points as dictionary and call out other views mostly


    def on_show(self):
        self.setup()
