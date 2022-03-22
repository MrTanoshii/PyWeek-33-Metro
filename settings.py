import arcade
from constants import MASTER_VOLUME
from player import Player
from bullet import Bullet
from enemy import Enemy
from gold import Gold


class Settings:
    """ Settings """

    def __init__(self):
        # Let parent initialize
        super().__init__()

    master_volume = MASTER_VOLUME
    mute = False

    @classmethod
    def master_volume_toggle(cls):
        cls.mute = not cls.mute

        # if muted, then 0, other default
        if cls.mute:
            cls.master_volume = 0
        else:
            cls.master_volume = MASTER_VOLUME

        # Update all volumes
        cls.update_master_volume()

    @classmethod
    def update_master_volume(cls):
        Player.audio_volume = cls.master_volume
        Bullet.audio_volume = cls.master_volume
        Enemy.audio_volume = cls.master_volume
        Gold.audio_volume = cls.master_volume

