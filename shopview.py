import arcade
import const.constants as C
import os
from lib import global_scale

# Base ShopView


class ShopView(arcade.View):
    def __init__(self):
        # Inherit parent class
        super().__init__()

        self.cursor_sprite = None
        self.preview = None
        self.preview_dir_name_list = os.listdir("assets/")

        # Left button
        self.btn_left = arcade.Sprite(
            "resources/images/shop/shop_left.png", 0.2)
        self.btn_left.center_x = 100 * global_scale()
        self.btn_left.center_y = 350 * global_scale()

        # Right button
        self.btn_right = arcade.Sprite(
            "resources/images/shop/shop_right.png", 0.2)
        self.btn_right.center_x = 1200 * global_scale()
        self.btn_right.center_y = 350 * global_scale()

        # Cursor
        self.cursor_sprite = arcade.Sprite(
            "resources/images/goat_cursor.png", 1)
        self.cursor_sprite.center_x = C.SCREEN_WIDTH * global_scale()
        self.cursor_sprite.center_y = C.SCREEN_HEIGHT * global_scale()

        self.current_preview_index = 0
        self.preview = PreviewSprite(
            self.preview_dir_name_list[self.current_preview_index])

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # arcade.draw_lrwh_rectangle_textured(0, 0,
        #                                     C.SCREEN_WIDTH, C.SCREEN_HEIGHT,
        #                                     self.background)

        self.preview.draw()

        # TODO: Asset should not be pixelated ingame
        self.btn_left.draw(pixelated=True)
        self.btn_right.draw(pixelated=True)

        # Cursor should always be top most
        self.cursor_sprite.draw()

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(C.MENU_BACKGROUND_COLOR)

    def on_mouse_press(self, x, y, button, modifiers):

        # Go to previous or next preview index
        if self.btn_left.collides_with_sprite(self.cursor_sprite):
            self.current_preview_index -= 1
            if self.current_preview_index < 0:
                self.current_preview_index = len(
                    self.preview_dir_name_list) - 1
        elif self.btn_right.collides_with_sprite(self.cursor_sprite):
            self.current_preview_index += 1
            if self.current_preview_index >= len(self.preview_dir_name_list):
                self.current_preview_index = 0

        # Display preview
        self.preview = PreviewSprite(
            self.preview_dir_name_list[self.current_preview_index])

    def on_mouse_motion(self, x, y, _dx, _dy):
        self.cursor_sprite.center_x = x + C.GUI["Crosshair"]["offset_x"]
        self.cursor_sprite.center_y = y + C.GUI["Crosshair"]["offset_y"]

    def on_update(self, delta_time=1 / 60):
        self.preview.update_animation(delta_time)


class PreviewSprite(arcade.Sprite):

    def __init__(self, dir):
        super().__init__()

        self.center_x = 650 * global_scale()
        self.center_y = 400 * global_scale()
        self.scale = 1 * global_scale()
        self.cur_texture = 0

        base_path = f"assets/{dir}/"

        self.texture_list = []
        for filename in os.listdir(f"{base_path}"):
            self.texture_list.append(
                arcade.load_texture(f"{base_path}{filename}"))

        self.texture = self.texture_list[int(self.cur_texture)]

    def on_key_press(self, key, _modifiers):
        """Handle keyboard key press"""
        if key == arcade.key.ESCAPE:
            arcade.exit()

    def update_animation(self, delta_time=1 / 60):
        texture_speed = 30

        if len(self.texture_list) > 1:
            self.cur_texture += texture_speed * delta_time
            while self.cur_texture >= len(self.texture_list) - 1:
                self.cur_texture -= len(self.texture_list) - 1
                if (self.cur_texture <= 0):
                    self.cur_texture = 0
                    break
        self.texture = self.texture_list[int(self.cur_texture)]

    def on_key_press(self, key, _modifiers):
        """Handle keyboard key press"""
        if key == arcade.key.ESCAPE:
            arcade.exit()
