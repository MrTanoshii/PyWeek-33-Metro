import arcade
import const.constants as C
import os
from lib import global_scale
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
            "resources/images/map/gold-bar.png", 0.6 * global_scale())
        self.gold_sprite.position = (
            1200 * global_scale(), 680 * global_scale())

        # Cursor
        self.cursor_sprite = arcade.Sprite(
            "resources/images/goat_cursor.png", 1)
        self.cursor_sprite.center_x = C.SCREEN_WIDTH * global_scale()
        self.cursor_sprite.center_y = C.SCREEN_HEIGHT * global_scale()

        self.revolver_sprite = arcade.Sprite(
            "resources/images/weapon/weapon_revolver/weapon_revolver.png", C.WEAPON_LIST[0]["scale"] * C.WEAPON_SCALE * global_scale())
        self.revolver_sprite.center_x = 200
        self.revolver_sprite.center_y = 200
        self.rifle_sprite = arcade.Sprite(
            "resources/images/weapon/weapon_ak/weapon_ak.png", C.WEAPON_LIST[1]["scale"] * C.WEAPON_SCALE * global_scale())
        self.rifle_sprite.center_x = 200
        self.rifle_sprite.center_y = 300
        self.shotgun_sprite = arcade.Sprite(
            "resources/images/weapon/weapon_shotgun/weapon_shotgun.png", C.WEAPON_LIST[2]["scale"] * C.WEAPON_SCALE * global_scale())
        self.shotgun_sprite.center_x = 200
        self.shotgun_sprite.center_y = 400
        self.rpg_sprite = arcade.Sprite(
            "resources/images/weapon/weapon_rpg/weapon_rpg.png", C.WEAPON_LIST[3]["scale"] * C.WEAPON_SCALE * global_scale())
        self.rpg_sprite.center_x = 200
        self.rpg_sprite.center_y = 500

        self.revolver_lvl_1 = arcade.Sprite()
        self.revolver_lvl_2 = arcade.Sprite()
        self.revolver_lvl_3 = arcade.Sprite()

        self.rifle_lvl_1 = arcade.Sprite()
        self.rifle_lvl_2 = arcade.Sprite()
        self.rifle_lvl_3 = arcade.Sprite()

        self.shotgun_lvl_1 = arcade.Sprite()
        self.shotgun_lvl_2 = arcade.Sprite()
        self.shotgun_lvl_3 = arcade.Sprite()

        self.rpg_lvl_1 = arcade.Sprite()
        self.rpg_lvl_2 = arcade.Sprite()
        self.rpg_lvl_3 = arcade.Sprite()

        self.normal_scale = 0.8 * global_scale()
        self.highlight_scale = 1 * global_scale()

        self.button = arcade.Sprite(
            filename="resources/images/pause_view/btn_back_to_map.png",
            scale=self.normal_scale * global_scale())
        self.button.center_x = C.SCREEN_WIDTH // 2
        self.button.center_y = C.SCREEN_HEIGHT - 50

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # arcade.draw_lrwh_rectangle_textured(0, 0,
        #                                     C.SCREEN_WIDTH, C.SCREEN_HEIGHT,
        #                                     self.background)

        # self.preview.draw()

        # TODO: Asset should not be pixelated ingame
        # self.btn_left.draw(pixelated=True)
        # self.btn_right.draw(pixelated=True)

        self.gold_sprite.draw()
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

        # Revolver
        self.revolver_lvl_1 = None
        if GameData.loadout["Revolver"]["lvl"] < 1:
            self.revolver_lvl_1 = arcade.Sprite(
                "resources/images/shop/lvl_blank.png")
        else:
            self.revolver_lvl_1 = arcade.Sprite(
                "resources/images/shop/lvl_bought.png")
        self.revolver_lvl_1.center_x = 400
        self.revolver_lvl_1.center_y = 200

        self.revolver_lvl_2 = None
        if GameData.loadout["Revolver"]["lvl"] < 2:
            self.revolver_lvl_2 = arcade.Sprite(
                "resources/images/shop/lvl_blank.png")
        else:
            self.revolver_lvl_2 = arcade.Sprite(
                "resources/images/shop/lvl_bought.png")
        self.revolver_lvl_2.center_x = 600
        self.revolver_lvl_2.center_y = 200

        self.revolver_lvl_3 = None
        if GameData.loadout["Revolver"]["lvl"] < 3:
            self.revolver_lvl_3 = arcade.Sprite(
                "resources/images/shop/lvl_blank.png")
        else:
            self.revolver_lvl_3 = arcade.Sprite(
                "resources/images/shop/lvl_bought.png")
        self.revolver_lvl_3.center_x = 800
        self.revolver_lvl_3.center_y = 200

        # Rifle
        self.rifle_lvl_1 = None
        if GameData.loadout["Rifle"]["lvl"] < 1:
            self.rifle_lvl_1 = arcade.Sprite(
                "resources/images/shop/lvl_blank.png")
        else:
            self.rifle_lvl_1 = arcade.Sprite(
                "resources/images/shop/lvl_bought.png")
        self.rifle_lvl_1.center_x = 400
        self.rifle_lvl_1.center_y = 300

        self.rifle_lvl_2 = None
        if GameData.loadout["Rifle"]["lvl"] < 2:
            self.rifle_lvl_2 = arcade.Sprite(
                "resources/images/shop/lvl_blank.png")
        else:
            self.rifle_lvl_2 = arcade.Sprite(
                "resources/images/shop/lvl_bought.png")
        self.rifle_lvl_2.center_x = 600
        self.rifle_lvl_2.center_y = 300

        self.rifle_lvl_3 = None
        if GameData.loadout["Rifle"]["lvl"] < 3:
            self.rifle_lvl_3 = arcade.Sprite(
                "resources/images/shop/lvl_blank.png")
        else:
            self.rifle_lvl_3 = arcade.Sprite(
                "resources/images/shop/lvl_bought.png")
        self.rifle_lvl_3.center_x = 800
        self.rifle_lvl_3.center_y = 300

        # Shotgun
        self.shotgun_lvl_1 = None
        if GameData.loadout["Shotgun"]["lvl"] < 1:
            self.shotgun_lvl_1 = arcade.Sprite(
                "resources/images/shop/lvl_blank.png")
        else:
            self.shotgun_lvl_1 = arcade.Sprite(
                "resources/images/shop/lvl_bought.png")
        self.shotgun_lvl_1.center_x = 400
        self.shotgun_lvl_1.center_y = 400

        self.shotgun_lvl_2 = None
        if GameData.loadout["Shotgun"]["lvl"] < 2:
            self.shotgun_lvl_2 = arcade.Sprite(
                "resources/images/shop/lvl_blank.png")
        else:
            self.shotgun_lvl_2 = arcade.Sprite(
                "resources/images/shop/lvl_bought.png")
        self.shotgun_lvl_2.center_x = 600
        self.shotgun_lvl_2.center_y = 400

        self.shotgun_lvl_3 = None
        if GameData.loadout["Shotgun"]["lvl"] < 3:
            self.shotgun_lvl_3 = arcade.Sprite(
                "resources/images/shop/lvl_blank.png")
        else:
            self.shotgun_lvl_3 = arcade.Sprite(
                "resources/images/shop/lvl_bought.png")
        self.shotgun_lvl_3.center_x = 800
        self.shotgun_lvl_3.center_y = 400

        # RPG
        self.rpg_lvl_1 = None
        if GameData.loadout["RPG"]["lvl"] < 1:
            self.rpg_lvl_1 = arcade.Sprite(
                "resources/images/shop/lvl_blank.png")
        else:
            self.rpg_lvl_1 = arcade.Sprite(
                "resources/images/shop/lvl_bought.png")
        self.rpg_lvl_1.center_x = 400
        self.rpg_lvl_1.center_y = 500

        self.rpg_lvl_2 = None
        if GameData.loadout["RPG"]["lvl"] < 2:
            self.rpg_lvl_2 = arcade.Sprite(
                "resources/images/shop/lvl_blank.png")
        else:
            self.rpg_lvl_2 = arcade.Sprite(
                "resources/images/shop/lvl_bought.png")
        self.rpg_lvl_2.center_x = 600
        self.rpg_lvl_2.center_y = 500

        self.rpg_lvl_3 = None
        if GameData.loadout["RPG"]["lvl"] < 3:
            self.rpg_lvl_3 = arcade.Sprite(
                "resources/images/shop/lvl_blank.png")
        else:
            self.rpg_lvl_3 = arcade.Sprite(
                "resources/images/shop/lvl_bought.png")
        self.rpg_lvl_3.center_x = 800
        self.rpg_lvl_3.center_y = 500

        self.revolver_lvl_1.cost = 0
        self.revolver_lvl_2.cost = 50
        self.revolver_lvl_3.cost = 100

        self.rifle_lvl_1.cost = 75
        self.rifle_lvl_2.cost = 125
        self.rifle_lvl_3.cost = 200

        self.shotgun_lvl_1.cost = 100
        self.shotgun_lvl_2.cost = 150
        self.shotgun_lvl_3.cost = 225

        self.rpg_lvl_1.cost = 125
        self.rpg_lvl_2.cost = 175
        self.rpg_lvl_3.cost = 250

        self.revolver_sprite.draw()
        self.revolver_lvl_1.draw()
        self.revolver_lvl_2.draw()
        self.revolver_lvl_3.draw()
        self.rifle_sprite.draw()
        self.rifle_lvl_1.draw()
        self.rifle_lvl_2.draw()
        self.rifle_lvl_3.draw()
        self.shotgun_sprite.draw()
        self.shotgun_lvl_1.draw()
        self.shotgun_lvl_2.draw()
        self.shotgun_lvl_3.draw()
        self.rpg_sprite.draw()
        self.rpg_lvl_1.draw()
        self.rpg_lvl_2.draw()
        self.rpg_lvl_3.draw()

        self.draw_text("Level 1", 400, 600)
        self.draw_text("Level 2", 600, 600)
        self.draw_text("Level 3", 800, 600)

        self.draw_text(self.revolver_lvl_1.cost, 400, 200)
        self.draw_text(self.revolver_lvl_2.cost, 600, 200)
        self.draw_text(self.revolver_lvl_3.cost, 800, 200)

        self.draw_text(self.rifle_lvl_1.cost, 400, 300)
        self.draw_text(self.rifle_lvl_2.cost, 600, 300)
        self.draw_text(self.rifle_lvl_3.cost, 800, 300)

        self.draw_text(self.shotgun_lvl_1.cost, 400, 400)
        self.draw_text(self.shotgun_lvl_2.cost, 600, 400)
        self.draw_text(self.shotgun_lvl_3.cost, 800, 400)

        self.draw_text(self.rpg_lvl_1.cost, 400, 500)
        self.draw_text(self.rpg_lvl_2.cost, 600, 500)
        self.draw_text(self.rpg_lvl_3.cost, 800, 500)

        self.draw_text("WORKS", 400, 150)
        self.draw_text("NOT WORKING", 600, 150)
        self.draw_text("NOT WORKING", 800, 150)

        self.button.draw()

        # Cursor should always be top most
        self.cursor_sprite.draw()

    def draw_text(self, text, x, y):
        arcade.draw_text(
            text,
            x,
            y,
            arcade.color.BLACK,
            font_name="Kenney High",
            bold=True,
            font_size=30 * global_scale(),
            anchor_x="center",
            anchor_y="center",
        )

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(C.MENU_BACKGROUND_COLOR)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.revolver_lvl_1.collides_with_sprite(self.cursor_sprite):
            if GameData.loadout["Revolver"]["lvl"] == 0 and GameData.gold:
                GameData.update_gold(GameData.gold - self.revolver_lvl_1.cost)
                GameData.update_loadout("Revolver", 1)
        elif self.revolver_lvl_2.collides_with_sprite(self.cursor_sprite):
            if GameData.loadout["Revolver"]["lvl"] == 1 and GameData.gold:
                GameData.update_gold(GameData.gold - self.revolver_lvl_2.cost)
                GameData.update_loadout("Revolver", 2)
        elif self.revolver_lvl_3.collides_with_sprite(self.cursor_sprite):
            if GameData.loadout["Revolver"]["lvl"] == 2 and GameData.gold:
                GameData.update_gold(GameData.gold - self.revolver_lvl_3.cost)
                GameData.update_loadout("Revolver", 3)

        elif self.rifle_lvl_1.collides_with_sprite(self.cursor_sprite):
            if GameData.loadout["Rifle"]["lvl"] == 0 and GameData.gold:
                GameData.update_gold(GameData.gold - self.rifle_lvl_1.cost)
                GameData.update_loadout("Rifle", 1)
        elif self.rifle_lvl_2.collides_with_sprite(self.cursor_sprite):
            if GameData.loadout["Rifle"]["lvl"] == 1 and GameData.gold:
                GameData.update_gold(GameData.gold - self.rifle_lvl_2.cost)
                GameData.update_loadout("Rifle", 2)
        elif self.rifle_lvl_3.collides_with_sprite(self.cursor_sprite):
            if GameData.loadout["Rifle"]["lvl"] == 2 and GameData.gold:
                GameData.update_gold(GameData.gold - self.rifle_lvl_3.cost)
                GameData.update_loadout("Rifle", 3)

        elif self.shotgun_lvl_1.collides_with_sprite(self.cursor_sprite):
            if GameData.loadout["Shotgun"]["lvl"] == 0 and GameData.gold:
                GameData.update_gold(GameData.gold - self.shotgun_lvl_1.cost)
                GameData.update_loadout("Shotgun", 1)
        elif self.shotgun_lvl_2.collides_with_sprite(self.cursor_sprite):
            if GameData.loadout["Shotgun"]["lvl"] == 1 and GameData.gold:
                GameData.update_gold(GameData.gold - self.shotgun_lvl_2.cost)
                GameData.update_loadout("Shotgun", 2)
        elif self.shotgun_lvl_3.collides_with_sprite(self.cursor_sprite):
            if GameData.loadout["Shotgun"]["lvl"] == 2 and GameData.gold:
                GameData.update_gold(GameData.gold - self.shotgun_lvl_3.cost)
                GameData.update_loadout("Shotgun", 3)

        elif self.rpg_lvl_1.collides_with_sprite(self.cursor_sprite):
            if GameData.loadout["RPG"]["lvl"] == 0 and GameData.gold:
                GameData.update_gold(GameData.gold - self.rpg_lvl_1.cost)
                GameData.update_loadout("RPG", 1)
        elif self.rpg_lvl_2.collides_with_sprite(self.cursor_sprite):
            if GameData.loadout["RPG"]["lvl"] == 1 and GameData.gold:
                GameData.update_gold(GameData.gold - self.rpg_lvl_2.cost)
                GameData.update_loadout("RPG", 2)
        elif self.rpg_lvl_3.collides_with_sprite(self.cursor_sprite):
            if GameData.loadout["RPG"]["lvl"] == 2 and GameData.gold:
                GameData.update_gold(GameData.gold - self.rpg_lvl_3.cost)
                GameData.update_loadout("RPG", 3)

        hit_list = arcade.check_for_collision(
            self.cursor_sprite, self.button)

        if hit_list:
            self.to_map()

    def to_map(self):
        # Audio.stop_sound(self.bgm_stream)
        # self.bgm_stream = None
        self.window.show_view(self.map_view)

    def on_mouse_motion(self, x, y, _dx, _dy):
        self.cursor_sprite.center_x = x + C.GUI["Crosshair"]["offset_x"]
        self.cursor_sprite.center_y = y + C.GUI["Crosshair"]["offset_y"]

        hit_list = arcade.check_for_collision(
            self.cursor_sprite, self.button)

        if hit_list:
            self.button.scale = self.highlight_scale
        else:
            self.button.scale = self.normal_scale

    def on_update(self, delta_time=1 / 60):
        pass
