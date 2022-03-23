import arcade
import os.path
from constants import ENEMY_SCALING, SCREEN_WIDTH, SCREEN_HEIGHT, DEATH
from constants import MASTER_VOLUME
import random
from bullet import Bullet
from gold import Gold
from player import Player


class Enemy(arcade.Sprite):
    """
    Enemy Sprite

    ...

    Attributes
    ----------
    enemy_list : arcade.SpriteList()
        List of friendly enemy sprites
    audio_volume : float
        The volume of sfx

    Class Methods
    -------------
    spawn_enemy()
        Create the enemy
    update()
        Update the enemy
    preload()
        Preload the enemy resources

    Methods
    -------
    despawn()
        Remove the enemy
    shoot(enemy_bullet_list: arcade.SpriteList())
        Handle enemy shooting
    """

    # SpriteList class attribute
    enemy_list = arcade.SpriteList()

    # Volume class attribute
    audio_volume = MASTER_VOLUME



    def __init__(self, hit_box_algorithm, level):
        # Let parent initialize

        super().__init__()

        self.current_speed = 0
        self.SPEED = -2
        self.HP = 10

        # Damage
        self.damage_value = 3

        # Set our scale
        self.scale = ENEMY_SCALING

        """ Load Assets """
        base_path = f"resources/images/levels/{level}/"

        # Load texture
        self.texture_list = []
        for i in range(1, 12):
            if os.path.exists(f"{base_path}enemy/{i}.png"):
                self.texture_list.append(arcade.load_texture(f"{base_path}enemy/{i}.png", hit_box_algorithm=hit_box_algorithm))
            else: break

        self.cur_texture = 0

        # Load sounds
        self.audio_destroyed = arcade.load_sound(f"{base_path}enemy_destroyed.wav")
        self.audio_hit = arcade.load_sound(f"{base_path}enemy_hit.wav")
        self.audio_volume = MASTER_VOLUME

        # Set the initial texture
        self.texture = self.texture_list[int(self.cur_texture)]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

    @classmethod
    def spawn_enemy(cls, level):
        enemy = Enemy(hit_box_algorithm="Simple", level=level)

        # Set enemy location
        enemy.center_x = SCREEN_WIDTH + enemy.width
        enemy.center_y = SCREEN_HEIGHT // 2 + \
            random.uniform(-SCREEN_HEIGHT/3.25, SCREEN_HEIGHT/3.25)

        # Turn the enemy 90 degree
        enemy.angle = 0

        # Add to player sprite list
        cls.enemy_list.append(enemy)

    def despawn(self, death):
        if death == DEATH.KILLED:
            Gold.spawn(self.center_x, self.center_y)
        self.remove_from_sprite_lists()

    @classmethod
    def update(cls):
        # Cycle trough all enemies
        for enemy in cls.enemy_list:

            # Move all Enemies Forwards
            enemy.center_x += enemy.SPEED

            # Check if enemy is in view, if not delete it
            if enemy.center_x + enemy.width < 0:
                cls.despawn(enemy, DEATH.OOB)

    @classmethod
    def preload(cls, level):
        Enemy.spawn_enemy(level)

        cls.enemy_list = arcade.SpriteList()

    def shoot(self, enemy_bullet_list):
        """Handle enemy shooting"""
        bullet = Bullet("Simple", -20, 0,
                        Player.weapon.bullet_texture_list, 180)

        # Set bullet location
        bullet.center_x = self.center_x + self.width
        bullet.center_y = self.center_y

        # Turn the bullet -90 degree
        # bullet.angle = 0

        # Add to bullet sprite list
        enemy_bullet_list.append(bullet)

        # Play a sound
        arcade.play_sound(bullet.audio_gunshot)

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 0.02
        if self.cur_texture > len(self.texture_list) - 1:
            self.cur_texture = 0
        self.texture = self.texture_list[int(self.cur_texture)]
