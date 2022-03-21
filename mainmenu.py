import arcade
import mapview
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MENU_FONT_SIZE, MENU_BACKGROUND_COLOR

CENTER_POINTS = [[700, 450], [900, 450]]


class MainMenu(arcade.View):
    """Class that manages the 'menu' view."""

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(MENU_BACKGROUND_COLOR)

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        arcade.draw_text(
            "Main Menu - Click to play",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=MENU_FONT_SIZE,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        self.window.show_view(mapview.MapView())


###Egypt - Pyramid
# China
# Moscow
# Brazil
# London
# Africa
# ##USA
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

        # self.set_mouse_visible(False)

    def setup(self):
        """ Set up everything with the game """

        # self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        self.monument_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        # Create the sprite lists
        self.background = arcade.load_texture(
            "resources/images/earthmap1k.jpg")

        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_person/femalePerson_idle.png", 0.5)

        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        # First sprite
        self.monument_sprite = arcade.Sprite(
            "resources/images/pyramids.jpeg", 0.5)
        self.monument_sprite.center_x = 700
        self.monument_sprite.center_y = 450
        self.monument_list.append(self.monument_sprite)

        self.monument_sprite = arcade.Sprite(
            "resources/images/taj_mahal.jpeg", 0.5)
        self.monument_sprite.center_x = 900
        self.monument_sprite.center_y = 450
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
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        self.monument_sprite.update()

        hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.monument_list)

        for i in hit_list:
            i.scale = 0.7

        # self.monument_sprite.clear()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.player_sprite.collides_with_list(self.monument_list):
            p = self.player_sprite.collides_with_list(self.monument_list)
            for i in CENTER_POINTS:
                if [p[0].center_x, p[0].center_y] == i:
                    print(p[0].collision_radius, p[0].center_x, p[0].center_y)
                    game_view = GameView()
                    self.window.show_view(GameView())

# Make center points as dictionary and call out other views mostly

    def on_show(self):
        self.setup()
