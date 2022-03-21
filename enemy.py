import arcade
from constants import ENEMY_SCALING, SCREEN_WIDTH, SCREEN_HEIGHT
import random
from bullet import Bullet


class Enemy(arcade.Sprite):
    enemy_list = arcade.SpriteList()

    """ Player Sprite """

    def __init__(self, hit_box_algorithm):
        # Let parent initialize
        super().__init__()

        self.current_speed = 0
        self.SPEED = -2
        self.HP = 10

        # Set our scale
        self.scale = ENEMY_SCALING

        # load player texture
        base_path = "resources/"
        self.idle_texture_pair = arcade.load_texture_pair(
            f"{base_path}images/enemy.png", hit_box_algorithm=hit_box_algorithm)
        # Load sounds
        self.audio_destroyed = arcade.load_sound(
            f"{base_path}audio/enemy_destroyed.wav")
        self.audio_hit = arcade.load_sound(f"{base_path}audio/enemy_hit.wav")

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

    @classmethod
    def spawn_enemy(cls):
        enemy = Enemy(hit_box_algorithm="Detailed")

        # Set bullet location
        enemy.center_x = SCREEN_WIDTH + enemy.width
        enemy.center_y = SCREEN_HEIGHT // 2 + \
            random.uniform(-SCREEN_HEIGHT/3.25, SCREEN_HEIGHT/3.25)

        # Turn the enemy 90 degree
        enemy.angle = -90

        # Add to player sprite list
        cls.enemy_list.append(enemy)

    @classmethod
    def update(cls):
        # Cycle trough all enemies
        for enemy in cls.enemy_list:

            # Move all Enemies Forwards
            enemy.center_x += enemy.SPEED

            # Check if enemy is in view, if not delete it
            if enemy.center_x + enemy.width < 0:
                enemy.remove_from_sprite_lists()

    def shoot(self, enemy_bullet_list):
        """Handle Enemy shooting"""
        bullet = Bullet(hit_box_algorithm="Detailed")

        # Set bullet location
        bullet.center_x = self.center_x + self.width
        bullet.center_y = self.center_y

        # Turn the bullet -90 degree
        # bullet.angle = 0

        # Add to bullet sprite list
        enemy_bullet_list.append(bullet)

        # Play a sound
        arcade.play_sound(bullet.audio_gunshot)
