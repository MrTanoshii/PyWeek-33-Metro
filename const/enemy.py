from const.scale import *
from const.audio import *

ENEMY_LIST = {
    "tank": {
        "name": "tank",
        "weapon": "tank",
        "animation_speed": 1.5,
        "scale": 1,
        "speed": -2,
        "spawn_rate": 1,
        "health": 10,
        "shoot_offset": (80, 85),
        "sfx_death": [AUDIO.SOUND["enemy_death_tank_1"]["name"], AUDIO.SOUND["enemy_death_tank_2"]["name"]],
        "sfx_death_gain": [AUDIO.SOUND["enemy_death_tank_1"]["gain"], AUDIO.SOUND["enemy_death_tank_2"]["gain"]],
        "sfx_hit": [AUDIO.SOUND["enemy_hit_1"]["name"]],
        "sfx_hit_gain": [AUDIO.SOUND["enemy_hit_1"]["gain"]]
    },
    "soldier desert": {
        "name": "soldier desert",
        "weapon": "soldier",
        "animation_speed": 1.5,
        "scale": 1,
        "speed": -2,
        "spawn_rate": 1,
        "health": 10,
        "shoot_offset": (20, 88),
        "sfx_death": [AUDIO.SOUND["player_death"]["name"]],
        "sfx_death_gain": [AUDIO.SOUND["player_death"]["gain"]],
        "sfx_hit": [AUDIO.SOUND["player_hit"]["name"], AUDIO.SOUND["player_hit"]["name"]],
        "sfx_hit_gain": [AUDIO.SOUND["player_hit"]["gain"], AUDIO.SOUND["player_hit"]["gain"]]
    }
}
