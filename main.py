import arcade
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, level1
from player import Player
from bullet import Bullet
from enemy import Enemy
from bg import BackGround


class MainMenu(arcade.View):
    """Class that manages the 'menu' view."""

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        arcade.draw_text(
            "Main Menu - Click to play",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = GameView()
        self.window.show_view(game_view)


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
        self.enemy_list = None
        self.bullet_list = None
        self.bg_list = None

        # Separate variable that holds the player sprite
        self.player = None
        self.bullet = None
        self.enemy = None
        self.bg = None

        # What key is pressed down?
        self.left_key_down = False
        self.right_key_down = False
        self.space_down = False

        # GUI
        self.score = 0
        self.gui_camera = None

        arcade.set_background_color(arcade.csscolor.DARK_GREEN)

    def setup(self):
        """ Set up everything with the game """

        # self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
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
        self.enemy_list.draw()
        self.bullet_list.draw()

        arcade.draw_text(
            f"Score : {self.score}",
            SCREEN_WIDTH / 5,
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
            self.spawn_enemy()

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

        # Cycle trough all enemies
        for enemy in self.enemy_list:

            # Move all Enemies Forwards
            enemy.center_x += enemy.SPEED

            # Check if enemy is in view, if not delete it
            if enemy.center_x + enemy.width < 0:
                enemy.remove_from_sprite_lists()

        # Cycle trough all bullets
        for bullet in self.bullet_list:

            # Move all Bullets Forwards
            bullet.center_x += bullet.SPEED

            """ Collision """
            # Add enemy to list, if collided with bullet
            enemy_hit_list = arcade.check_for_collision_with_list(
                bullet, self.enemy_list
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
                    self.score += 1
                else:
                    # Play a sound
                    arcade.play_sound(_enemy.audio_hit)

            """ Remove off screen bullets """

            # Check if bullet is in view, if not delete it
            if bullet.center_x - bullet.width / 2 > SCREEN_WIDTH:
                self.bullet_list.remove(bullet)

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
        if key == arcade.key.SPACE:
            self.space_down = True
            self.player.shoot(self.bullet_list)

        # E
        if key == arcade.key.E:
            self.spawn_enemy()

        # T
        if key == arcade.key.T:
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

    def spawn_enemy(self):
        self.enemy = Enemy(hit_box_algorithm="Detailed")

        # Set bullet location
        self.enemy.center_x = SCREEN_WIDTH + self.enemy.width
        self.enemy.center_y = SCREEN_HEIGHT // 2 + random.uniform(-SCREEN_HEIGHT/3.25, SCREEN_HEIGHT/3.25)

        # Turn the enemy 90 degree
        self.enemy.angle = -90

        # Add to player sprite list
        self.enemy_list.append(self.enemy)

    def spawn_bg(self):
        # Create BG sprite
        assets = level1.assets
        self.bg = BackGround(asset=random.choice(assets), size=random.uniform(.9, 1.1))
        self.bg.center_x = SCREEN_WIDTH + self.bg.width / 2
        if random.randint(0,1) == 1:
            self.bg.center_y = SCREEN_HEIGHT + self.bg.height / 2 - random.uniform(50, 75)
        else:
            self.bg.center_y = self.bg.height / 2 + random.uniform(-50, 50)
        self.bg_list.append(self.bg)

    def on_show(self):
        self.setup()


def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
