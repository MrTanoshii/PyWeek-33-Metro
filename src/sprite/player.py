import os.path
import math

import arcade

import src.const as C

from src.audio import Audio
import src.lib as lib
from src.sprite.weapon import Weapon


class Player(arcade.Sprite):
    """
    Player Sprite

    ...

    Attributes
    ----------
    player_list : arcade.SpriteList()
        List of player sprites
    weapon : arcade.Sprite()
        The weapon sprite
    audio_volume : float
        The volume of sfx

    Methods
    -------
    shoot(delta_time: float, shoot_pressed: bool)
        Handle shooting & reloading
    take_damage(damage_source: arcade.Sprite())
        Handles damage taken by player
    death()
        Handles death of player
    follow_mouse(mouse_x: float, mouse_y: float)

    on_mouse_motion(x: float, y: float, dx: float, dy: float)
        Listen to mouse motion event
    update(delta_time: float, movement_key_pressed: dict[str, bool], shoot_pressed: bool)
        Update the player
    move(movement_key_pressed: dict[str, bool])
        Move the player
    set_skin(name: str):
        change the player texture
    update_animation(delta_time: float)
        Update the animated texture
    """

    # SpriteList class attribute
    player_list = arcade.SpriteList()
    weapon = arcade.Sprite()

    def __init__(self, hit_box_algorithm, current_level):
        # Inherit parent class
        super().__init__()

        # Set player location
        self.center_x = C.SCREEN_WIDTH * .1 * lib.global_scale()
        self.center_y = C.SCREEN_HEIGHT * .5 * lib.global_scale()
        self.angle = C.SPRITE_PLAYER_INIT_ANGLE

        # Movement Speed
        self.max_speed = C.PLAYER.SPEED
        self.speed_x = 0
        self.speed_y = 0

        # Health
        self.max_health = C.PLAYER.MAX_HP
        self.cur_health = C.PLAYER.START_HP
        self.death_health = C.PLAYER.DEATH_HP

        # Weapon
        self.weapon = Weapon()
        Player.weapon = self.weapon
        self.weapon_angle = 0

        self.is_dead = None

        # Set our scale
        self.scale = C.PLAYER.SCALE * lib.global_scale()

        player_style = C.MAP_MONUMENTS_LIST[0]["player"]

        """ Load Assets """
        dir_name = f"src/resources/images/assets/players/{player_style}/"

        # Load texture
        self.texture_list = []
        for filename in sorted(os.listdir(f"{dir_name}animation/")):
            self.texture_list.append(
                arcade.load_texture(f"{dir_name}animation/{filename}",
                                    hit_box_algorithm=hit_box_algorithm))

        self.current_texture: float = 0
        self.animation_speed: float = C.PLAYER.ANIMATION_SPEED

        # Set the initial texture
        self.texture = self.texture_list[int(self.current_texture)]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

        # Set player sounds
        self.sfx_death_list = Audio.sfx_player_death_list

        # Find & set hit sfx
        self.sfx_hit_list = []
        for _i, sfx in enumerate(Audio.sfx_hit_list):
            if sfx["name"] == C.PLAYER.NAME:
                self.sfx_hit_list.append(sfx["sound_list"])
                break

        Player.player_list.append(self)

        self.level = current_level
        self._player_style = C.PLAYER_TEXTURES[self.level-1]["name"]
        # Create dictionary of all textures
        self.textures_dict = {}
        for weapon in C.PLAYER_WEAPONS:
            texture_list = []
            for filename in sorted(os.listdir(f"assets/{self._player_style}{weapon['name']}/")):
                texture_list.append(
                    arcade.load_texture(f"assets/{self._player_style}{weapon['name']}/{filename}",
                                        hit_box_algorithm=hit_box_algorithm))
            self.textures_dict[f"{self._player_style}{weapon['name']}"] = texture_list

        # Set default skin for ak and level style player
        self.set_skin(weapon="Revolver")

    def set_skin(self, weapon: str, player_style=None):
        """Takes asset/texture name as input and update current texture/skin"""
        if not player_style:
            player_style = self._player_style
        self.texture_list = self.textures_dict[f"{player_style}{weapon}"]

        self.texture = self.textures_dict[f"{player_style}{weapon}"][int(
            self.current_texture)]

    def shoot(self, delta_time, shoot_pressed):
        """Handles shooting & reloading"""
        self.weapon.shoot(delta_time, shoot_pressed, self)

        # if player shoots RPG, change skin
        if self.weapon.weapon_name == "RPG":
            if self.weapon.cur_ammo <= 0:
                self.set_skin(weapon="RPGempty")
            elif self.weapon.cur_ammo > 0:
                self.set_skin(weapon="RPG")

    def take_damage(self, damage_source):
        """Handles damage taken by player"""
        # Decrease player hp
        self.cur_health -= damage_source.damage_value
        # Cause death of player if hp low
        if self.cur_health <= self.death_health:
            self.death()

        # Play random player hit sfx
        Audio.play_rand_sound(self.sfx_hit_list)

    def death(self):
        """Handles death of player"""

        # TODO: Implement better player death
        self.cur_health = self.max_health

        # Play random death sfx
        Audio.play_rand_sound(self.sfx_death_list)

        self.is_dead = True

    def update(self, delta_time, movement_key_pressed, shoot_pressed):
        self.move(movement_key_pressed)
        self.shoot(delta_time, shoot_pressed)

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

        # Automatically move back towards left side
        if self.speed_x <= 0 and self.center_x > 50 * lib.global_scale():
            self.speed_x -= 1 * lib.global_scale()

        # Move player
        self.center_x += self.speed_x * lib.global_scale()
        self.center_y += self.speed_y * lib.global_scale()
        if self.center_x > C.SCREEN_WIDTH / 2:
            self.center_x = C.SCREEN_WIDTH / 2
        if self.center_x < 0:
            self.center_x = 0
        if self.center_y > C.SCREEN_HEIGHT * .85:
            self.center_y = C.SCREEN_HEIGHT * .85
        if self.center_y < C.SCREEN_HEIGHT * .15:
            self.center_y = C.SCREEN_HEIGHT * .15

    def update_animation(self, delta_time: float):
        """ Update the animated texture """

        self.current_texture = lib.find_next_texture(
            delta_time, self.current_texture, self.texture_list, self.animation_speed)
        self.texture = self.texture_list[int(self.current_texture)]
