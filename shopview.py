import os

import arcade

import const.constants as C
import lib

from gamedata import GameData

# Base ShopView


class ShopView(arcade.View):
    def __init__(self, mapview):
        # Inherit parent class
        super().__init__()

        self.cursor_sprite = None
        self.preview = None
        self.preview_dir_name_list = os.listdir("assets/")

        self.map_view = mapview

        # GUI - Gold
        self.gold_sprite = arcade.Sprite(
            "resources/images/map/gold-bar.png", 0.6 * lib.global_scale())

        # Cursor
        self.cursor_sprite = arcade.Sprite(
            "resources/images/goat_cursor.png", 1)
        self.cursor_sprite.center_x = C.SCREEN_WIDTH * lib.global_scale()
        self.cursor_sprite.center_y = C.SCREEN_HEIGHT * lib.global_scale()

        self.max_lvl = 0

        # Weapon sprites
        pos_x = 200
        pos_y = 200
        self.weapon_sprite_list = []
        self.weapon_upgrade_sprite_list = []
        for weapon in C.WEAPON_LIST:
            path = f"resources/images/weapon/{weapon['img_name']}/{weapon['img_name']}.png"
            scale = weapon["scale"] * C.WEAPON_SCALE * lib.global_scale()
            position = (pos_x * lib.global_scale(), pos_y * lib.global_scale())
            self.weapon_sprite_list.append(arcade.Sprite(
                path, scale, center_x=position[0], center_y=position[1]))
            self.weapon_sprite_list[-1].base_scale = weapon["scale"]
            pos_y += 100

        self.normal_scale = 0.8 * lib.global_scale()
        self.highlight_scale = 1 * lib.global_scale()

        self.button = arcade.Sprite(
            filename="resources/images/pause_view/btn_back_to_map.png",
            scale=self.normal_scale)

        arcade.set_background_color(C.MENU_BACKGROUND_COLOR)

    def on_draw(self):

        # Clear the view with the background color
        self.clear()

        self.gold_sprite.position = (
            1200 * lib.global_scale(),
            680 * lib.global_scale()
        )
        self.gold_sprite.draw()

        lib.draw_text(
            GameData.gold,
            self.gold_sprite.position[0]*.99,
            self.gold_sprite.position[1]*1.005,
            30,
            anchor_x="left")

        # Set weapon upgrade sprites
        pos_x = 400
        pos_y = 200
        self.weapon_upgrade_sprite_list = []
        for index, weapon in enumerate(C.WEAPON_LIST, 0):
            self.weapon_upgrade_sprite_list.append([])
            for level in range(0, weapon["lvl_max"]):
                # Set max level
                if self.max_lvl < weapon["lvl_max"]:
                    self.max_lvl = weapon["lvl_max"]
                if GameData.loadout[weapon["name"]]["lvl"] - 1 < level:
                    path = "resources/images/shop/lvl_blank.png"
                else:
                    path = "resources/images/shop/lvl_bought.png"
                position = (pos_x * lib.global_scale(), pos_y * lib.global_scale())
                self.weapon_upgrade_sprite_list[index].append(arcade.Sprite(
                    path, lib.global_scale(), center_x=position[0], center_y=position[1]))
                self.weapon_upgrade_sprite_list[index][-1].name = weapon["name"]
                self.weapon_upgrade_sprite_list[index][-1].cost = weapon["lvl_cost"][level]
                self.weapon_upgrade_sprite_list[index][-1].lvl = level
                pos_x += 200
            pos_x = 400
            pos_y += 100

        # Draw level headers
        for i in range(1, self.max_lvl + 1):
            lib.draw_text(f"Level {i}", pos_x * lib.global_scale(), pos_y * lib.global_scale())
            pos_x += 200

        # Draw weapon sprites
        pos_x = 200
        pos_y = 200
        for sprite in self.weapon_sprite_list:
            sprite.scale = sprite.base_scale * C.WEAPON_SCALE * lib.global_scale()
            sprite.position = (pos_x * lib.global_scale(),
                               pos_y * lib.global_scale())
            sprite.draw()
            pos_y += 100

        # Draw weapon upgrade sprites
        for weapon in self.weapon_upgrade_sprite_list:
            for sprite in weapon:
                sprite.draw()
                lib.draw_text(sprite.cost, sprite.center_x, sprite.center_y)

        # Back to menu button
        self.button.center_x = C.SCREEN_WIDTH / 2 * lib.global_scale()
        self.button.center_y = C.SCREEN_HEIGHT - (50 * lib.global_scale())
        self.button.draw()

        # Cursor should always be top most/drawn last
        self.cursor_sprite.draw()

    def on_key_press(self, symbol: int, _modifiers: int):

        # ESCAPE | Back to map
        if symbol == arcade.key.ESCAPE:
            self.to_map()

    def on_mouse_press(self, _x, _y, _button, _modifiers):

        # Upgrade weapon
        for weapon in self.weapon_upgrade_sprite_list:
            for sprite in weapon:
                if sprite.collides_with_sprite(self.cursor_sprite):
                    print(sprite.name, sprite.lvl, sprite.cost,
                          GameData.loadout[sprite.name]["lvl"])
                    if sprite.lvl == GameData.loadout[sprite.name]["lvl"] \
                            and sprite.cost <= GameData.gold:
                        GameData.update_gold(GameData.gold - sprite.cost)
                        GameData.update_loadout(sprite.name, sprite.lvl + 1)
                        break

        # Back to map
        hit_list = arcade.check_for_collision(
            self.cursor_sprite, self.button)
        if hit_list:
            self.to_map()

    def to_map(self):
        """ Select map view """

        # Audio.stop_sound(self.bgm_stream)
        # self.bgm_stream = None
        self.window.show_view(self.map_view)

    def on_mouse_motion(self, x, y, _dx, _dy):

        # Cursor follows mouse
        self.cursor_sprite.center_x = x + C.GUI["Crosshair"]["offset_x"]
        self.cursor_sprite.center_y = y + C.GUI["Crosshair"]["offset_y"]

        # Animate back to map button
        hit_list = arcade.check_for_collision(
            self.cursor_sprite, self.button)
        if hit_list:
            self.button.scale = self.highlight_scale
        else:
            self.button.scale = self.normal_scale
