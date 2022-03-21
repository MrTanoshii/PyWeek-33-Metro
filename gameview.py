from bullet import Bullet
from bg import BackGround
from player import Player
from enemy import Enemy

import arcade
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, level1


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__()

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.player_list = None
        self.bg_list = None

        # Separate variable that holds the player sprite
        self.player = None
        self.bg = None

        # What key is pressed down?
        self.left_key_down = False
        self.right_key_down = False
        self.space_down = False

        # GUI
        self.score = 0
        self.gui_camera = None

        self.setup_complete = False

        arcade.set_background_color(arcade.csscolor.DARK_GREEN)

    def setup(self):
        """ Set up everything with the game """

        # self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.bg_list = arcade.SpriteList()

        # Create player sprite
        self.player = Player(hit_box_algorithm="Detailed")

        # Set player location
        self.player.center_x = SCREEN_WIDTH * .1
        self.player.center_y = SCREEN_HEIGHT * .5

        # Turn the player -90 degree
        self.player.angle = -90

        # Add to player sprite list
        self.player_list.append(self.player)

        # Create BG sprite
        self.bg = BackGround()
        self.bg.center_x = self.bg.width/2
        self.bg.center_y = SCREEN_HEIGHT/2
        self.bg_list.append(self.bg)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        self.bg_list.draw()
        self.player_list.draw()
        Enemy.enemy_list.draw()
        Bullet.friendly_bullet_list.draw()
        Bullet.enemy_bullet_list.draw()

        # GUI - Score
        arcade.draw_text(
            f"Score : {self.score}",
            SCREEN_WIDTH / 5,
            SCREEN_HEIGHT - 50,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

        # GUI - Player HP
        arcade.draw_text(
            f"HP : {self.player.cur_health}",
            (SCREEN_WIDTH / 5) + 200,
            SCREEN_HEIGHT - 50,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

    # Run every tick
    # TODO: How to limit fps? Does computing power affect the speed?

    def on_update(self, delta_time: float):
        if random.randint(0, 200) == 1:
            self.spawn_bg()
            Enemy.spawn_enemy()

        for bg in self.bg_list:
            bg.center_x += bg.SPEED
            if bg.asset == "bg-1.png":
                if bg.center_x - bg.width / 2 < - 220 - bg.SPEED:
                    bg.center_x = bg.width/2
            else:
                if bg.center_x + bg.width < 0:
                    bg.remove_from_sprite_lists()

        # MOVE PLAYER: Add player y coordinate the current speed
        self.player.center_y += self.player.current_speed
        self.check_collisions()

        Enemy.update()

    def on_mouse_press(self, x, y, button, modifiers):
        """Called whenever a mouse key is pressed."""
        # Mouse Left Click
        if button == arcade.MOUSE_BUTTON_LEFT:
            for enemy in Enemy.enemy_list:
                enemy.shoot(Bullet.enemy_bullet_list)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        # Left
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = True
            self.update_player_speed()

        # Right
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = True
            self.update_player_speed()

        # Space
        elif key == arcade.key.SPACE:
            self.space_down = True
            self.player.shoot(Bullet.friendly_bullet_list)

        # E
        elif key == arcade.key.E:
            Enemy.spawn_enemy()

        # T
        elif key == arcade.key.T:
            self.spawn_bg()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = False
            self.update_player_speed()

    def update_player_speed(self):
        self.player.current_speed = 0

        # D pressed
        if self.left_key_down and not self.right_key_down:
            self.player.current_speed = self.player.SPEED
        # A pressed
        elif self.right_key_down and not self.left_key_down:
            self.player.current_speed = -self.player.SPEED

    def spawn_bg(self):
        # Create BG sprite
        assets = level1.assets
        self.bg = BackGround(asset=random.choice(
            assets), size=random.uniform(.9, 1.1))
        self.bg.center_x = SCREEN_WIDTH + self.bg.width / 2
        if random.randint(0, 1) == 1:
            self.bg.center_y = SCREEN_HEIGHT + \
                self.bg.height / 2 - random.uniform(50, 75)
        else:
            self.bg.center_y = self.bg.height / 2 + random.uniform(-50, 50)
        self.bg_list.append(self.bg)

    def check_collisions(self):
        """Check for collisions and calculate score"""
        # Check friendly bullet collisions
        for bullet in Bullet.friendly_bullet_list:
            # Move all Bullets Forwards
            bullet.center_x += bullet.speed_x
            bullet.center_y += bullet.speed_y

            """ Collision """
            # Add enemy to list, if collided with bullet
            enemy_hit_list = arcade.check_for_collision_with_list(
                bullet, Enemy.enemy_list
            )

            # Loop through each enemy we hit (if any) and remove it
            for _enemy in enemy_hit_list:

                # Remove bullet damage from enemy HP
                _enemy.HP -= bullet.damage_value

                # Remove bullet
                bullet.remove_from_sprite_lists()

                # if HP 0, destroy enemy
                if _enemy.HP <= 0:
                    _enemy.remove_from_sprite_lists()
                    # Play a sound
                    arcade.play_sound(_enemy.audio_destroyed)
                    self.score += 1
                else:
                    # Play a sound
                    arcade.play_sound(_enemy.audio_hit)
        # Check enemy bullet collisions
        for bullet in Bullet.enemy_bullet_list:
            # Move all Bullets Forwards
            bullet.center_x += bullet.speed_x
            bullet.center_y += bullet.speed_y

            # Loop through each coin we hit (if any) and remove it
            if arcade.check_for_collision(self.player, bullet):
                # Apply damage to player
                self.player.take_damage(bullet)
                # Remove bullet
                bullet.remove_from_sprite_lists()
        # Check enemy collision with player
            enemy_collision_list = arcade.check_for_collision_with_list(
                self.player, Enemy.enemy_list)
            for enemy in enemy_collision_list:
                enemy.remove_from_sprite_lists()
                arcade.play_sound(enemy.audio_destroyed)
                self.player.take_damage(enemy)

    def on_show(self):
        self.setup()
