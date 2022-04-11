import arcade
import const.constants as C
from tracker import Tracker
from audio import Audio
from lib import global_scale


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
    audio_volume = C.AUDIO.MASTER_VOLUME

    def __init__(self, hit_box_algorithm="Simple", scale=C.GOLD_SCALE):
        # Inherit parent class
        super().__init__()

        # Load texture
        base_path = ":resources:"
        self.texture = arcade.load_texture(
            f"{base_path}images/items/gold_1.png", hit_box_algorithm=hit_box_algorithm)

        # Scale
        self.scale = scale * global_scale()

        # TODO: Change hardcoded gold
        self.name = C.GOLD_LIST[0]["name"]

        # Find & set pickup sfx
        for i in enumerate(Audio.sfx_gold_pickup_list):
            if Audio.sfx_gold_pickup_list[i]["gold_name"] == self.name:
                self.sfx_pickup = Audio.sfx_gold_pickup_list[i]["sound"]
                break

        # Speed
        self.speed = C.SPEED_SCROLLING

    @classmethod
    def spawn(cls, center_x, center_y):
        gold = Gold()
        gold.center_x = center_x
        gold.center_y = center_y
        Gold.gold_list.append(gold)

    def despawn(self, death):
        if death == C.DEATH.PICKED_UP:
            Tracker.increment_score(2)
            Tracker.increment_gold(5)

            # Play pickup sfx sound
            Audio.play_sound(self.sfx_pickup)

        self.remove_from_sprite_lists()

    @classmethod
    def update(cls, delta_time: float = 1 / 60):
        for gold in cls.gold_list:
            gold.center_x += gold.speed * global_scale()
            if gold.center_x + gold.width <= 0:
                cls.despawn(gold, C.DEATH.OOB)
