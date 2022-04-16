import src.const as C

from src.sprite.bullet import Bullet
from src.sprite.enemy import Enemy
from src.sprite.gold import Gold


class Settings:
    """
    Settings Class

    ...

    Attributes
    ----------
    master_volume : float
        The volume of sfx
    mute : bool
        True/False for muting sfx

    Class Methods
    -------------
    master_volume_toggle()
        Toggles the master volume
    update_master_volume()
        Updates the master volume of classes
    """

    # Volume class attribute
    master_volume = C.AUDIO.MASTER_VOLUME
    mute = False

    # def __init__(self):
    #     # Inherit parent class
    #     super().__init__()

    @classmethod
    def master_volume_toggle(cls):
        cls.mute = not cls.mute

        # if muted, then 0, other default
        if cls.mute:
            cls.master_volume = 0
        else:
            cls.master_volume = C.AUDIO.MASTER_VOLUME

        # Update all volumes
        cls.update_master_volume()

    @classmethod
    def update_master_volume(cls):
        Bullet.audio_volume = cls.master_volume
        Enemy.audio_volume = cls.master_volume
        Gold.audio_volume = cls.master_volume
