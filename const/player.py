from const.audio import *


class PLAYER:
    MAX_HP = 69
    START_HP = 69
    DEATH_HP = 0
    SPEED = 8
    NAME = "player"
    SFX_DEATH = {
        "name": AUDIO.SOUND["player_death"]["name"],
        "gain": AUDIO.SOUND["player_death"]["gain"]
    }
    SFX_HIT = {
        "name": AUDIO.SOUND["player_hit"]["name"],
        "gain": AUDIO.SOUND["player_hit"]["gain"]
    }
    SCALE = 1


# TODO: Refactor SPRITE_PLAYER_INIT_ANGLE into PLAYER
SPRITE_PLAYER_INIT_ANGLE = 0


class MOVE_DIRECTION:
    LEFT = 0
    BOTTOM_LEFT = 1
    BOTTOM = 2
    BOTTOM_RIGHT = 3
    RIGHT = 4
    TOP_RIGHT = 5
    TOP = 6
    TOP_LEFT = 7
    IDLE = 8


PLAYER_TEXTURES = [
    {
        "name": "GuyGoat"
    },
    {
        "name": "GuyJeep"
    },
    {
        "name": "GuyJeep"
    },
    {
        "name": "GuySurf"
    },
    {
        "name": "GuyGoat"
    },
    {
        "name": "GuyJeep"
    },
]
PLAYER_WEAPONS = [
    {
        "name": "Revolver"
    },
    {
        "name": "AK"
    },
    {
        "name": "Shotgun"
    },
    {
        "name": "RPG"
    },
    {
        "name": "RPGempty"
    },
]
