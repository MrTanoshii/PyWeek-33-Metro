import arcade
from constants import BG_SCALING, SPEED_SCROLLING, SCREEN_HEIGHT


class BackGround(arcade.Sprite):
    """ Background Sprite """

    bg_list = arcade.SpriteList()

    def __init__(self, current_level, speed=SPEED_SCROLLING):
        # Inherit parent class
        super().__init__()

        self.speed = speed
        # Set our scale
        self.scale = BG_SCALING

        # load player texture
        self.idle_texture = arcade.load_texture(
            f"resources/images/levels/{str(current_level)}/bg.png")

        # Set the initial texture
        self.texture = self.idle_texture

    @classmethod
    def update(cls, delta_time: float = 1 / 60):
        for bg in cls.bg_list:
            bg.center_x += bg.speed
            if bg.center_x - bg.width / 2 < -880 / 720 * SCREEN_HEIGHT - bg.speed:
                bg.center_x = bg.width/2
        return super().on_update(delta_time)
