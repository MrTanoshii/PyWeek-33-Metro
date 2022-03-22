import pause_menu_view
from bullet import Bullet
from bg import BackGround
from player import Player
from enemy import Enemy
from gold import Gold
from tracker import Tracker
from settings import Settings
import constants as C

import arcade
import mapview
from pause_menu_view import PauseMenuView
import random


class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__()

        self.level = Player.current_level

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.

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
        self.gui_camera = None
        self.setup_complete = False

        # Player shoot
        self.shoot_pressed = False

        arcade.set_background_color(arcade.csscolor.GREEN)

    def setup(self):
        """ Set up everything with the game """

        # self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Create player sprite
        self.player = Player(hit_box_algorithm="Simple")

        # Rotate player to face to the right

        # Add to player sprite list

        # Create BG sprite
        self.bg = BackGround(self.level)
        self.bg.center_x = self.bg.width/2
        self.bg.center_y = C.SCREEN_HEIGHT/2
        BackGround.bg_list.append(self.bg)
        self.setup_complete = True

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        BackGround.bg_list.draw()
        Gold.gold_list.draw()
        Player.player_list.draw()
        Player.weapon.draw()
        Enemy.enemy_list.draw()
        Bullet.friendly_bullet_list.draw()
        Bullet.enemy_bullet_list.draw()

        # Update animations
        Bullet.friendly_bullet_list.update_animation()
        Bullet.enemy_bullet_list.update_animation()

        # GUI - Score
        arcade.draw_text(
            f"Score : {Tracker.score}",
            C.SCREEN_WIDTH / 5,
            C.SCREEN_HEIGHT - 50,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

        # GUI - Gold
        arcade.draw_text(
            f"Gold : {Tracker.gold}",
            C.SCREEN_WIDTH / 5,
            C.SCREEN_HEIGHT - 150,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

        # GUI - Player HP
        arcade.draw_text(
            f"HP : {self.player.cur_health}",
            (C.SCREEN_WIDTH / 5) + 200,
            C.SCREEN_HEIGHT - 50,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

        # GUI - Player Ammo
        arcade.draw_text(
            f"Ammo : {self.player.weapon.cur_ammo} \ {self.player.weapon.max_ammo}",
            (C.SCREEN_WIDTH / 5) + 500,
            C.SCREEN_HEIGHT - 50,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

    # Run every tick
    # TODO: How to limit fps? Does computing power affect the speed?

    def on_update(self, delta_time):
        if random.randint(0, 200) == 1:
            Enemy.spawn_enemy()

        BackGround.update(delta_time)
        Gold.update(delta_time)

        movement_key_pressed = {
            "left": self.left_key_down,
            "up": self.up_key_down,
            "down": self.down_key_down,
            "right": self.right_key_down
        }
        self.player.update(delta_time, movement_key_pressed,
                           self.shoot_pressed)
        self.check_collisions()

        Enemy.update()

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

        # Movement | WASD + Arrow keys
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = True
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_key_down = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_key_down = True

        # Shoot | Spacebar
        elif key == arcade.key.SPACE:
            self.space_down = True
            self.shoot_pressed = True

        # Weapon swap | 1-3
        elif key == arcade.key.KEY_1 or arcade.key.KEY_2 or arcade.key.KEY_3:
            requested_weapon = ""
            # 1 - Rifle
            if key == arcade.key.KEY_1:
                requested_weapon = "Rifle"
            # 2 - Shotgun
            elif key == arcade.key.KEY_2:
                requested_weapon = "Shotgun"
            # 3 - RPG
            elif key == arcade.key.KEY_3:
                requested_weapon = "RPG"

            # Swap weapon
            if Player.weapon.weapon_name != requested_weapon:
                Player.weapon.swap_weapon(requested_weapon)

        # E
        elif key == arcade.key.E:
            Enemy.spawn_enemy()

        # M
        elif key == arcade.key.M:
            Settings.master_volume_toggle()

        elif key == arcade.key.ESCAPE:

            self.window.show_view(PauseMenuView(self))

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        # Movement | WASD + Arrow keys
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = False
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_key_down = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_key_down = False

        # Shoot | Spacebar
        elif key == arcade.key.SPACE:
            self.space_down = False
            self.shoot_pressed = False

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
                    Enemy.despawn(enemy, C.DEATH.KILLED)
                    # Play a sound
                    arcade.play_sound(enemy.audio_destroyed,
                                      volume=enemy.audio_volume)
                    Tracker.increment_score(10)
                else:
                    # Play a sound
                    arcade.play_sound(
                        enemy.audio_hit, volume=enemy.audio_volume)
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
        for enemy in arcade.check_for_collision_with_list(
                self.player, Enemy.enemy_list):
            Enemy.despawn(enemy, C.DEATH.COLLISION)
            arcade.play_sound(enemy.audio_destroyed, volume=enemy.audio_volume)
            self.player.take_damage(enemy)
        # Check gold collision with player
        for gold in arcade.check_for_collision_with_list(self.player, Gold.gold_list):
            Gold.despawn(gold, C.DEATH.PICKED_UP)
            arcade.play_sound(gold.pick_up, volume=gold.audio_volume)

    def on_show(self):
        pass
