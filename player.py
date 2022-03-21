import arcade
from constants import CHARACTER_SCALING, PLAYER_DEATH_HP, PLAYER_GUN_DAMAGE, PLAYER_GUN_RELOAD_TIME, PLAYER_GUN_SHOOT_SPEED, PLAYER_MAX_HP, PLAYER_START_HP, PLAYER_GUN_MAX_AMMO
from bullet import Bullet
import time


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

        # Shooting
        self.can_shoot = True
        self.shoot_speed = PLAYER_GUN_SHOOT_SPEED
        self.shoot_timer = 0
        self.gun_damage = PLAYER_GUN_DAMAGE

        # Ammo
        self.max_ammo = PLAYER_GUN_MAX_AMMO
        self.cur_ammo = self.max_ammo
        self.reload_speed = PLAYER_GUN_RELOAD_TIME
        self.is_reloading = False
        self.reload_timer = 0

        # Set our scale
        self.scale = CHARACTER_SCALING

        # load player texture
        base_path = "resources/"
        self.idle_texture_pair = arcade.load_texture_pair(
            f"{base_path}images/car.png", hit_box_algorithm=hit_box_algorithm)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

        # Load sounds
        # TODO: Change SFX
        self.audio_destroyed = arcade.load_sound(
            f"{base_path}audio/enemy_destroyed.wav")
        self.audio_hit = arcade.load_sound(f"{base_path}audio/enemy_hit.wav")

    def shoot(self, friendly_bullet_list):
        if not self.is_reloading and self.cur_ammo > 0:
            self.cur_ammo -= 1
            bullet = Bullet("Detailed", 20, 0, damage_value=self.gun_damage)

            # Set bullet location
            bullet.center_x = self.center_x + self.width
            bullet.center_y = self.center_y

            # Add to bullet sprite list
            friendly_bullet_list.append(bullet)

            # Play weapon shoot sfx
            arcade.play_sound(bullet.audio_gunshot)

            if self.cur_ammo <= 0:
                self.is_reloading = True
        # else:
            # Play empty gun sfx

    def reload_weapon(self):
        """Handles gun reload"""
        self.cur_ammo = self.max_ammo
        self.reload_timer = 0
        self.is_reloading = False
        self.can_shoot = True
        # Play weapon reload sfx

    def take_damage(self, damage_source):
        """Handles damage taken by Player"""
        # Play damage taken sound
        # TODO: Change sound effect
        arcade.play_sound(self.audio_destroyed)
        # Decrease player hp
        self.cur_health -= damage_source.damage_value
        # Cause death of player if hp low
        if self.cur_health <= self.death_health:
            self.death()

    def death(self):
        """Handles death of Player"""
        # TO BE IMPROVED, player health resets
        self.cur_health = self.max_health
        print("You died.")
