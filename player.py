import arcade
import os.path
import constants as C
from bullet import Bullet
import math
from lib import calculate_angle
from weapon import Weapon
from bullet import Bullet
from audio import Audio


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
    """

    # SpriteList class attribute
    player_list = arcade.SpriteList()
    weapon = arcade.Sprite()

    def __init__(self, hit_box_algorithm):
        # Inherit parent class
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
        self.max_health = C.PLAYER.MAX_HP
        self.cur_health = C.PLAYER.START_HP
        self.death_health = C.PLAYER.DEATH_HP

        # Weapon
        self.weapon = Weapon()
        Player.weapon = self.weapon
        self.weapon_angle = 0

        # Set our scale
        self.scale = C.CHARACTER_SCALING

        player_style = C.MAP_MONUMENTS_LIST[0]["player"]

        """ Load Assets """
        base_path = f"resources/images/assets/players/{player_style}/"

        # Load texture
        self.texture_list = []
        for filename in os.listdir(f"{base_path}animation/"):
            self.texture_list.append(
                arcade.load_texture(f"{base_path}animation/{filename}", hit_box_algorithm=hit_box_algorithm))

        self.cur_texture = 0

        # Set the initial texture
        self.texture = self.texture_list[int(self.cur_texture)]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

        # Set player sounds
        self.sfx_death_list = Audio.sfx_player_death_list
        self.sfx_hit_list = Audio.sfx_player_hit_list

        Player.player_list.append(self)

    def shoot(self, delta_time, shoot_pressed):
        """Handles shooting & reloading"""

        # Reload weapon
        if self.weapon.is_reloading and not shoot_pressed:
            self.weapon.reload_timer += delta_time
            if self.weapon.reload_timer >= self.weapon.reload_time:
                self.weapon.reload_weapon()
        if self.weapon.can_shoot and shoot_pressed:
            # Shoot if ammo available
            # TODO: Implement fire_type
            if self.weapon.cur_ammo > 0:
                self.weapon.can_shoot = False
                self.weapon.is_reloading = False
                # Decrease ammo count
                self.weapon.cur_ammo -= 1
                # Calculate bullet speed
                speed_x = self.weapon.bullet_speed * \
                    math.cos(math.radians(self.weapon_angle +
                                          C.WEAPON_INIT_ANGLE))
                speed_y = self.weapon.bullet_speed * \
                    math.sin(math.radians(self.weapon_angle +
                                          C.WEAPON_INIT_ANGLE))

                bullet = Bullet("Detailed", speed_x, speed_y, self.weapon.bullet_texture_list,
                                self.weapon_angle + C.WEAPON_INIT_ANGLE, self.weapon.bullet_damage, scale=self.weapon.bullet_scale)

                # Set bullet location
                bullet.center_x = self.center_x + \
                    (self.width / 2 *
                        math.cos(math.radians(self.weapon_angle + C.WEAPON_INIT_ANGLE)))
                bullet.center_y = self.center_y + \
                    (self.height / 2 *
                        math.sin(math.radians(self.weapon_angle + C.WEAPON_INIT_ANGLE)))

                # Add to bullet sprite list
                Bullet.friendly_bullet_list.append(bullet)

                # Play random weapon shoot sfx
                Audio.play_rand_sound(self.weapon.sfx_single_shot_list)

                # Start reload if ammo depleted
                if self.weapon.cur_ammo <= 0:
                    self.weapon.is_reloading = True

                self.weapon.shoot_timer = 0
            else:
                # Reload weapon
                self.weapon.reload_timer += delta_time
                if self.weapon.reload_timer >= self.weapon.reload_time:
                    self.weapon.reload_weapon()
                # TODO: Play empty weapon sfx
        else:
            self.weapon.shoot_timer += delta_time
            if self.weapon.shoot_timer >= self.weapon.shoot_time:
                self.weapon.can_shoot = True
                self.weapon.shoot_timer = 0

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

    def follow_mouse(self, mouse_x: float, mouse_y: float):
        """Handles bullet angle rotation to follow mouse"""
        new_angle = calculate_angle(
            self.center_x, self.center_y, mouse_x, mouse_y)
        if mouse_x < self.center_x:
            new_angle = new_angle + C.WEAPON_INIT_ANGLE
        else:
            new_angle = new_angle - C.WEAPON_INIT_ANGLE
        self.weapon_angle = new_angle

    def on_mouse_motion(self, x, y, dx, dy):
        """Called whenever mouse is moved."""
        self.player.follow_mouse(x, y)

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

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 0.02
        if self.cur_texture > len(self.texture_list) - 1:
            self.cur_texture = 0
        self.texture = self.texture_list[int(self.cur_texture)]
