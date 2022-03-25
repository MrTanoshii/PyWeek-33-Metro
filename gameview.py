import arcade
import random
import os.path

import const.constants as C
from bg import BackGround
from lib import global_scale
from player import Player
from bullet import Bullet
from enemy import Enemy
from gold import Gold
from tracker import Tracker
from settings import Settings
from audio import Audio

from pause_menu_view import PauseMenuView
from game_over_view import GameOverView
import mapview


class GameView(arcade.View):
    """
    GameView View

    ...

    Methods
    -------
    setup()
        Set up the game view and initialize the variables
    on_draw()
        Draw the game view
    on_update(delta_time: float)
        Update the game view
    on_mouse_motion(x: float, y: float, dx: float, dy: float)
        Listen to mouse motion event
    on_mouse_press(x: float, y: float, button: int, modifiers: int)
        Listen to mouse press event
    on_key_press(key: int, modifiers: int)
        Listen to keyboard press event
    on_key_release(key: int, modifiers: int)
        Listen to keyboard release event
    check_collision()
        Check for collisions and calculate score
    on_show()
        Show the game view
    """

    def __init__(self, map_view):
        # Inherit parent class
        super().__init__()

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

        # Counting the enemy killed -> Temporary level completion (kill 5 enemies)
        self.enemy_killed = 0

        # GUI
        self.gui_camera = None
        self.setup_complete = False

        # Player shoot
        self.shoot_pressed = False

        self.level = mapview.MapView.current_level
        for monument in C.MAP_MONUMENTS_LIST:
            if monument["level"] == self.level:
                self.enemy_list = monument["enemy"]
                break

        self.map_view = map_view

        arcade.set_background_color(arcade.csscolor.GREEN)

        self.text_color = None

    def setup(self):
        """ Set up everything with the game """

        # self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Create player sprite
        self.player = Player(hit_box_algorithm="Simple",
                             current_level=self.level)

        # Rotate player to face to the right

        # Add to player sprite list

        # Create BG sprite
        self.bg = BackGround(mapview.MapView.current_level)
        self.bg.center_x = -self.bg.width
        self.bg.center_y = (C.SCREEN_HEIGHT/2)
        BackGround.bg_list.append(self.bg)
        self.setup_complete = True

        # Preload enemy
        Enemy.preload(self.enemy_list)

        # Cursor
        self.cursor = arcade.Sprite(scale=0.7)
        self.cursor.cur_texture = 0
        self.cursor.texture_list = []
        for filename in os.listdir(f"assets/CursorCrosshair/"):
            self.cursor.texture_list.append(
                arcade.load_texture(f"assets/CursorCrosshair/{filename}"))
        self.cursor.texture = self.cursor.texture_list[0]
        self.cursor.color = (128, 0, 0)

        # Find & set map bgm
        view = None
        for monument_dict in C.MAP_MONUMENTS_LIST:
            if monument_dict["level"] == mapview.MapView.current_level:
                view = monument_dict
        for i in range(0, len(Audio.bgm_list)):
            if Audio.bgm_list[i]["view_name"] == view["name"]:
                self.bgm = Audio.bgm_list[i]["sound"]
                break

        # change bullets for ak for night level
        if self.level == 1:
            self.text_color = arcade.color.WHITE
            Bullet.friendly_bullet_list.color = (300, 128, 128)
        else:
            Bullet.friendly_bullet_list.color = (255, 255, 255)
            self.text_color = arcade.color.BLACK

        # Start bgm
        self.bgm_stream = Audio.play_sound(self.bgm, True)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        #  Night Colors for level one
        if self.level == 1:
            self.bg.color = (32, 32, 64)
            Bullet.enemy_bullet_list.color = (610, 255, 255)
            Enemy.enemy_list.color = (64, 64, 64)
            self.player.color = (64, 64, 64)
        else:
            self.bg.color = (255, 255, 255)
            Bullet.enemy_bullet_list.color = (255, 255, 255)
            Enemy.enemy_list.color = (255, 255, 255)
            self.player.color = (255, 255, 255)

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
        Enemy.enemy_list.update_animation()

        # GUI - Score
        arcade.draw_text(
            f"Score : {Tracker.score}",
            (C.SCREEN_WIDTH / 5) * global_scale(),
            (C.SCREEN_HEIGHT - 50) * global_scale(),
            self.text_color,
            font_size=30 * global_scale(),
            anchor_x="center",
        )

        # GUI - Gold
        arcade.draw_text(
            f"Gold : {Tracker.gold}",
            (C.SCREEN_WIDTH / 5) * global_scale(),
            (C.SCREEN_HEIGHT - 150) * global_scale(),
            self.text_color,
            font_size=30 * global_scale(),
            anchor_x="center",
        )

        # GUI - Player HP
        arcade.draw_text(
            f"HP : {self.player.cur_health}",
            ((C.SCREEN_WIDTH / 5) + 200) * global_scale(),
            (C.SCREEN_HEIGHT - 50) * global_scale(),
            self.text_color,
            font_size=30 * global_scale(),
            anchor_x="center",
        )

        # GUI - Player Ammo
        arcade.draw_text(
            f"Ammo : {self.player.weapon.cur_ammo} \ {self.player.weapon.max_ammo}",
            ((C.SCREEN_WIDTH / 5) + 500) * global_scale(),
            (C.SCREEN_HEIGHT - 50) * global_scale(),
            self.text_color,
            font_size=30 * global_scale(),
            anchor_x="center",
        )

        self.cursor.draw()

        # Restart bgm
        if self.bgm_stream == None:
            self.bgm_stream = Audio.play_sound(self.bgm, True)

    def on_update(self, delta_time):
        if self.player.is_dead:
            # Stop bgm
            Audio.stop_sound(self.bgm_stream)
            # Game Over Screen
            self.window.show_view(GameOverView(
                self, self.map_view, self.level))
        else:
            if random.randint(0, 200) == 1:
                Enemy.spawn_enemy(self.enemy_list)

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

            Enemy.update(delta_time)
            Bullet.update()
            self.player.update_animation(delta_time)
            self.update_cursor_animation(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        """Called whenever mouse is moved."""
        self.player.weapon.on_mouse_motion(x, y, dx, dy)
        self.cursor.center_x = x + C.GUI["Crosshair"]["offset_x"]
        self.cursor.center_y = y + C.GUI["Crosshair"]["offset_y"]

    def on_mouse_press(self, x, y, button, modifiers):
        """Called whenever a mouse key is pressed."""
        # Mouse Left Click
        if button == arcade.MOUSE_BUTTON_LEFT:
            for enemy in Enemy.enemy_list:
                enemy.shoot()

        if C.DEBUG.MAP:
            print(x, y)

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
        elif key == arcade.key.KEY_1 or key == arcade.key.KEY_2 or key == arcade.key.KEY_3 or key == arcade.key.KEY_4:
            requested_weapon = ""
            # 1 - Revolver
            if key == arcade.key.KEY_1:
                requested_weapon = "Revolver"
                self.player.set_skin('Revolver')
                if self.level == 1:
                    Bullet.friendly_bullet_list.color = (300, 128, 128)
                else:
                    Bullet.friendly_bullet_list.color = (255, 255, 255)
            # 2 - Rifle
            elif key == arcade.key.KEY_2:
                requested_weapon = "Rifle"
                self.player.set_skin('AK')
                if self.level == 1:
                    Bullet.friendly_bullet_list.color = (300, 128, 128)
                else:
                    Bullet.friendly_bullet_list.color = (255, 255, 255)
            # 2 - Shotgun
            elif key == arcade.key.KEY_3:
                requested_weapon = "Shotgun"
                self.player.set_skin('Shotgun')
                if self.level == 1:
                    Bullet.friendly_bullet_list.color = (128, 64, 64)
                else:
                    Bullet.friendly_bullet_list.color = (255, 255, 255)
            # 4 - RPG
            elif key == arcade.key.KEY_4:
                requested_weapon = "RPG"
                self.player.set_skin('RPG')
                if self.level == 1:
                    Bullet.friendly_bullet_list.color = (610, 255, 255)
                else:
                    Bullet.friendly_bullet_list.color = (255, 255, 255)

            # Swap weapon
            if Player.weapon.weapon_name != requested_weapon:
                Player.weapon.swap_weapon(requested_weapon)

        # Enemy spawn | E
        elif key == arcade.key.E:
            Enemy.spawn_enemy(self.enemy_list)

        # Volume Toggle | M
        elif key == arcade.key.M:
            Settings.master_volume_toggle()

        # Pause menu | Escape
        elif key == arcade.key.ESCAPE:

            # Stop bgm
            Audio.stop_sound(self.bgm_stream)
            self.bgm_stream = None
            self.window.show_view(PauseMenuView(
                self, self.map_view, self.level))

        # test atc demo, when press num pad 0 change skin
        elif key == arcade.key.NUM_0:
            self.player.set_skin('GuyGoatRPG')

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

                    # Play enemy death sfx
                    Audio.play_rand_sound(enemy.sfx_death_list)
                    self.enemy_killed += 1  # Increment Enemy killed

                    Tracker.increment_score(10)
                else:
                    # Play enemy hit sfx
                    Audio.play_rand_sound(enemy.sfx_hit_list)

        # Check enemy bullet collisions
        for bullet in Bullet.enemy_bullet_list:
            # Move all Bullets Forwards
            bullet.center_x += bullet.speed_x * global_scale()
            bullet.center_y += bullet.speed_y * global_scale()

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
            self.player.take_damage(enemy)

        # Check gold collision with player
        for gold in arcade.check_for_collision_with_list(self.player, Gold.gold_list):
            Gold.despawn(gold, C.DEATH.PICKED_UP)

    def on_show(self):
        pass

    def update_cursor_animation(self, delta_time: float = 1 / 60):
        # TODO: Change animation speed from hardcoded to constant
        animation_speed = 12

        if len(self.cursor.texture_list) > 1:
            self.cursor.cur_texture += animation_speed * delta_time
            while self.cursor.cur_texture >= len(self.cursor.texture_list) - 1:
                self.cursor.cur_texture -= len(self.cursor.texture_list) - 1
                if self.cursor.cur_texture <= 0:
                    self.cursor.cur_texture = 0
                    break
        self.cursor.texture = self.cursor.texture_list[int(
            self.cursor.cur_texture)]
