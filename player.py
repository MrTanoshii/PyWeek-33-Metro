import arcade
from constants import CHARACTER_SCALING


class Player(arcade.Sprite):
    """ Player Sprite """
    def __init__(self, hit_box_algorithm):
        self.current_speed = 0
        self.SPEED = 2
        # Let parent initialize
        super().__init__()

        # Set our scale
        self.scale = CHARACTER_SCALING

        # load player texture
        base_path = "resources/images/"
        self.idle_texture_pair = arcade.load_texture_pair(f"{base_path}car.png", hit_box_algorithm=hit_box_algorithm)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points
