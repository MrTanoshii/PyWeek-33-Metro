import arcade
from constants import GOLD_SCALING, SPEED_SCROLLING


class Gold(arcade.Sprite):
    """ Gold Sprite """

    gold_list = arcade.SpriteList()

    def __init__(self, hit_box_algorithm="Detailed"):
        # Let parent initialize
        super().__init__()

        # Load texture
        base_path = ":resources:"
        self.texture = arcade.load_texture(
            f"{base_path}images/items/gold_1.png", hit_box_algorithm=hit_box_algorithm)

        # Scale
        self.scale = GOLD_SCALING

        # Speed
        self.speed = SPEED_SCROLLING

    def spawn(center_x, center_y):
        gold = Gold()
        gold.center_x = center_x
        gold.center_y = center_y
        Gold.gold_list.append(gold)

    @classmethod
    def update(cls, delta_time: float = 1 / 60):
        for gold in cls.gold_list:
            gold.center_x += gold.speed
