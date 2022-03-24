import arcade
import os.path
import random
import constants as C
from bullet import Bullet
from gold import Gold
from player import Player
from audio import Audio
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

    def __init__(self, hit_box_algorithm, level):
        # Inherit parent class

        super().__init__()

        enemy_style = C.MAP_MONUMENTS_LIST[level-1]["enemy"]

        # load enemy configs
        self.config = enemy_style
        self.name = self.config["name"]
        self.barrel_location = self.config["barrel"]

        # Speed
        self.SPEED = self.config["speed"]
        self.current_speed = 0

        # Health
        self.HP = self.config["health"]

        # Set Weapon
        for weapon in C.ENEMY_WEAPON_LIST:
            if weapon["name"] == self.name:
                self.damage_value = weapon["bullet_damage"]
                self.weapon = weapon["name"]
                self.bullet_scale = weapon["bullet_scale"]
                self.shooting_speed = weapon["shoot_time"]
                self.bullet_speed = weapon["bullet_speed"]
                break

        """ Load Assets """
        base_path = f"resources/images/assets/enemies/{self.name}/"

        # Load texture
        self.texture_list = []
        file_name_list = os.listdir(f"{base_path}animation/")
        file_name_list = sorted(file_name_list, key=lambda x: int(x.split('.')[0]))
        for filename in file_name_list:
            self.texture_list.append(
                arcade.load_texture(f"{base_path}animation/{filename}", hit_box_algorithm=hit_box_algorithm))

        self.cur_texture = 0

        self.animation_speed = self.config["animation_speed"]

        # Set our scale
        self.scale = C.ENEMY_SCALING

        # Find & set hit sfx
        for i in range(0, len(Audio.sfx_enemy_hit_list)):
            if Audio.sfx_enemy_hit_list[i]["enemy_name"] == self.name:
                self.sfx_hit_list = Audio.sfx_enemy_hit_list[i]["sound"]
                break

        # Find & set death sfx
        for i in range(0, len(Audio.sfx_enemy_death_list)):
            if Audio.sfx_enemy_death_list[i]["enemy_name"] == self.name:
                self.sfx_death_list = Audio.sfx_enemy_death_list[i]["sound"]
                break

        # Find & set single shot sfx
        for i in range(0, len(Audio.sfx_enemy_weapon_shoot_list)):
            if Audio.sfx_enemy_weapon_shoot_list[i]["weapon_name"] == self.weapon:
                self.sfx_single_shot_list = Audio.sfx_enemy_weapon_shoot_list[i]["sound"]
                break

        # Set the initial texture
        self.texture = self.texture_list[0]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

        """ Atributes """

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
        # Play enemy death sfx
        Audio.play_rand_sound(self.sfx_death_list)

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
                cls.despawn(enemy, C.DEATH.OOB)

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
        bullet.position = ((self.center_x - (self.width / 2) +
                           self.barrel_location[0]), (self.center_y - (self.height / 2) + self.barrel_location[1]))

        # Turn the bullet -90 degree
        # bullet.angle = 0

        # Add to bullet sprite list
        enemy_bullet_list.append(bullet)

        # Play weapon shoot sfx
        Audio.play_rand_sound(self.sfx_single_shot_list)

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += delta_time * self.animation_speed
        if self.cur_texture > len(self.texture_list) - 1:
            self.cur_texture = 0
        self.texture = self.texture_list[int(self.cur_texture)]