import arcade
import os.path
import const.constants as C
import math
from weapon import Weapon
from audio import Audio
from lib import global_scale


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
    """

    # SpriteList class attribute
    player_list = arcade.SpriteList()
    weapon = arcade.Sprite()

    def __init__(self, hit_box_algorithm, current_level):
        # Inherit parent class
        super().__init__()

        # Set player location
        self.center_x = C.SCREEN_WIDTH * .1 * global_scale()
        self.center_y = C.SCREEN_HEIGHT * .5 * global_scale()
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

        # Set our scale
        self.scale = C.PLAYER.SCALE * global_scale()

        player_style = C.MAP_MONUMENTS_LIST[0]["player"]

        """ Load Assets """
        dir_name = f"resources/images/assets/players/{player_style}/"

        # Load texture
        self.texture_list = []
        for filename in os.listdir(f"{dir_name}animation/"):
            self.texture_list.append(
                arcade.load_texture(f"{dir_name}animation/{filename}", hit_box_algorithm=hit_box_algorithm))

        self.cur_texture = 0

        # Set the initial texture
        self.texture = self.texture_list[int(self.cur_texture)]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

        # Set player sounds
        self.sfx_death_list = Audio.sfx_player_death_list
        self.sfx_hit_list = Audio.sfx_player_hit_list

        Player.player_list.append(self)

        self.level = current_level
        self._player_style = C.PLAYER_TEXTURES[self.level-1]["name"]
        # Create dictionary of all textures
        self.textures_dict = {}
        for weapon in C.PLAYER_WEAPONS:
            texture_list = []
            for filename in os.listdir(f"assets/{self._player_style}{weapon['name']}/"):
                texture_list.append(
                    arcade.load_texture(f"assets/{self._player_style}{weapon['name']}/{filename}", hit_box_algorithm=hit_box_algorithm))
            self.textures_dict[f"{self._player_style}{weapon['name']}"] = texture_list

        # Set default skin for ak and level style player
        self.set_skin(weapon="AK")

    def set_skin(self, weapon: str, player_style=None):
        if not player_style: player_style = self._player_style
        """Takes asset/texture name as input and update current texture/skin"""
        self.texture_list = self.textures_dict[f"{player_style}{weapon}"]

        self.texture = self.textures_dict[f"{player_style}{weapon}"][int(self.cur_texture)]

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

        print("You died.")

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

        # Move player
        self.center_x += self.speed_x * global_scale()
        self.center_y += self.speed_y * global_scale()
        if self.center_x > C.SCREEN_WIDTH / 2 * global_scale():
            self.center_x = C.SCREEN_WIDTH / 2 * global_scale()
        if self.center_x < 0 * global_scale():
            self.center_x = 0 * global_scale()
        if self.center_y > C.SCREEN_HEIGHT * .85 * global_scale():
            self.center_y = C.SCREEN_HEIGHT * .85 * global_scale()
        if self.center_y < C.SCREEN_HEIGHT * .15 * global_scale():
            self.center_y = C.SCREEN_HEIGHT * .15 * global_scale()

    def update_animation(self, delta_time: float = 1 / 60):
        # TODO: Change animation speed from hardcoded to constant
        animation_speed = 0.20

        if len(self.texture_list) > 1:
            self.cur_texture += animation_speed * delta_time
            while self.cur_texture >= len(self.texture_list) - 1:
                self.cur_texture -= len(self.texture_list) - 1
                if (self.cur_texture <= 0):
                    self.cur_texture = 0
                    break
        self.texture = self.texture_list[int(self.cur_texture)]
