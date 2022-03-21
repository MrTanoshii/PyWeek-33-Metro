from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SPRITE_PLAYER_INIT_ANGLE
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, level1, SPRITE_PLAYER_INIT_ANGLE, MOVE_DIRECTION
from webbrowser import BackgroundBrowser
from bullet import Bullet
from bg import BackGround
from player import Player
from enemy import Enemy
from gold import Gold

import arcade
import random
<< << << < HEAD
== == == =
>>>>>> > e312f0e(refactor: bg spawn & update handled by class)


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__()

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.player_list = arcade.SpriteList()

        # Separate variable that holds the player sprite
        self.player = None
        self.bg = None

        # What key is pressed down?
        self.left_key_down = False
        self.right_key_down = False
        self.up_key_down = False
        self.down_key_down = False
        self.space_down = False

        # GUI
        self.score = 0
        self.gui_camera = None

        self.setup_complete = False

        # Player shoot
        self.shoot_pressed = False

        arcade.set_background_color(arcade.csscolor.DARK_GREEN)

    def setup(self):
        """ Set up everything with the game """

        # self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Create player sprite
        self.player = Player(hit_box_algorithm="Detailed")

        # Set player location
        self.player.center_x = SCREEN_WIDTH * .1
        self.player.center_y = SCREEN_HEIGHT * .5

        # Rotate player to face to the right
        self.player.angle = SPRITE_PLAYER_INIT_ANGLE

        # Add to player sprite list
        self.player_list.append(self.player)

        # Create BG sprite
        self.bg = BackGround()
        self.bg.center_x = self.bg.width/2
        self.bg.center_y = SCREEN_HEIGHT/2
        BackGround.bg_list.append(self.bg)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        BackGround.bg_list.draw()
        Gold.gold_list.draw()
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

        # GUI - Player HP
        arcade.draw_text(
            f"Ammo : {self.player.cur_ammo} \ {self.player.max_ammo}",
            (SCREEN_WIDTH / 5) + 500,
            SCREEN_HEIGHT - 50,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

    # Run every tick
    # TODO: How to limit fps? Does computing power affect the speed?

    def on_update(self, delta_time):
        if random.randint(0, 200) == 1:
            BackGround.spawn()
            Enemy.spawn_enemy()

        BackGround.update(delta_time)

        player_move_dir = None
        if self.left_key_down:
            if self.up_key_down:
                player_move_dir = MOVE_DIRECTION.TOP_LEFT
            elif self.down_key_down:
                player_move_dir = MOVE_DIRECTION.BOTTOM_LEFT
            else:
                player_move_dir = MOVE_DIRECTION.LEFT
        elif self.right_key_down:
            if self.up_key_down:
                player_move_dir = MOVE_DIRECTION.TOP_RIGHT
            elif self.down_key_down:
                player_move_dir = MOVE_DIRECTION.BOTTOM_RIGHT
            else:
                player_move_dir = MOVE_DIRECTION.RIGHT
        elif self.up_key_down:
            player_move_dir = MOVE_DIRECTION.TOP
        elif self.down_key_down:
            player_move_dir = MOVE_DIRECTION.BOTTOM
        else:
            player_move_dir = MOVE_DIRECTION.IDLE

        self.player.update(player_move_dir)
        self.check_collisions()

        Enemy.update()

        # Player shoot
        if self.player.can_shoot:
            if self.shoot_pressed:
                self.player.can_shoot = False
                self.player.shoot(Bullet.friendly_bullet_list)
        else:
            if self.player.is_reloading:
                self.player.reload_timer += delta_time
                if self.player.reload_timer >= self.player.reload_speed:
                    self.player.reload_weapon()
            else:
                self.player.shoot_timer += delta_time
                if self.player.shoot_timer >= self.player.shoot_speed:
                    self.player.can_shoot = True
                    self.player.shoot_timer = 0

    def on_mouse_motion(self, x, y, dx, dy):
        """Called whenever mouse is moved."""
        self.player.follow_mouse(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        """Called whenever a mouse key is pressed."""
        # Mouse Left Click
        if button == arcade.MOUSE_BUTTON_LEFT:
            for enemy in Enemy.enemy_list:
                enemy.shoot(Bullet.enemy_bullet_list)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = True
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_key_down = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_key_down = True
        elif key == arcade.key.SPACE:
            self.space_down = True
            self.shoot_pressed = True
        elif key == arcade.key.E:
            Enemy.spawn_enemy()
        elif key == arcade.key.T:
            BackGround.spawn()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = False
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_key_down = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_key_down = False
        elif key == arcade.key.SPACE:
            self.space_down = False
            self.shoot_pressed = False

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
            for enemy in enemy_hit_list:

                # Remove bullet damage from enemy HP
                enemy.HP -= bullet.damage_value

                # Remove bullet
                Bullet.despawn(bullet)

                # if HP 0, destroy enemy
                if enemy.HP <= 0:
                    Enemy.despawn(enemy)
                    # Play a sound
                    arcade.play_sound(enemy.audio_destroyed)
                    self.score += 1
                else:
                    # Play a sound
                    arcade.play_sound(enemy.audio_hit)
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
                Bullet.despawn(bullet)
        # Check enemy collision with player
        enemy_collision_list = arcade.check_for_collision_with_list(
            self.player, Enemy.enemy_list)
        for enemy in enemy_collision_list:
            Enemy.despawn(enemy)
            arcade.play_sound(enemy.audio_destroyed)
            self.player.take_damage(enemy)

    def on_show(self):
        self.setup()
