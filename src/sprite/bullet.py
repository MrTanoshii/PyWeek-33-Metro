import arcade

import src.const as C

import src.lib as lib


class Bullet(arcade.Sprite):
    """
    Bullet Sprite

    ...

    Attributes
    ----------
    friendly_bullet_list : arcade.SpriteList
        List of friendly bullet sprites
    enemy_bullet_list: arcade.SpriteList
        List of enemy bullet sprites

    Class Methods
    -------------
    update()
        Update the bullet

    Methods
    -------
    update_animation(delta_time: float)
        Update the bullet animation
    despawn()
        Remove the bullet
    update_animation(delta_time: float)
        Update the animated texture
    """

    # SpriteList class attribute
    friendly_bullet_list = arcade.SpriteList()
    enemy_bullet_list = arcade.SpriteList()

    # Volume class attribute
    audio_volume = C.AUDIO.MASTER_VOLUME

    def __init__(self, hit_box_algorithm, speed_x, speed_y, texture_list=None,
                 angle=0, damage_value=1, scale=C.BULLET_SCALE):
        # Inherit parent class
        super().__init__()

        # Speed
        self.speed_x = speed_x
        self.speed_y = speed_y

        # Damage
        self.damage_value = damage_value

        # Angle
        self.angle = angle

        # Set our scale
        self.scale = scale * lib.global_scale()

        base_path = "src/resources/"

        # Load & set bullet texture
        # TODO: Remove regular non animated texture loading when enemies have their own bullets
        if texture_list is None:
            self.texture = arcade.load_texture(
                f"{base_path}images/bullet.png", hit_box_algorithm=hit_box_algorithm)
        else:
            self.texture_list = texture_list
            self.texture = self.texture_list[0]
        self.current_texture: float = 0
        self.animation_speed: float = 1

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

    @classmethod
    def update(cls):

        # Cycle through player bullets
        for bullet in cls.friendly_bullet_list:
            # Delete bullets that are off-screen
            if abs(bullet.center_x - (bullet.width * lib.global_scale() / 2)) \
                - (C.SCREEN_WIDTH / 2 * lib.global_scale()) \
                > C.SCREEN_WIDTH / 2 * lib.global_scale() \
                    or abs(bullet.center_y - (bullet.height * lib.global_scale() / 2)) \
                    > C.SCREEN_HEIGHT * lib.global_scale():
                cls.friendly_bullet_list.remove(bullet)

        # Cycle through enemy bullets
        for bullet in cls.enemy_bullet_list:
            # Delete bullets that are off-screen
            if abs(bullet.center_x - (bullet.width * lib.global_scale() / 2)) \
                > C.SCREEN_WIDTH * 1.5 * lib.global_scale() or abs(
                    bullet.center_y - (bullet.height * lib.global_scale() / 2)) \
                    > C.SCREEN_HEIGHT * lib.global_scale():
                cls.enemy_bullet_list.remove(bullet)

    def update_animation(self, delta_time: float):
        """ Update the animated texture """

        self.current_texture = lib.find_next_texture(
            delta_time, self.current_texture, self.texture_list)
        self.texture = self.texture_list[int(self.current_texture)]

    def despawn(self):
        if self in Bullet.friendly_bullet_list:
            Bullet.friendly_bullet_list.remove(self)
        elif self in Bullet.enemy_bullet_list:
            Bullet.enemy_bullet_list.remove(self)
        self.remove_from_sprite_lists()
