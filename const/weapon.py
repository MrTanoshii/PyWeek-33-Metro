from const.audio import *
from const.weapon_fire import *
from const.scale import *


# TODO: Refactor WEAPON_INIT_ANGLE into WEAPON_LIST
WEAPON_INIT_ANGLE = -90

WEAPON_LIST = [
    {
        "name": "Rifle",
        "img_name": "weapon_ak",
        "width": 640,
        "height": 360,
        "scale": 3*WEAPON_SCALING,
        "center_x": 0,
        "center_y": 0,
        "fire_mode": FIRE_MODE.FULL_AUTO,
        "fire_type": FIRE_TYPE.LINE,
        "max_ammo": 30,
        "bullet_texture_amount": 39,
        "bullet_speed": 25,
        "bullet_damage": 3,
        "bullet_scale": .3,
        "shoot_time": 0.1,
        "reload_time": 1.5,
        "reload_rate": 30,
        "sfx_single_shot_list": [AUDIO.SOUND["weapon_ak_1"]["name"], AUDIO.SOUND["weapon_ak_2"]["name"], AUDIO.SOUND["weapon_ak_3"]["name"]],
        "sfx_single_shot_vol_gain_list": [AUDIO.SOUND["weapon_ak_1"]["gain"], AUDIO.SOUND["weapon_ak_2"]["gain"], AUDIO.SOUND["weapon_ak_3"]["gain"]]
    },
    {
        "name": "Shotgun",
        "img_name": "weapon_shotgun",
        "width": 640,
        "height": 360,
        "scale": 3*WEAPON_SCALING,
        "center_x": 0,
        "center_y": 0,
        "fire_mode": FIRE_MODE.FULL_AUTO,
        "fire_type": FIRE_TYPE.CONE,
        "max_ammo": 8,
        "bullet_texture_amount": 1,
        "bullet_speed": 18,
        "bullet_damage": 2,
        "bullet_scale": .5,
        "shoot_time": 0.3,
        "reload_time": 0.8,
        "reload_rate": 8,
        "sfx_single_shot_list": [AUDIO.SOUND["weapon_shotgun_1"]["name"], AUDIO.SOUND["weapon_shotgun_2"]["name"], AUDIO.SOUND["weapon_shotgun_3"]["name"]],
        "sfx_single_shot_vol_gain_list": [AUDIO.SOUND["weapon_shotgun_1"]["gain"], AUDIO.SOUND["weapon_shotgun_2"]["gain"], AUDIO.SOUND["weapon_shotgun_3"]["gain"]]
    },
    {
        "name": "RPG",
        "img_name": "weapon_rpg",
        "width": 640,
        "height": 360,
        "scale": 3*WEAPON_SCALING,
        "center_x": 0,
        "center_y": 0,
        "fire_mode": FIRE_MODE.SEMI_AUTO,
        "fire_type": FIRE_TYPE.LINE,
        "max_ammo": 1,
        "bullet_texture_amount": 24,
        "bullet_speed": 21,
        "bullet_damage": 15,
        "bullet_scale": 2,
        "shoot_time": 1,
        "reload_time": 2.5,
        "reload_rate": 1,
        "sfx_single_shot_list": [AUDIO.SOUND["weapon_rpg_1"]["name"], AUDIO.SOUND["weapon_rpg_2"]["name"]],
        "sfx_single_shot_vol_gain_list": [AUDIO.SOUND["weapon_rpg_1"]["gain"], AUDIO.SOUND["weapon_rpg_2"]["gain"]]
    }
]
