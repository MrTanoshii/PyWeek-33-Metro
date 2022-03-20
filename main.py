import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from player import Player
from bullet import Bullet


class Game(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.player_list = None
        self.bullet_list = None

        # Separate variable that holds the player sprite
        self.player = None
        self.bullet = None

        # What key is pressed down?
        self.left_key_down = False
        self.right_key_down = False
        self.space_down = False

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up everything with the game """

        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Create player sprite
        self.player = Player(hit_box_algorithm="Detailed")

        # Set player location
        self.player.center_x = SCREEN_WIDTH * .1
        self.player.center_y = SCREEN_HEIGHT * .5

        # Turn the player -90 degree
        self.player.angle = -90

        # Add to player sprite list
        self.player_list.append(self.player)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        self.player_list.draw()
        self.bullet_list.draw()

    # Run every tick
    # TODO: How to limit fps? Does computing power affect the speed?
    def on_update(self, delta_time: float):

        # MOVE PLAYER: Add player y coordinate the current speed
        self.player.center_y += self.player.current_speed

        # Cycle trough all bullets
        for bullet in self.bullet_list:

            # Move all Bullets Forwards
            bullet.center_x += bullet.SPEED

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
            self.shoot()

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

    def shoot(self):
        print("shot")
        self.bullet = Bullet(hit_box_algorithm="Detailed")

        # Set bullet location
        self.bullet.center_x = self.player.center_x + self.player.width
        self.bullet.center_y = self.player.center_y

        # Turn the player -90 degree
        # self.bullet.angle = 0

        # Add to player sprite list
        self.bullet_list.append(self.bullet)


def main():
    """Main function"""
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
