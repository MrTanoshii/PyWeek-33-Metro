import const.constants as C
import arcade
import math
import random
from bullet import Bullet
from audio import Audio
from lib import calculate_angle, global_scale
import sys
import os


bullet_texture_lists_list = {}

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)


# Create example bullet texture lists
def init_bullet_texture_lists():

    # Load animated bullet textures
    for enemy_weapon in C.ENEMY_WEAPON_LIST:
        bullet_texture_list = []
        for i in range(1, enemy_weapon["bullet_texture_amount"] + 1):
            bullet_texture_list.append(arcade.load_texture(
                f"resources/images/weapon/" +
                enemy_weapon["bullet_texture_dir_name"] +
                "/bullet/" + str(i) + ".png",
                hit_box_algorithm="Simple"))
        bullet_texture_lists_list[enemy_weapon["name"]] = bullet_texture_list


init_bullet_texture_lists()


class Weapon(arcade.Sprite):
    """
    Weapon Sprite

    ...

    Attributes
    ----------
    current_level : int
        Hold the current level

    Methods
    -------
    update_tracked_ammo(weapon_name: str, ammo_count: int)
        Keep the ammo count tracked
    reload_weapon()
        Reloads the current weapon
    shoot(self, delta_time: float, shoot_pressed: bool, player: arcade.Sprite)
        Handles shooting and reloading
    swap_weapon(weapon_name: str)
        Swap the current weapon
    set_weapon(weapon_name: str)
        Set the current weapon
    on_mouse_motion(self, x, y, _dx, _dy)
        Called whenever mouse is moved
    """

    def __init__(self):
        # Inherit parent class
        super().__init__()

        # Set sound
        self.sound = None

        self.tracked_ammo = {}
        for weapon in C.WEAPON_LIST:
            self.tracked_ammo[weapon["name"]
                              ] = weapon["max_ammo"]

        # Set default weapon
        self.set_weapon("Revolver")

        self.last_mouse_x = 0
        self.last_mouse_y = 0

    def update_tracked_ammo(self, weapon_name: str, ammo_count: int):
        """ Keep the ammo count tracked """
        for weapon in self.tracked_ammo:
            if weapon == weapon_name:
                self.tracked_ammo[weapon] = ammo_count
                break

    def reload_weapon(self):
        """ Reloads the current weapon """
        # Increment ammo count
        self.cur_ammo += self.reload_rate
        self.update_tracked_ammo(self.weapon_name, self.cur_ammo)

        # Allow shooting if ammo present
        self.can_shoot = True

        self.reload_timer = 0

        # TODO: Play weapon reload sfx

        # Finish reloading
        if self.cur_ammo >= self.max_ammo:
            # Do not allow over-reload
            self.cur_ammo = self.max_ammo

            self.is_reloading = False

    def shoot(self, delta_time: float, shoot_pressed: bool, player: arcade.Sprite):
        """ Handles shooting and reloading """

        # Reload weapon
        if self.is_reloading and not shoot_pressed:
            self.reload_timer += delta_time
            if self.reload_timer >= self.reload_time:
                self.reload_weapon()
        if self.can_shoot and shoot_pressed:
            # Shoot if ammo available
            # TODO: Implement fire_type
            if self.cur_ammo > 0:
                self.is_reloading = False
                self.can_shoot = False

                # Decrease ammo count
                self.cur_ammo -= 1
                self.update_tracked_ammo(
                    self.weapon_name, self.cur_ammo)

                # Instantiate the amount of bullets per shot
                for _ in range(0, self.bullet_amount):
                    # Calculate angle from player to mouse location
                    calc_angle = calculate_angle(
                        player.center_x, player.center_y, self.last_mouse_x + C.GUI["Crosshair"]["offset_x"], self.last_mouse_y + C.GUI["Crosshair"]["offset_y"])
                    if self.last_mouse_x + C.GUI["Crosshair"]["offset_x"] < player.center_x:
                        calc_angle = calc_angle + self.init_angle
                    else:
                        calc_angle = calc_angle - self.init_angle
                    self.weapon_angle = calc_angle

                    # Calculate bullet location
                    bullet_center_x = player.center_x + \
                        (player.width / 2 *
                            math.cos(math.radians(self.weapon_angle + self.init_angle)))
                    bullet_center_y = player.center_y + \
                        (player.height / 2 *
                            math.sin(math.radians(self.weapon_angle + self.init_angle)))

                    # Generate random pattern
                    random_angle = random.uniform(-(self.bullet_spread/2),
                                                  (self.bullet_spread/2))
                    random_speed = random.uniform(
                        -self.bullet_speed_spread + self.bullet_speed, self.bullet_speed_spread + self.bullet_speed)

                    # Calculate angle from bullet to mouse location
                    calc_angle = calculate_angle(
                        bullet_center_x, bullet_center_y, self.last_mouse_x + C.GUI["Crosshair"]["offset_x"], self.last_mouse_y + C.GUI["Crosshair"]["offset_y"])
                    if self.last_mouse_x + C.GUI["Crosshair"]["offset_x"] < bullet_center_x:
                        calc_angle = calc_angle + self.init_angle
                    else:
                        calc_angle = calc_angle - self.init_angle
                    self.bullet_angle = calc_angle + random_angle

                    # Calculate bullet speed
                    speed_x = random_speed * math.cos(math.radians(self.bullet_angle +
                                                                   self.init_angle))
                    speed_y = random_speed * math.sin(math.radians(self.bullet_angle +
                                                                   self.init_angle))

                    # Instantiate bullet
                    bullet = Bullet("Detailed", speed_x, speed_y, self.bullet_texture_list,
                                    self.bullet_angle + self.init_angle, self.bullet_damage, scale=self.bullet_scale)

                    # Set bullet location
                    bullet.center_x = bullet_center_x
                    bullet.center_y = bullet_center_y

                    # Add to bullet sprite list
                    Bullet.friendly_bullet_list.append(bullet)

                # Play random weapon shoot sfx
                Audio.play_rand_sound(self.sfx_single_shot_list)

                # Start reload if ammo depleted
                if self.cur_ammo <= 0:
                    self.is_reloading = True

                self.shoot_timer = 0
            else:
                # Reload weapon
                self.reload_timer += delta_time
                if self.reload_timer >= self.reload_time:
                    self.reload_weapon()
                # TODO: Play empty weapon sfx
        else:
            self.shoot_timer += delta_time
            if self.shoot_timer >= self.shoot_time:
                self.can_shoot = True
                self.shoot_timer = 0

    def swap_weapon(self, weapon_name: str):
        self.set_weapon(weapon_name)

    def set_weapon(self, weapon_name: str):
        """Handle weapon setting"""

        found_weapon = False
        for weapon in C.WEAPON_LIST:
            if weapon_name in weapon["name"]:
                found_weapon = True

                # Set weapon name
                self.weapon_name = weapon["name"]
                self.img_name = weapon["img_name"]

                # Load weapon texture
                self.texture = arcade.load_texture(
                    f"resources/images/weapon/" + self.img_name + "/" + self.img_name + ".png", weapon["center_x"], weapon["center_y"], weapon["width"], weapon["height"])
                self.scale = weapon["scale"] * C.WEAPON_SCALE * global_scale()

                # Load animated bullet textures
                self.bullet_texture_list = []
                for i in range(1, weapon["bullet_texture_amount"] + 1):
                    self.bullet_texture_list.append(arcade.load_texture(
                        f"resources/images/weapon/" + self.img_name + "/bullet/" + str(i) + ".png", hit_box_algorithm="Detailed"))

                # Set GUI location
                self.center_x = C.GUI["Weapon"]["center_x"] * global_scale()
                self.center_y = C.GUI["Weapon"]["center_y"] * global_scale()

                # Set Gun attributes
                self.init_angle = weapon["init_angle"]
                self.fire_mode = weapon["fire_mode"]
                self.max_ammo = weapon["max_ammo"]
                self.cur_ammo = self.tracked_ammo[self.weapon_name]
                self.bullet_amount = weapon["bullet_amount"]
                self.bullet_spread = weapon["bullet_spread"]
                self.bullet_speed = weapon["bullet_speed"]
                self.bullet_speed_spread = weapon["bullet_speed_spread"]
                self.bullet_damage = weapon["bullet_damage"]
                self.bullet_scale = weapon["bullet_scale"]
                self.can_shoot = True
                self.shoot_time = weapon["shoot_time"]
                self.shoot_timer = 0
                self.reload_time = weapon["reload_time"]
                self.reload_timer = 0
                self.reload_rate = weapon["reload_rate"]
                if self.cur_ammo <= 0:
                    self.is_reloading = True
                else:
                    self.is_reloading = False

                # Find & set single shot sfx
                for i in range(0, len(Audio.sfx_player_weapon_shoot_list)):
                    if Audio.sfx_player_weapon_shoot_list[i]["weapon_name"] == self.weapon_name:
                        self.sfx_single_shot_list = Audio.sfx_player_weapon_shoot_list[i]["sound"]
                        break

                # Break out of loop if weapon found
                break
        if not found_weapon:
            print("Error: Weapon not found.")

    def on_mouse_motion(self, x, y, _dx, _dy):
        """ Called whenever mouse is moved """
        self.last_mouse_x = x
        self.last_mouse_y = y
