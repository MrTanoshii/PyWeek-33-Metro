import arcade
from constants import GOLD_SCALING, SPEED_SCROLLING, DEATH, MASTER_VOLUME
from tracker import Tracker


class Gold(arcade.Sprite):
    """
    Gold Sprite

    ...

    Attributes
    ----------
    gold_list : arcade.SpriteList()
        List of gold sprites 
    audio_volume : float
        The volume of sfx

    Class Methods
    -------
    update(delta_time: float = 1 / 60)
        Update the gold

    Methods
    -------
    spawn(center_x: float, center_y:float)
        Create the gold
    despawn(death: Literal)
        Remove the gold
    """

    # SpriteList class attribute
    gold_list = arcade.SpriteList()

    # Volume class attribute
    audio_volume = MASTER_VOLUME

    def __init__(self, hit_box_algorithm="Simple"):
        # Inherit parent class
        super().__init__()

        # Load texture
        base_path = ":resources:"
        self.texture = arcade.load_texture(
            f"{base_path}images/items/gold_1.png", hit_box_algorithm=hit_box_algorithm)

        # Scale
        self.scale = GOLD_SCALING

        # Load sfx
        self.pick_up = arcade.load_sound(f"{base_path}sounds/coin1.wav")

        # Speed
        self.speed = SPEED_SCROLLING

    def spawn(center_x, center_y):
        gold = Gold()
        gold.center_x = center_x
        gold.center_y = center_y
        Gold.gold_list.append(gold)

    def despawn(self, death):
        if death == DEATH.PICKED_UP:
            Tracker.increment_score(2)
            Tracker.increment_gold(5)
        self.remove_from_sprite_lists()

    @classmethod
    def update(cls, delta_time: float = 1 / 60):
        for gold in cls.gold_list:
            gold.center_x += gold.speed
            if gold.center_x + gold.width <= 0:
                cls.despawn(gold, DEATH.OOB)
