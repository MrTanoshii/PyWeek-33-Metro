import constants as C
import arcade
from audio import Audio


bullet_texture_lists_list = {}


# Create example bullet texture lists
def init_bullet_texture_lists():
    # for weapon in C.WEAPON_LIST:

    #     # Set weapon name
    #     weapon_name = weapon["name"]

    #     # Load animated bullet textures
    #     bullet_texture_list = []
    #     for i in range(1, weapon["bullet_texture_amount"] + 1):
    #         bullet_texture_list.append(arcade.load_texture(
    #             f"resources/images/weapon/" + weapon["img_name"] + "/bullet/" + str(i) + ".png",
    #             hit_box_algorithm="Simple"))
    #     bullet_texture_lists_list[weapon_name] = bullet_texture_list

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
    reload_weapon()
        Reloads the current weapon
    swap_weapon(weapon_name: str)
        Swap the current weapon
    set_weapon(weapon_name: str)
        Set the current weapon
    """

    def __init__(self):
        # Inherit parent class
        super().__init__()

        # Set default weapon
        self.set_weapon("Rifle")

        # Set sound
        self.sound = None

    def reload_weapon(self):
        """ Reloads the current weapon """
        # Increment ammo count
        self.cur_ammo += self.reload_rate

        # Allow shooting if ammo present
        self.can_shoot = True

        self.reload_timer = 0

        # TODO: Play weapon reload sfx

        # Finish reloading
        if self.cur_ammo >= self.max_ammo:
            # Do not allow over-reload
            self.cur_ammo = self.max_ammo

            self.is_reloading = False

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
                self.scale = weapon["scale"]

                # Load animated bullet textures
                self.bullet_texture_list = []
                for i in range(1, weapon["bullet_texture_amount"] + 1):
                    self.bullet_texture_list.append(arcade.load_texture(
                        f"resources/images/weapon/" + self.img_name + "/bullet/" + str(i) + ".png", hit_box_algorithm="Detailed"))

                # Set GUI location
                self.center_x = C.GUI["Weapon"]["center_x"]
                self.center_y = C.GUI["Weapon"]["center_y"]

                # Set Gun attributes
                self.fire_mode = weapon["fire_mode"]
                self.fire_type = weapon["fire_type"]
                self.max_ammo = weapon["max_ammo"]
                self.cur_ammo = self.max_ammo
                self.bullet_speed = weapon["bullet_speed"]
                self.bullet_damage = weapon["bullet_damage"]
                self.bullet_scale = weapon["bullet_scale"]
                self.can_shoot = True
                self.shoot_time = weapon["shoot_time"]
                self.shoot_timer = 0
                self.reload_time = weapon["reload_time"]
                self.reload_timer = 0
                self.reload_rate = weapon["reload_rate"]
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
