import constants as C
import arcade


class Weapon(arcade.Sprite):
    def __init__(self):
        # Inherit parent class
        super().__init__()

        # Set default weapon
        self.set_weapon("Rifle")

    def reload_weapon(self):
        """Handle weapon reload"""
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

    def swap_weapon(self, weapon_name):
        self.set_weapon(weapon_name)

    def set_weapon(self, weapon_name):
        """Handle weapon setting"""

        found_weapon = False
        for weapon in C.WEAPON_LIST:
            if weapon_name in weapon["name"]:
                found_weapon = True

                # Set weapon name
                self.weapon_name = weapon["name"]

                # Load weapon texture
                self.texture = arcade.load_texture(
                    f"resources/images/weapon/" + weapon["img_name"] + "/" + weapon["img_name"] + ".png", weapon["center_x"], weapon["center_y"], weapon["width"], weapon["height"])
                self.scale = weapon["scale"]

                # Load animated bullet textures
                self.bullet_texture_list = []
                for i in range(1, weapon["bullet_texture_amount"] + 1):
                    self.bullet_texture_list.append(arcade.load_texture(
                        f"resources/images/weapon/" + weapon["img_name"] + "/bullet/" + str(i) + ".png", hit_box_algorithm="Detailed"))

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

                # Break out of loop if weapon found
                break

        if not found_weapon:
            print("Error: Weapon not found.")
