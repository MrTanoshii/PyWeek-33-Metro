import arcade
import random
from constants import BG_SCALING, SPEED_SCROLLING, LEVEL1, SCREEN_WIDTH, SCREEN_HEIGHT


class BackGround(arcade.Sprite):
    """ Player Sprite """

    bg_list = arcade.SpriteList()

    def __init__(self, speed=SPEED_SCROLLING, asset="bg-1.png", size=1):
        # Let parent initialize
        super().__init__()

        self.speed = speed

        # Set our scale
        self.scale = size or BG_SCALING

        # load player texture
        base_path = "resources/"
        self.asset = asset
        self.idle_texture = arcade.load_texture(f"{base_path}images/{asset}")

        # Set the initial texture
        self.texture = self.idle_texture

    @classmethod
    def spawn(cls):
        """ Create BG sprite"""
        assets = LEVEL1.assets
        bg = cls(asset=random.choice(
            assets), size=random.uniform(.9, 1.1))
        bg.center_x = SCREEN_WIDTH + bg.width / 2
        if random.randint(0, 1) == 1:
            bg.center_y = SCREEN_HEIGHT + \
                bg.height / 2 - random.uniform(50, 75)
        else:
            bg.center_y = bg.height / 2 + random.uniform(-50, 50)
        cls.bg_list.append(bg)

    @classmethod
    def update(cls, delta_time: float = 1 / 60):
        for bg in cls.bg_list:
            bg.center_x += bg.speed
            if bg.asset == "bg-1.png":
                if bg.center_x - bg.width / 2 < - 220 - bg.speed:
                    bg.center_x = bg.width/2
            else:
                if bg.center_x + bg.width < 0:
                    bg.remove_from_sprite_lists()
        return super().on_update(delta_time)
