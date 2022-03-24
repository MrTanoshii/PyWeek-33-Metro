import arcade
import constants as C

#Base ShopView
class ShopView(arcade.View):

    def __init__(self):

        super().__init__()

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(C.MENU_BACKGROUND_COLOR)

    def on_draw(self):
        """Draw the menu"""
        self.clear()

        arcade.draw_text(
            "Congrats you have passed Level - Let's go for Shop",
            C.SCREEN_WIDTH / 2,
            C.SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=C.MENU_FONT_SIZE,
            anchor_x="center",
        )

    def on_key_press(self, key, _modifiers):
        """Handle keyboard key press"""
        if key == arcade.key.ESCAPE:
            arcade.exit()