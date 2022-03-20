import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MAP_SCALING
from player import Player
from bullet import Bullet
from enemy import Enemy


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
        self.enemy_list = None
        self.bullet_list = None

        # Separate variable that holds the player sprite
        self.player = None
        self.bullet = None
        self.enemy = None

        # What key is pressed down?
        self.left_key_down = False
        self.right_key_down = False
        self.space_down = False

        # Tile map
        self.tile_map = None

        # Camera
        self.camera = None

        # Set up camera
        self.camera = arcade.Camera(self.width, self.height)

        # Set up the map / tiles
        border_layer = "border"
        road_layer = "road"
        holes_layer = "holes"
        map_path = "resources/maps/repeat.tmx"

        # Set layer options
        layer_options = {
            border_layer: {

            },
            road_layer: {
                "use_spatial_hash": True,
            },
            holes_layer: {

            },
        }

        # Read the map
        self.tile_map = arcade.tilemap.load_tilemap(map_path, MAP_SCALING, layer_options)

        # Initialize scene with map
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up everything with the game """

        # Create the sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
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

        # Activate Camera
        self.camera.use()

        # Draw our sprites
        self.scene.draw()

        # Draw our sprites
        self.player_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()

    # Run every tick
    # TODO: How to limit fps? Does computing power affect the speed?
    def on_update(self, delta_time: float):


        # MOVE PLAYER:
        self.player.center_x += 1
        # Add player y coordinate the current speed
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
                else:
                    # Play a sound
                    arcade.play_sound(_enemy.audio_hit)

            """ Remove off screen bullets """

            # Check if bullet is in view, if not delete it
            if bullet.center_x - bullet.width / 2 > SCREEN_WIDTH:
                self.bullet_list.remove(bullet)

        self.center_camera_to_player()

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

        # E
        if key == arcade.key.E:
            self.spawn_enemy()

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
        self.enemy.center_y = SCREEN_HEIGHT // 2

        # Turn the enemy 90 degree
        self.enemy.angle = 90

        # Add to player sprite list
        self.enemy_list.append(self.enemy)

    def shoot(self):
        self.bullet = Bullet(hit_box_algorithm="Detailed")

        # Set bullet location
        self.bullet.center_x = self.player.center_x + self.player.width
        self.bullet.center_y = self.player.center_y

        # Turn the player -90 degree
        # self.bullet.angle = 0

        # Add to player sprite list
        self.bullet_list.append(self.bullet)

        # Play a sound
        arcade.play_sound(self.bullet.audio_gunshot)

    def center_camera_to_player(self):
        screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player.center_y - (
                self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        # Don't let it go too far the other way either
        if self.player.center_x - screen_center_x > 150:
            screen_center_x = self.player.center_x - 150
        player_centered = screen_center_x, screen_center_y
        self.camera.move_to(player_centered)

def main():
    """Main function"""
    window = Game()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
