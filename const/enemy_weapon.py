from const.audio import *
from const.weapon_fire import *
from const.scale import *

ENEMY_LOGIC = {
    "aim_player": 0,
    "aim_straight": 1,
    "aim_random": 2,
    "prob_aim_player": 0.2,
    "prob_aim_straight": 0.4,
    "prob_aim_random": 0.4
}

ENEMY_WEAPON_LIST = [
    {
        "name": "tank",
        "folder_name": "weapon_tank",
        "init_angle": 180,
        "fire_mode": FIRE_MODE.SEMI_AUTO,
        "max_ammo": 1,
        "damage_value": 5,
        "bullet_texture_amount": 39,
        "bullet_amount": 1,
        "bullet_spread": 0.5,
        "bullet_speed": 20,
        "bullet_speed_spread": 0.01,
        "bullet_damage": 3,
        "bullet_texture_dir_name": "weapon_rpg",
        "bullet_texture_amount": 24,
        "bullet_scale": .8,
        "shoot_time": 1.8,
        "shoot_constant": False,
        "shoot_probability": 0.15,
        "shoot_max_angle": 100,
        "sfx_single_shot_list": [AUDIO.SOUND["weapon_tank_1"]["name"]],
        "sfx_single_shot_vol_gain_list": [AUDIO.SOUND["weapon_tank_1"]["gain"]]
    },
    {
        "name": "heli",
        "folder_name": "weapon_heli",
        "init_angle": 180,
        "fire_mode": FIRE_MODE.FULL_AUTO,
        "max_ammo": 8,
        "damage_value": 5,
        "bullet_texture_amount": 39,
        "bullet_amount": 1,
        "bullet_spread": 2,
        "bullet_speed": 15,
        "bullet_speed_spread": 0.1,
        "bullet_damage": 2,
        "bullet_texture_dir_name": "weapon_rpg",
        "bullet_texture_amount": 24,
        "bullet_scale": .2,
        "shoot_time": .05,
        "shoot_constant": True,
        "shoot_probability": 0.2,
        "shoot_max_angle": 140,
        "sfx_single_shot_list": [AUDIO.SOUND["weapon_heli_1"]["name"]],
        "sfx_single_shot_vol_gain_list": [AUDIO.SOUND["weapon_heli_1"]["gain"]]
    }
]
