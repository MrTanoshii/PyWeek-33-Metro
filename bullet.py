import arcade
from constants import BULLET_SCALING, SCREEN_WIDTH, SCREEN_HEIGHT


class Bullet(arcade.Sprite):
    """ Player Sprite """

    friendly_bullet_list = arcade.SpriteList()
    enemy_bullet_list = arcade.SpriteList()

    def __init__(self, hit_box_algorithm, speed_x, speed_y, angle=0, damage_value=1):
        # Let parent initialize
        super().__init__()

        # Speed
        self.speed_x = speed_x
        self.speed_y = speed_y

        # Damage
        self.damage_value = damage_value

        # Angle
        self.angle = angle

        # Set our scale
        self.scale = BULLET_SCALING

        # load player texture
        base_path = "resources/"
        self.idle_texture = arcade.load_texture(
            f"{base_path}images/bullet.png", hit_box_algorithm=hit_box_algorithm)
        # Load sounds
        self.audio_gunshot = arcade.load_sound(f"{base_path}audio/gunshot.wav")

        # Set the initial texture
        self.texture = self.idle_texture

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

    @classmethod
    def update(cls):
        # Cycle through all bullets
        for bullet in cls.friendly_bullet_list:
            # Delete bullets that are off-screen
            if bullet.center_x - bullet.width / 2 > SCREEN_WIDTH or bullet.center_y - bullet.height / 2 > SCREEN_HEIGHT:
                cls.friendly_bullet_list.remove(bullet)
