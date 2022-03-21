import arcade
from constants import BULLET_SCALING, SCREEN_WIDTH
from enemy import Enemy


class Bullet(arcade.Sprite):
    """ Player Sprite """

    bullet_list = arcade.SpriteList()

    def __init__(self, hit_box_algorithm):
        # Let parent initialize
        super().__init__()

        self.current_speed = 0
        self.SPEED = 20
        self.DAMAGE = 2

        # Set our scale
        self.scale = BULLET_SCALING

        # load player texture
        base_path = "resources/"
        self.idle_texture_pair = arcade.load_texture_pair(f"{base_path}images/bullet.png", hit_box_algorithm=hit_box_algorithm)
        # Load sounds
        self.audio_gunshot = arcade.load_sound(f"{base_path}audio/gunshot.wav")

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used.
        self.hit_box = self.texture.hit_box_points

    @classmethod
    def update(cls):
        # Cycle through all bullets
        score = 0
        for bullet in cls.bullet_list:

            # Move all Bullets Forwards
            bullet.center_x += bullet.SPEED

            """ Collision """
            # Add enemy to list, if collided with bullet
            enemy_hit_list = arcade.check_for_collision_with_list(
                bullet, Enemy.enemy_list
            )

            # Loop through each coin we hit (if any) and remove it
            for _enemy in enemy_hit_list:

                # Remove bullet damage from enemy HP
                _enemy.HIT_POINTS -= bullet.DAMAGE

                # Remove bullet
                bullet.remove_from_sprite_lists()

                # if HP 0, destroy enemy
                if _enemy.HIT_POINTS <= 0:
                    _enemy.remove_from_sprite_lists()
                    # Play a sound
                    arcade.play_sound(_enemy.audio_destroyed)
                    score += 1
                else:
                    # Play a sound
                    arcade.play_sound(_enemy.audio_hit)

            """ Remove off screen bullets """

            # Check if bullet is in view, if not delete it
            if bullet.center_x - bullet.width / 2 > SCREEN_WIDTH:
                cls.bullet_list.remove(bullet)
        return score
