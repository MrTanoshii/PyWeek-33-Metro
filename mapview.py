import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CENTER_POINTS
import gameview


class MapView(arcade.View):
    """ Class Managing the Map View"""

    # def on_show(self):
    #     self.background = "resources/images/map.png"

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__()

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.player_sprite = None
        self.player_list = None

        self.background = None

        self.monument_list = None
        self.monument_sprite = None

        # arcade.set_background_color((170,218,255))

        # self.set_mouse_visible(False)

    def setup(self):
        """ Set up everything with the game """

        # self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.monument_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        # Create the sprite lists
        self.background = arcade.load_texture(
            "resources/images/pixel_map.png")

        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png", 0.5)

        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        # First sprite
        self.monument_sprite = arcade.Sprite(
            "resources/images/pyramids.jpeg", 0.5)
        self.monument_sprite.center_x = CENTER_POINTS[0][0]
        self.monument_sprite.center_y = CENTER_POINTS[0][1]
        self.monument_sprite.name = "EGYPT"
        self.monument_list.append(self.monument_sprite)

        self.monument_sprite = arcade.Sprite(
            "resources/images/taj_mahal.jpeg", 0.5)
        self.monument_sprite.center_x = CENTER_POINTS[1][0]
        self.monument_sprite.center_y = CENTER_POINTS[1][1]
        self.monument_sprite.name = "INDIA"
        self.monument_list.append(self.monument_sprite)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        self.monument_list.draw()
        self.player_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for monument in self.monument_list:
            monument.scale = 0.5
        self.player_sprite.center_x = x+20
        self.player_sprite.center_y = y-20

    def on_update(self, delta_time):
        self.monument_sprite.update()

        hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.monument_list)

        for i in hit_list:
            i.scale = 0.7

        # self.monument_sprite.clear()

    def on_mouse_press(self, x, y, button, modifiers):
        p = self.player_sprite.collides_with_list(self.monument_list)
        for location in p:
            if location.name == "EGYPT":
                self.window.show_view(gameview.GameView())
            elif location.name == "INDIA":
                self.window.show_view(gameview.GameView())

# Make center points as dictionary and call out other views mostly

    def on_show(self):
        self.setup()
