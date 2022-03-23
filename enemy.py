import arcade
import os.path
import constants as C
import random
from bullet import Bullet
from gold import Gold
from player import Player
import weapon


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
    audio_volume = C.MASTER_VOLUME

    def __init__(self, hit_box_algorithm, level):
        # Let parent initialize

        super().__init__()

        enemy_style = C.MAP_MONUMENTS_LIST[level-1]["enemy"]

        # load enemy configs
        self.config = C.ENEMIES[enemy_style]

        """ Load Assets """
        base_path = f"resources/images/assets/enemies/{enemy_style}/"

        # Load texture
        self.texture_list = []
        for filename in os.listdir(f"{base_path}animation/"):
            self.texture_list.append(
                arcade.load_texture(f"{base_path}animation/{filename}", hit_box_algorithm=hit_box_algorithm))

        self.cur_texture = 0

        self.animation_speed = self.config["animation_speed"]

        # Set our scale
        self.scale = self.config["scale"]

        # Load sounds
        self.audio_destroyed = arcade.load_sound(f"{base_path}enemy_destroyed.wav")
        self.audio_hit = arcade.load_sound(f"{base_path}enemy_hit.wav")
        self.audio_volume = C.MASTER_VOLUME

        # Set the initial texture
        self.texture = self.texture_list[0]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

        """ Atributes """
        # Speed
        self.SPEED = self.config["speed"]
        self.current_speed = 0

        # Health
        self.HP = self.config["health"]

        # Shooting
        self.damage_value = self.config["damage"]
        self.weapon = self.config["weapon"]
        self.bullet_scale = self.config["bullet_scale"]
        self.shooting_speed = self.config["shooting_speed"]
        self.bullet_speed = self.config["bullet_speed"]
        self.barrel_location = self.config["barrel"]

    @classmethod
    def spawn_enemy(cls, level):
        enemy = Enemy(hit_box_algorithm="Simple", level=level)

        # Set enemy location
        enemy.center_x = C.SCREEN_WIDTH + enemy.width
        enemy.center_y = C.SCREEN_HEIGHT // 2 + \
            random.uniform(-C.SCREEN_HEIGHT/3.25, C.SCREEN_HEIGHT/3.25)

        # Turn the enemy 90 degree
        enemy.angle = 0

        # Add to player sprite list
        cls.enemy_list.append(enemy)

    def despawn(self, death):
        if death == C.DEATH.KILLED:
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
                enemy.despawn(death=C.DEATH.OOB)

    @classmethod
    def preload(cls, level):
        Enemy.spawn_enemy(level)

        cls.enemy_list = arcade.SpriteList()

    def shoot(self, enemy_bullet_list):
        """Handle enemy shooting"""
        bullet = Bullet(
            hit_box_algorithm="Simple",
            speed_x=-self.bullet_speed,
            speed_y=0,
            texture_list=weapon.bullet_texture_lists_list[self.weapon],
            angle=180,
            damage_value=self.damage_value,
            scale=self.bullet_scale)

        # Set bullet location
        bullet.position = ((self.center_x - (self.width / 2) + self.barrel_location[0]), (self.center_y - (self.height / 2) + self.barrel_location[1]))

        # Turn the bullet -90 degree
        # bullet.angle = 0

        # Add to bullet sprite list
        enemy_bullet_list.append(bullet)

        # Play a sound
        arcade.play_sound(bullet.audio_gunshot)

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += delta_time * 0.02
        if self.cur_texture > len(self.texture_list) - 1:
            self.cur_texture = 0
