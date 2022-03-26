import arcade
import os.path
import random
import math
import const.constants as C
from bullet import Bullet
from const.enemy_weapon import ENEMY_LOGIC
from gold import Gold
from player import Player
from audio import Audio
import weapon
from lib import global_scale, calculate_angle


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
    update(delta_time: float)
        Update the enemy
    preload()
        Preload the enemy resources

    Methods
    -------
    despawn()
        Remove the enemy
    shoot()
        Handle enemy shooting
    """

    # SpriteList class attribute
    enemy_list = arcade.SpriteList()

    def __init__(self, hit_box_algorithm, level, scale=0.8):
        # Inherit parent class

        super().__init__()

        enemy_style = C.MAP_MONUMENTS_LIST[level-1]["enemy"]

        # load enemy configs
        self.config = enemy_style
        self.name = self.config["name"]
        self.barrel_location = self.config["barrel"]

        # Speed
        self.speed = self.config["speed"]
        self.current_speed = 0

        # Health
        self.HP = self.config["health"]

        # Set Weapon
        for weapon in C.ENEMY_WEAPON_LIST:
            if weapon["name"] == self.name:
                self.weapon = weapon["name"]
                self.weapon_init_angle = weapon["init_angle"]
                self.damage_value = weapon["damage_value"]
                self.shooting_speed = weapon["shoot_time"]
                self.shoot_constant = weapon["shoot_constant"]
                self.shoot_probability = weapon["shoot_probability"]
                self.shoot_max_angle = weapon["shoot_max_angle"]
                self.bullet_damage = weapon["bullet_damage"]
                self.bullet_scale = weapon["bullet_scale"] * global_scale()
                self.bullet_amount = weapon["bullet_amount"]
                self.bullet_spread = weapon["bullet_spread"] * global_scale()
                self.bullet_speed = weapon["bullet_speed"] * global_scale()
                self.bullet_speed_spread = weapon["bullet_speed_spread"] * \
                    global_scale()
                break
        self.can_shoot = True
        self.shooting_timer = 0

        # Ballistics
        self.bullet_center_x = 0
        self.bullet_center_y = 0
        self.random_angle = 0
        self.random_speed = 0

        """ Load Assets """
        base_path = f"resources/images/assets/enemies/{self.name}/"

        # Load texture
        self.texture_list = []
        file_name_list = os.listdir(f"{base_path}animation/")
        file_name_list = sorted(
            file_name_list, key=lambda x: int(x.split('.')[0]))
        for filename in file_name_list:
            self.texture_list.append(
                arcade.load_texture(f"{base_path}animation/{filename}", hit_box_algorithm=hit_box_algorithm))

        self.cur_texture = 0

        self.animation_speed = self.config["animation_speed"]

        # Set our scale
        self.scale = scale * global_scale()

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
        enemy.center_x = (C.SCREEN_WIDTH + enemy.width) * global_scale()
        enemy.center_y = (C.SCREEN_HEIGHT // 2 +
                          random.uniform(-C.SCREEN_HEIGHT/3.25, C.SCREEN_HEIGHT/3.25)) * global_scale()

        # Turn the enemy 90 degree
        enemy.angle = 0

        # Add to player sprite list
        cls.enemy_list.append(enemy)

    def despawn(self, death):
        # Play enemy death sfx

        if death == C.DEATH.KILLED or death == C.DEATH.COLLISION:
            Audio.play_rand_sound(self.sfx_death_list)

        if death == C.DEATH.KILLED:
            Gold.spawn(self.center_x, self.center_y)
        self.remove_from_sprite_lists()

    @classmethod
    def update(cls, delta_time: float):
        # Cycle trough all enemies
        for enemy in cls.enemy_list:
            # Move all Enemies Forwards
            enemy.center_x += enemy.speed * global_scale()

            # Check if enemy is in view, if not delete it
            if enemy.center_x + enemy.width < 0:
                cls.despawn(enemy, C.DEATH.OOB)
            else:
                enemy.maybe_shoot(delta_time)

    @classmethod
    def preload(cls, level):
        Enemy.spawn_enemy(level)

    def calculate_bullet_ballistic(self, aim_type) -> dict:
        """ Calculate the weapon ballistics and return as a dict """

        angle = 0
        speed_x = 0
        speed_y = 0

        if aim_type == "aim_player":
            # NOTE: Only last player in list will be used
            for player in Player.player_list:
                calc_angle = calculate_angle(
                    self.bullet_center_x, self.bullet_center_y, player.center_x, player.center_y)

                angle = self.weapon_init_angle + calc_angle + self.random_angle
                speed_x = self.random_speed * math.cos(math.radians(angle))
                speed_y = self.random_speed * math.sin(math.radians(angle))

        elif aim_type == "aim_straight":
            angle = self.weapon_init_angle + self.random_angle
            speed_x = self.random_speed * math.cos(math.radians(angle))
            speed_y = self.random_speed * math.sin(math.radians(angle))

        elif aim_type == "aim_random":
            random_point_x = 0
            if self.bullet_center_x > 0:
                random_point_x = random.randint(
                    0, int(self.bullet_center_x))
            random_point_y = random.randint(
                int((C.SCREEN_HEIGHT * .15 * global_scale())), int(C.SCREEN_HEIGHT * .85 * global_scale()))

            calc_angle = calculate_angle(
                self.bullet_center_x, self.bullet_center_y, random_point_x, random_point_y)

            angle = self.weapon_init_angle + calc_angle + self.random_angle
            speed_x = self.random_speed * math.cos(math.radians(angle))
            speed_y = self.random_speed * math.sin(math.radians(angle))

        ballistic_dict = {
            "angle": angle,
            "speed_x": speed_x,
            "speed_y": speed_y
        }

        return ballistic_dict

    def maybe_shoot(self, delta_time: float):
        """ Handle probable enemy shooting """

        # Calculate bullet position
        self.bullet_center_x = self.center_x - \
            (self.width * global_scale() / 2) + \
            self.barrel_location[0] * global_scale()
        self.bullet_center_y = self.center_y - \
            (self.height * global_scale() / 2) + \
            self.barrel_location[1] * global_scale()

        # NOTE: Only last player in list will be used
        if self.bullet_center_x <= Player.player_list[0].center_x:
            self.can_shoot = False
        elif self.can_shoot:
            self.can_shoot = False

            if self.shoot_constant == True or random.random() <= self.shoot_probability:
                # Generate random pattern
                self.random_angle = random.uniform(-(self.bullet_spread/2),
                                                   (self.bullet_spread/2))
                self.random_speed = random.uniform(
                    -self.bullet_speed_spread + self.bullet_speed, self.bullet_speed_spread + self.bullet_speed)

                probability = random.random()
                speed_x = 0
                speed_y = 0
                angle = 0
                # Ballistics at player
                if probability <= C.ENEMY_LOGIC["prob_aim_player"]:
                    if C.DEBUG.ENEMY_SHOOT:
                        print("Enemy aiming at player")
                    ballistic_dict = self.calculate_bullet_ballistic(
                        "aim_player")
                    speed_x = ballistic_dict["speed_x"]
                    speed_y = ballistic_dict["speed_y"]
                    angle = ballistic_dict["angle"]

                # Ballistics straight
                elif probability <= C.ENEMY_LOGIC["prob_aim_player"] + C.ENEMY_LOGIC["prob_aim_straight"]:
                    if C.DEBUG.ENEMY_SHOOT:
                        print("Enemy aiming straight")
                    ballistic_dict = self.calculate_bullet_ballistic(
                        "aim_straight")
                    speed_x = ballistic_dict["speed_x"]
                    speed_y = ballistic_dict["speed_y"]
                    angle = ballistic_dict["angle"]

                # Ballistics random
                elif probability <= C.ENEMY_LOGIC["prob_aim_player"] + C.ENEMY_LOGIC["prob_aim_straight"] + C.ENEMY_LOGIC["prob_aim_random"]:
                    if C.DEBUG.ENEMY_SHOOT:
                        print("Enemy aiming at random")
                    ballistic_dict = self.calculate_bullet_ballistic(
                        "aim_random")
                    speed_x = ballistic_dict["speed_x"]
                    speed_y = ballistic_dict["speed_y"]
                    angle = ballistic_dict["angle"]
                else:
                    pass

                # Ballistics straight if shooting angle too high
                if angle > self.weapon_init_angle + (self.shoot_max_angle / 2) or angle < self.weapon_init_angle - (self.shoot_max_angle / 2):
                    ballistic_dict = self.calculate_bullet_ballistic(
                        "aim_straight")
                    speed_x = ballistic_dict["speed_x"]
                    speed_y = ballistic_dict["speed_y"]
                    angle = ballistic_dict["angle"]

                if C.DEBUG.ENEMY_SHOOT:
                    print(speed_x, speed_y, angle)
                # Instantiate bullet
                bullet = Bullet(
                    hit_box_algorithm="Simple",
                    speed_x=speed_x,
                    speed_y=speed_y,
                    texture_list=weapon.bullet_texture_lists_list[self.weapon],
                    angle=angle,
                    damage_value=self.bullet_damage,
                    scale=self.bullet_scale)

                # Set bullet location
                bullet.position = (self.bullet_center_x, self.bullet_center_y)

                # Turn the bullet -90 degree
                # bullet.angle = 0

                # Add to bullet sprite list
                Bullet.enemy_bullet_list.append(bullet)

                # Play weapon shoot sfx
                Audio.play_rand_sound(self.sfx_single_shot_list)
        else:
            self.shooting_timer += delta_time

            if self.shooting_timer >= self.shooting_speed:
                self.can_shoot = True
                self.shooting_timer = 0

    def shoot(self):
        """Handle enemy shooting"""

        # Generate random pattern
        random_angle = random.uniform(-(self.bullet_spread/2),
                                      (self.bullet_spread/2))
        random_speed = random.uniform(
            -self.bullet_speed_spread + self.bullet_speed, self.bullet_speed_spread + self.bullet_speed)

        # Instantiate bullet
        bullet = Bullet(
            hit_box_algorithm="Simple",
            speed_x=random_speed * math.cos(math.radians(random_angle +
                                                         self.weapon_init_angle)),
            speed_y=random_speed * math.sin(math.radians(random_angle +
                                                         self.weapon_init_angle)),
            texture_list=weapon.bullet_texture_lists_list[self.weapon],
            angle=self.weapon_init_angle + random_angle,
            damage_value=self.bullet_damage,
            scale=self.bullet_scale)

        # Set bullet location
        bullet.position = ((self.center_x - (self.width * global_scale() / 2) +
                           self.barrel_location[0] * global_scale()), (self.center_y - (self.height * global_scale() / 2) + self.barrel_location[1] * global_scale()))

        # Turn the bullet -90 degree
        # bullet.angle = 0

        # Add to bullet sprite list
        Bullet.enemy_bullet_list.append(bullet)

        # Play weapon shoot sfx
        Audio.play_rand_sound(self.sfx_single_shot_list)

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += delta_time * self.animation_speed
        if self.cur_texture > len(self.texture_list) - 1:
            self.cur_texture = 0
        self.texture = self.texture_list[int(self.cur_texture)]
