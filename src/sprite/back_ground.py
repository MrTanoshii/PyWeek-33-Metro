import arcade

import src.const as C

from src.lib import global_scale


class BackGround(arcade.Sprite):
    """
    Background Sprite

    ...

    Attributes
    ----------
    bg_list : arcade.SpriteList()
        List of all backGround sprites

    Class Methods
    -------------
    update(delta_time: float = 1 / 60)
        Update the background
    """

    # SpriteList class attribute
    bg_list = arcade.SpriteList()

    def __init__(self, current_level, speed=C.SPEED_SCROLLING, scale=C.BG_SCALE):
        # Inherit parent class
        super().__init__()

        self.speed = speed
        # Set our scale
        self.scale = scale * global_scale()

        # load player texture
        self.idle_texture = arcade.load_texture(
            f"src/resources/images/levels/{str(current_level)}/bg.png")

        # Set the initial texture
        self.texture = self.idle_texture

    @classmethod
    def update(cls, delta_time: float = 1 / 60):
        for bg in cls.bg_list:
            bg.center_x += bg.speed * global_scale()
            if bg.center_x - (bg.width / 2) < (-880 - bg.speed) * global_scale():
                bg.center_x = bg.width/2
        return super().on_update(delta_time)
