import arcade
from constants import ENEMY_SCALING


class Enemy(arcade.Sprite):
    """ Player Sprite """
    def __init__(self, hit_box_algorithm):
        # Let parent initialize
        super().__init__()

        self.current_speed = 0
        self.SPEED = -2
        self.HIT_POINTS = 10

        # Set our scalea
        self.scale = ENEMY_SCALING

        # load player texture
        base_path = "resources/"
        self.idle_texture_pair = arcade.load_texture_pair(f"{base_path}images/enemy.png", hit_box_algorithm=hit_box_algorithm)
        # Load sounds
        self.audio_destroyed = arcade.load_sound(f"{base_path}audio/enemy_destroyed.wav")
        self.audio_hit = arcade.load_sound(f"{base_path}audio/enemy_hit.wav")

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points
