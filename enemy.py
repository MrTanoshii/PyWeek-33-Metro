import arcade
import constants as C
import random
from bullet import Bullet
from gold import Gold
from player import Player
from audio import Audio


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

    def __init__(self, hit_box_algorithm):
        # Inherit parent class
        super().__init__()

        self.current_speed = 0
        self.SPEED = -2
        self.HP = 10

        # Damage
        self.damage_value = 3

        # Set our scale
        self.scale = C.ENEMY_SCALING

        # load player texture
        base_path = "resources/"
        self.idle_texture = arcade.load_texture(
            f"{base_path}images/tank_enemy.png", hit_box_algorithm=hit_box_algorithm)

        # TODO: Change hardcoded enemy
        self.name = C.ENEMY_LIST[0]["name"]
        self.weapon = C.ENEMY_WEAPON_LIST[0]["name"]

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
        self.texture = self.idle_texture

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

    @classmethod
    def spawn_enemy(cls):
        enemy = Enemy(hit_box_algorithm="Simple")

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
    def preload(cls):
        Enemy.spawn_enemy()

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

        # Play weapon shoot sfx
        Audio.play_rand_sound(self.sfx_single_shot_list)
