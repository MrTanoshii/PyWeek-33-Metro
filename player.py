import arcade
import constants as C
from bullet import Bullet
import math
from lib import calculate_angle


class Player(arcade.Sprite):
    """ Player Sprite """
    player_list = arcade.SpriteList()

    audio_volume = C.MASTER_VOLUME

    current_level = None

    def __init__(self, hit_box_algorithm):
        # Let parent initialize
        super().__init__()

        # Set player location
        self.center_x = C.SCREEN_WIDTH * .1
        self.center_y = C.SCREEN_HEIGHT * .5
        self.angle = C.SPRITE_PLAYER_INIT_ANGLE

        # Movement Speed

        self.max_speed = C.SPEED_PLAYER
        self.speed_x = 0
        self.speed_y = 0

        # Health
        self.max_health = C.PLAYER_START_HP
        self.cur_health = C.PLAYER_MAX_HP
        self.death_health = C.PLAYER_DEATH_HP

        # Shooting
        self.can_shoot = True
        self.shoot_speed = C.PLAYER_GUN_SHOOT_SPEED
        self.shoot_timer = 0
        self.gun_damage = C.PLAYER_GUN_DAMAGE
        self.gun_angle = 0

        # Ammo
        self.max_ammo = C.PLAYER_GUN_MAX_AMMO
        self.cur_ammo = self.max_ammo
        self.gun_bullet_speed = C.PLAYER_GUN_BULLET_SPEED
        self.reload_speed = C.PLAYER_GUN_RELOAD_TIME
        self.is_reloading = False
        self.reload_timer = 0

        # Set our scale
        self.scale = C.CHARACTER_SCALING

        # load player texture
        base_path = "resources/"
        self.idle_texture = arcade.load_texture(
            f"{base_path}images/donky-example-player.png", hit_box_algorithm=hit_box_algorithm)

        # Set the initial texture
        self.texture = self.idle_texture

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

        # Load sounds
        # TODO: Change SFX
        self.audio_destroyed = arcade.load_sound(
            f"{base_path}audio/enemy_destroyed.wav")
        self.audio_hit = arcade.load_sound(f"{base_path}audio/enemy_hit.wav")

        Player.player_list.append(self)


    def shoot(self, friendly_bullet_list):
        if not self.is_reloading and self.cur_ammo > 0:
            self.cur_ammo -= 1

            # Calculate bullet speed
            speed_x = self.gun_bullet_speed * \
                math.cos(math.radians(self.gun_angle +
                         C.WEAPON_INIT_ANGLE))
            speed_y = self.gun_bullet_speed * \
                math.sin(math.radians(self.gun_angle +
                         C.WEAPON_INIT_ANGLE))

            bullet = Bullet("Detailed", speed_x, speed_y,
                            self.gun_angle + C.WEAPON_INIT_ANGLE, self.gun_damage)

            # Set bullet location
            bullet.center_x = self.center_x + \
                (self.width / 2 *
                 math.cos(math.radians(self.gun_angle + C.WEAPON_INIT_ANGLE)))
            bullet.center_y = self.center_y + \
                (self.height / 2 *
                 math.sin(math.radians(self.gun_angle + C.WEAPON_INIT_ANGLE)))

            # Add to bullet sprite list
            friendly_bullet_list.append(bullet)

            # Play weapon shoot sfx
            arcade.play_sound(bullet.audio_gunshot, volume=self.audio_volume)

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
        arcade.play_sound(self.audio_destroyed, volume=self.audio_volume)
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

    def follow_mouse(self, mouse_x: float, mouse_y: float):
        """Handles bullet angle rotation to follow mouse"""
        new_angle = calculate_angle(
            self.center_x, self.center_y, mouse_x, mouse_y)
        if mouse_x < self.center_x:
            new_angle = new_angle + C.WEAPON_INIT_ANGLE
        else:
            new_angle = new_angle - C.WEAPON_INIT_ANGLE
        self.gun_angle = new_angle


    def on_mouse_motion(self, x, y, dx, dy):
        """Called whenever mouse is moved."""
        self.player.follow_mouse(x, y)

    def update(self, movement_key_pressed):
        self.move(movement_key_pressed)

    def move(self, movement_key_pressed):
        """Deduce player movement direction from pressed movement keys."""

        # Find direction of movement
        player_move_dir = None
        if movement_key_pressed["left"]:
            if movement_key_pressed["up"]:
                player_move_dir = C.MOVE_DIRECTION.TOP_LEFT
            elif movement_key_pressed["down"]:
                player_move_dir = C.MOVE_DIRECTION.BOTTOM_LEFT
            else:
                player_move_dir = C.MOVE_DIRECTION.LEFT
        elif movement_key_pressed["right"]:
            if movement_key_pressed["up"]:
                player_move_dir = C.MOVE_DIRECTION.TOP_RIGHT
            elif movement_key_pressed["down"]:
                player_move_dir = C.MOVE_DIRECTION.BOTTOM_RIGHT
            else:
                player_move_dir = C.MOVE_DIRECTION.RIGHT
        elif movement_key_pressed["up"]:
            player_move_dir = C.MOVE_DIRECTION.TOP
        elif movement_key_pressed["down"]:
            player_move_dir = C.MOVE_DIRECTION.BOTTOM
        else:
            player_move_dir = C.MOVE_DIRECTION.IDLE

        # Calculate speed in x and y axes
        self.speed_x = 0
        self.speed_y = 0
        if player_move_dir == C.MOVE_DIRECTION.LEFT:
            self.speed_x = -self.max_speed
            self.speed_y = 0
        elif player_move_dir == C.MOVE_DIRECTION.BOTTOM_LEFT:
            self.speed_x = -self.max_speed * math.cos(math.radians(45))
            self.speed_y = -self.max_speed * math.sin(math.radians(45))
        elif player_move_dir == C.MOVE_DIRECTION.BOTTOM:
            self.speed_x = 0
            self.speed_y = -self.max_speed
        elif player_move_dir == C.MOVE_DIRECTION.BOTTOM_RIGHT:
            self.speed_x = self.max_speed * math.cos(math.radians(45))
            self.speed_y = -self.max_speed * math.sin(math.radians(45))
        elif player_move_dir == C.MOVE_DIRECTION.RIGHT:
            self.speed_x = self.max_speed
            self.speed_y = 0
        elif player_move_dir == C.MOVE_DIRECTION.TOP_RIGHT:
            self.speed_x = self.max_speed * math.cos(math.radians(45))
            self.speed_y = self.max_speed * math.sin(math.radians(45))
        elif player_move_dir == C.MOVE_DIRECTION.TOP:
            self.speed_x = 0
            self.speed_y = self.max_speed
        elif player_move_dir == C.MOVE_DIRECTION.TOP_LEFT:
            self.speed_x = -self.max_speed * math.cos(math.radians(45))
            self.speed_y = self.max_speed * math.sin(math.radians(45))

        # Move player
        self.center_x += self.speed_x
        self.center_y += self.speed_y
        if self.center_x > C.SCREEN_WIDTH / 2:
            self.center_x = C.SCREEN_WIDTH / 2
        if self.center_x < 0:
            self.center_x = 0
        if self.center_y > C.SCREEN_HEIGHT * .85:
            self.center_y = C.SCREEN_HEIGHT * .85
        if self.center_y < C.SCREEN_HEIGHT * .15:
            self.center_y = C.SCREEN_HEIGHT * .15