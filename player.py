import arcade
from constants import CHARACTER_SCALING, PLAYER_DEATH_HP, PLAYER_MAX_HP, PLAYER_START_HP
from bullet import Bullet


class Player(arcade.Sprite):
    """ Player Sprite """

    def __init__(self, hit_box_algorithm):
        # Let parent initialize
        super().__init__()

        # Movement Speed
        self.current_speed = 0
        self.SPEED = 3

        # Health
        self.max_health = PLAYER_START_HP
        self.cur_health = PLAYER_MAX_HP
        self.death_health = PLAYER_DEATH_HP

        # Set our scale
        self.scale = CHARACTER_SCALING

        # load player texture
        base_path = "resources/images/"
        self.idle_texture_pair = arcade.load_texture_pair(
            f"{base_path}car.png", hit_box_algorithm=hit_box_algorithm)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

    def shoot(self, bullet_list):
        bullet = Bullet(hit_box_algorithm="Detailed")

        # Set bullet location
        bullet.center_x = self.center_x + self.width
        bullet.center_y = self.center_y

        # Turn the bullet -90 degree
        # bullet.angle = 0

        # Add to bullet sprite list
        bullet_list.append(bullet)

        # Play a sound
        arcade.play_sound(bullet.audio_gunshot)

    def take_damage(self, damage_source):
        """Handles damage taken by Player"""
        self.cur_health -= damage_source.damage_value
        if self.cur_health <= self.death_health:
            self.death()

    def death(self):
        """Handles death of Player"""
        # TO BE IMPROVED, player health resets
        self.cur_health = self.max_health
