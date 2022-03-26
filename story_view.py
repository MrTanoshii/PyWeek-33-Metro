import arcade
import const.constants as C
from audio import Audio
from lib import global_scale
from gamedata import GameData


class StoryView(arcade.View):
    """
    PauseMenuView View

    ...

    Methods
    -------
    on_show()
        Show the pause menu view
    on_draw()
        Draw the pause menu view
    on_mouse_press(x: float, y: float, button: int, modifiers: int)
        Listen to mouse press event
    on_key_press(key: int, modifiers: int)
        Listen to keyboard press event
    """

    def __init__(self, map_view, current_level):
        # Inherit parent class
        super().__init__()

        # Init images
        self.cursor_sprite = None
        self.background = None

        # Define mapview so we can go back there
        self.map_view = map_view

        # Define current level so we can show right story
        self.current_level = current_level

        # Init text
        self.text_scale = None
        self.current_text = None
        self.current_text_index = None
        self.text_box = None

        # Controls
        self.mouse_pressed = None
        self.space_pressed = None

        # Music
        self.bgm_stream = None
        self.bgm = None

    def setup(self):
        """ Set up everything with the pause view """

        # Create the sprites
        self.background = arcade.load_texture(
            "resources/images/story_screen.png")
        self.cursor_sprite = arcade.Sprite(
            "resources/images/goat_cursor.png", 1)

        # Background music
        self.bgm_stream = None
        view = None
        for view_dict in C.VIEW_LIST:
            if view_dict["name"] == "Pause":
                view = view_dict
        for i in range(0, len(Audio.bgm_list)):
            if Audio.bgm_list[i]["view_name"] == view["name"]:
                self.bgm = Audio.bgm_list[i]["sound"]
                break

        # Define text
        self.text_scale = 1
        self.current_text = ""
        self.current_text_index = 0

        # Start background music
        self.bgm_stream = Audio.play_sound(self.bgm, True)

    def on_show(self):
        """Called when switching to this view."""
        self.setup()

    def on_draw(self):
        """Draw the view"""
        self.clear()

        # Draw the bg image
        arcade.draw_lrwh_rectangle_textured(0, 0, C.SCREEN_WIDTH * global_scale(),
                                            C.SCREEN_HEIGHT * global_scale(), self.background)

        # Draw the text
        self.text_box = arcade.Text(
            self.current_text,
            C.SCREEN_WIDTH // 2,
            C.SCREEN_HEIGHT * .1 // 1,
            arcade.color.BLACK,
            font_size=30 * global_scale(),
            multiline=True,
            width=C.SCREEN_WIDTH * .8,
            anchor_x="center",
            align="center",
        )

        arcade.draw_rectangle_filled(
            self.text_box.position[0],
            self.text_box.position[1] + self.text_box.y // 2 - self.text_box.content_height // 2,
            self.text_box.content_width * 1.1,
            self.text_box.content_height * 1.1,
            (255, 255, 255, 64)
        )

        self.text_box.draw()

        # Draw the cursor
        self.cursor_sprite.draw()

    def on_update(self, delta_time: float):
        if self.space_pressed or self.mouse_pressed:
            self.mouse_pressed, self.space_pressed = False, False
            self.current_text = self.next_text()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Move the cursor image when mouse moved """
        self.cursor_sprite.center_x = x + \
            C.MAP["Cursor"]["offset_x"] * global_scale()
        self.cursor_sprite.center_y = y + \
            C.MAP["Cursor"]["offset_y"] * global_scale()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        self.mouse_pressed = True

    def on_key_press(self, key, _modifiers):
        """Handle keyboard key press"""
        if key == arcade.key.SPACE:
            self.space_pressed = True

    def to_map(self):
        """ Go back to map view """
        Audio.stop_sound(self.bgm_stream)
        self.bgm_stream = None
        self.window.show_view(self.map_view)

    def next_text(self):
        """ Gets the index """
        story_list = C.STORY[self.current_level]
        index = self.current_text_index

        if len(story_list) > index:
            text = C.STORY[self.current_level][index]
            self.current_text_index = index + 1
            return "".join(text)

        else:
            # save story to passed
            GameData.update_steps(str(self.current_level), 2)
            self.to_map()
