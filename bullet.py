import arcade
from constants import BULLET_SCALING


class Bullet(arcade.Sprite):
    """ Player Sprite """
    def __init__(self, hit_box_algorithm):
        # Let parent initialize
        super().__init__()

        self.current_speed = 0
        self.SPEED = 20
        self.DAMAGE = 2

        # Set our scale
        self.scale = BULLET_SCALING

        # load player texture
        base_path = "resources/"
        self.idle_texture_pair = arcade.load_texture_pair(f"{base_path}images/bullet.png", hit_box_algorithm=hit_box_algorithm)
        # Load sounds
        self.audio_gunshot = arcade.load_sound(f"{base_path}audio/gunshot.wav")

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points
