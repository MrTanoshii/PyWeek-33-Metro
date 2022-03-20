import arcade
from constants import BG_SCALING


class BackGround(arcade.Sprite):
    """ Player Sprite """
    def __init__(self, speed=-10, asset="bg-1.png", size=1):
        # Let parent initialize
        super().__init__()

        self.SPEED = speed

        # Set our scale
        self.scale = size or BG_SCALING

        # load player texture
        base_path = "resources/"
        self.asset = asset
        self.idle_texture_pair = arcade.load_texture_pair(f"{base_path}images/{asset}")

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]
