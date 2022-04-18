import arcade

import src.const as C

from src.audio import Audio
import src.lib as lib
from src.tracker import Tracker


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
    update_animation(delta_time: float)
        Update the animated texture
    """

    # SpriteList class attribute
    gold_list = arcade.SpriteList()

    # Volume class attribute
    audio_volume = C.AUDIO.MASTER_VOLUME

    def __init__(self, hit_box_algorithm="Simple", scale=C.GOLD_SCALE):
        # Inherit parent class
        super().__init__()

        # TODO: Implement animated gold
        # Load texture
        base_path = ":resources:"
        self.texture = arcade.load_texture(
            f"{base_path}images/items/gold_1.png", hit_box_algorithm=hit_box_algorithm)
        self.current_texture: float = 0
        self.animation_speed: float = 1

        # Scale
        self.scale = scale * lib.global_scale()

        # TODO: Change hardcoded gold
        self.name = C.GOLD_LIST[0]["name"]

        # Find & set pickup sfx
        for _i, sfx in enumerate(Audio.sfx_gold_pickup_list):
            if sfx["gold_name"] == self.name:
                self.sfx_pickup = sfx["sound"]
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
            gold.center_x += gold.speed * lib.global_scale()
            if gold.center_x + gold.width <= 0:
                cls.despawn(gold, C.DEATH.OOB)

    # TODO: Implement animated gold
    # def update_animation(self, delta_time: float):
    # """ Update the animated texture """
    #
    #     self.current_texture = lib.find_next_texture(
    #         delta_time, self.cur_texture, self.texture_list, self.animation_speed)
    #     self.texture = self.texture_list[int(self.current_texture)]
