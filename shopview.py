import arcade
import const.constants as C
from lib import global_scale
import os

# Base ShopView


class ShopView(arcade.View):
    def __init__(self):
        # Inherit parent class
        super().__init__()

        self.cursor_sprite = None
        self.Player1 = None
        self.list1 = os.listdir("assets/")

    def setup(self):
        """ Set up everything with the game """
        # Create the sprite lists
        self.move_spritel = arcade.Sprite(
            "resources/images/shop/shop_left.png", 0.2)
        self.move_spriter = arcade.Sprite(
            "resources/images/shop/shop_right.png", 0.2)
        self.move_spritel.center_x = 100
        self.move_spritel.center_y = 350
        self.move_spriter.center_x = 1200
        self.move_spriter.center_y = 350
        self.cursor_sprite = arcade.Sprite(
            "resources/images/goat_cursor.png", 1)
        self.c_p = 0
        self.Player1 = PreviewSprite(self.list1[self.c_p])

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # arcade.draw_lrwh_rectangle_textured(0, 0,
        #                                     C.SCREEN_WIDTH, C.SCREEN_HEIGHT,
        #                                     self.background)

        self.move_spritel.draw(pixelated=True)
        self.move_spriter.draw(pixelated=True)
        self.cursor_sprite.draw()
        self.Player1.draw()

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(C.MENU_BACKGROUND_COLOR)
        self.setup()

    def on_mouse_press(self, x, y, button, modifiers):

        if self.move_spritel.collides_with_sprite(self.cursor_sprite):
            self.c_p = (self.c_p + 1)
            if self.c_p > len(self.list1):
                self.c_p = 0
            self.Player1 = PreviewSprite(self.list1[self.c_p])

        if self.move_spriter.collides_with_sprite(self.cursor_sprite):
            self.c_p = (self.c_p - 1)
            if self.c_p < 0:
                self.c_p = len(self.list1)-1
            self.Player1 = PreviewSprite(self.list1[self.c_p])

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor_sprite.center_x = x+20
        self.cursor_sprite.center_y = y-20

    def on_update(self, delta_time=1/60):
        self.Player1.update_animation(delta_time)


class PreviewSprite(arcade.Sprite):

    def __init__(self, dir):
        super().__init__()

        self.center_x = 650
        self.center_y = 400
        self.scale = 1
        self.cur_texture = 0

        base_path = f"assets/{dir}/"

        self.texture_list = []
        for filename in os.listdir(f"{base_path}"):
            self.texture_list.append(
                arcade.load_texture(f"{base_path}{filename}"))

        self.texture = self.texture_list[int(self.cur_texture)]

    def update_animation(self, delta_time=1/60):
        self.cur_texture += 0.1
        if self.cur_texture > len(self.texture_list) - 1:
            self.cur_texture = 0
        self.texture = self.texture_list[int(self.cur_texture)]
