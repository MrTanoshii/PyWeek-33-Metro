import arcade
import random
from constants import BG_SCALING, SPEED_SCROLLING, LEVEL1, SCREEN_WIDTH, SCREEN_HEIGHT


class BackGround(arcade.Sprite):
    """ Player Sprite """

    bg_list = arcade.SpriteList()

    current_level_ = None

    def __init__(self, current_level, speed=SPEED_SCROLLING):
        # Let parent initialize
        super().__init__()

        self.speed = speed
        # Set our scale
        self.scale = BG_SCALING

        # load player texture
        self.idle_texture = arcade.load_texture(f"resources/images/levels/{current_level}/bg.png")

        # Set the initial texture
        self.texture = self.idle_texture

    @classmethod
    def update(cls, delta_time: float = 1 / 60):
        for bg in cls.bg_list:
            bg.center_x += bg.speed
            if bg.center_x - bg.width / 2 < -880 - bg.speed:
                bg.center_x = bg.width/2
        return super().on_update(delta_time)
