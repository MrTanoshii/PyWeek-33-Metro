import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "REVƎЯ"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5

# arcade tutorial copy paste code :D
class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # player speed
        self.player_speed = 0
        self.SPEED = 2

        # What key is pressed down?
        self.left_key_down = False
        self.right_key_down = False

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "resources/images/car.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH * .1
        self.player_sprite.center_y = SCREEN_HEIGHT * .5
        self.player_sprite.angle = -90
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        self.player_list.draw()

    def on_update(self, delta_time: float):
        self.player_sprite.center_y += self.player_speed

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

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = False
            self.update_player_speed()

    def update_player_speed(self):
        self.player_speed = 0

        # D pressed
        if self.left_key_down and not self.right_key_down:
            self.player_speed = self.SPEED
        # A pressed
        elif self.right_key_down and not self.left_key_down:
            self.player_speed = -self.SPEED


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()