import arcade

""" Include all constant values """

# Window Size and Title
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "REVƎЯ"
FULLSCREEN = False
CENTER_WINDOW = True

CURSOR_VISIBLE = False


class DEBUG:
    ALL = False
    AUDIO = False
    MAP = False


GLOBAL_SCALE = SCREEN_WIDTH / 1280


# Audio
class AUDIO:
    """
    Volume levels for various sounds

    ...

    Value: float
    Range of values: 0.0 - 1.0
    """
    # Folder path
    FOLDER = "resources/audio/"

    # Master Volume
    MASTER_VOLUME = 0.8

    BGM_VOLUME = 0.7
    SFX_VOLUME = 1

    SOUND = {
        "ui_click": {
            "name": "388713__totalcult__finger-click-02.wav",
            "gain": 0
        },
        "bgm_1": {
            "name": "427441__kiluaboy__clouds.wav",
            "gain": 0
        },
        "bgm_2": {
            "name": "428857__supervanz__arpegio01-loop.wav",
            "gain": 1
        },
        "bgm_3": {
            "name": "428858__supervanz__duskwalkin-loop.wav",
            "gain": -0.5
        },
        "gold_pickup_1": {
            "name": "402767__matrixxx__retro-coin-03.wav",
            "gain": -0.73
        },
        "player_death": {
            "name": "396798__scorpion67890__male-death-1.ogg",
            "gain": 0.1
        },
        "player_hit": {
            "name": "553285__nettoi__hurt4.ogg",
            "gain": 0.1
        },
        "enemy_death_tank_1": {
            "name": "587183__derplayer__explosion-03.wav",
            "gain": -0.9
        },
        "enemy_death_tank_2": {
            "name": "587184__derplayer__explosion-02.wav",
            "gain": -0.9
        },
        "enemy_hit_1": {
            "name": "260435__roganmcdougald__metal-impact-ceramic-piece-in-sink.wav",
            "gain": -0.85
        },
        "weapon_tank_1": {
            "name": "127845__garyq__tank-fire-mixed.wav",
            "gain": -0.4
        },
        "weapon_heli_1": {
            "name": "522470__filmmakersmanual__heavy-machine-gun.wav",
            "gain": 0
        },
        "weapon_ak_1": {
            "name": "156073__duesto__ak-47.wav",
            "gain": -.9
        },
        "weapon_ak_2": {
            "name": "509430__seanmorrissey96__ak-47.wav",
            "gain": -.7
        },
        "weapon_ak_3": {
            "name": "616091__drummerdude525__ak-74-fire.wav",
            "gain": -.75
        },
        "weapon_shotgun_1": {
            "name": "522282__filmmakersmanual__shotgun-firing-1.wav",
            "gain": -.7
        },
        "weapon_shotgun_2": {
            "name": "522284__filmmakersmanual__shotgun-firing-3.wav",
            "gain": -.7
        },
        "weapon_shotgun_3": {
            "name": "522285__filmmakersmanual__shotgun-firing-4.wav",
            "gain": -.7
        },
        "weapon_rpg_1": {
            "name": "441499__matrixxx__rocket-01.wav",
            "gain": -0.65
        },
        "weapon_rpg_2": {
            "name": "441500__matrixxx__rocket-02.wav",
            "gain": -0.65
        }
    }


VIEW_LIST = [
    {
        "name": "Map",
        "bgm_name": AUDIO.SOUND["bgm_2"]["name"],
        "bgm_gain": AUDIO.SOUND["bgm_2"]["gain"]
    },
    {
        "name": "Pause",
        "bgm_name": AUDIO.SOUND["bgm_1"]["name"],
        "bgm_gain": AUDIO.SOUND["bgm_1"]["gain"]
    }
]


class FIRE_MODE:
    SEMI_AUTO = 0
    FULL_AUTO = 1
    BURST = 2,


class FIRE_TYPE:
    LINE = 0
    CONE = 1


ENEMY_WEAPON_LIST = [
    {
        "name": "tank",
        "folder_name": "weapon_tank",
        "fire_mode": FIRE_MODE.SEMI_AUTO,
        "fire_type": FIRE_TYPE.LINE,
        "max_ammo": 1,
        "bullet_texture_amount": 39,
        "bullet_speed": 20,
        "bullet_damage": 5,
        "bullet_texture_dir_name": "weapon_rpg",
        "bullet_texture_amount": 24,
        "bullet_scale": .8,
        "shoot_time": 2,
        "reload_time": 5,
        "reload_rate": 1,
        "sfx_single_shot_list": [AUDIO.SOUND["weapon_tank_1"]["name"]],
        "sfx_single_shot_vol_gain_list": [AUDIO.SOUND["weapon_tank_1"]["gain"]]
    },
    {
        "name": "heli",
        "folder_name": "weapon_heli",
        "fire_mode": FIRE_MODE.FULL_AUTO,
        "fire_type": FIRE_TYPE.LINE,
        "max_ammo": 8,
        "bullet_texture_amount": 39,
        "bullet_speed": 15,
        "bullet_damage": 2,
        "bullet_texture_dir_name": "weapon_rpg",
        "bullet_texture_amount": 24,
        "bullet_scale": .2,
        "shoot_time": .05,
        "reload_time": 5,
        "reload_rate": 1,
        "sfx_single_shot_list": [AUDIO.SOUND["weapon_heli_1"]["name"]],
        "sfx_single_shot_vol_gain_list": [AUDIO.SOUND["weapon_heli_1"]["gain"]]
    }
]

ENEMY_LIST = {
    "tank": {
        "name": "tank",
        "weapon": "tank",
        "animation_speed": 1.5,
        "scale": 1*GLOBAL_SCALE,
        "speed": -2,
        "spawn_rate": 1,
        "health": 10,
        "barrel": (0, 80),
        "sfx_death": [AUDIO.SOUND["enemy_death_tank_1"]["name"], AUDIO.SOUND["enemy_death_tank_2"]["name"]],
        "sfx_death_gain": [AUDIO.SOUND["enemy_death_tank_1"]["gain"], AUDIO.SOUND["enemy_death_tank_2"]["gain"]],
        "sfx_hit": [AUDIO.SOUND["enemy_hit_1"]["name"]],
        "sfx_hit_gain": [AUDIO.SOUND["enemy_hit_1"]["gain"]]
    }
}

MAP_MONUMENTS_LIST = [
    {
        "name": "EGYPT",
        "level": 1,
        "img_name": "icon1.png",
        "center_x": 650 * GLOBAL_SCALE,
        "center_y": 325 * GLOBAL_SCALE,
        "assets": ["pyramids.png", "cactus.png"],
        "enemy": ENEMY_LIST["tank"],
        "player": "donky",
        "sfx_click": AUDIO.SOUND["ui_click"]["name"],
        "sfx_gain": AUDIO.SOUND["ui_click"]["gain"],
        "bgm_name": AUDIO.SOUND["bgm_3"]["name"],
        "bgm_gain": AUDIO.SOUND["bgm_3"]["gain"]

    },
    {
        "name": "MOSCOW",
        "level": 2,
        "img_name": "icon2.png",
        "center_x": 700 / 1280 * SCREEN_WIDTH,
        "center_y": 480 * GLOBAL_SCALE,
        "assets": ["tree.png", "tree2.png"],
        "enemy": ENEMY_LIST["tank"],
        "player": "donky",
        "sfx_click": AUDIO.SOUND["ui_click"]["name"],
        "sfx_gain": AUDIO.SOUND["ui_click"]["gain"],
        "bgm_name": AUDIO.SOUND["bgm_3"]["name"],
        "bgm_gain": AUDIO.SOUND["bgm_3"]["gain"]
    },
    {
        "name": "CHINA",
        "level": 3,
        "img_name": "icon3.png",
        "center_x": 870 / 1280 * SCREEN_WIDTH,
        "center_y": 420 * GLOBAL_SCALE,
        "assets": ["cactus256.png", "tree.png"],
        "enemy": ENEMY_LIST["tank"],
        "player": "donky",
        "sfx_click": AUDIO.SOUND["ui_click"]["name"],
        "sfx_gain": AUDIO.SOUND["ui_click"]["gain"],
        "bgm_name": AUDIO.SOUND["bgm_3"]["name"],
        "bgm_gain": AUDIO.SOUND["bgm_3"]["gain"]
    },
    {
        "name": "OCEAN",
        "level": 4,
        "img_name": "icon4.png",
        "center_x": 1206 / 1280 * SCREEN_WIDTH,
        "center_y": 169 * GLOBAL_SCALE,
        "assets": ["cactus256.png", "tree.png"],
        "enemy": ENEMY_LIST["tank"],
        "player": "donky",
        "sfx_click": AUDIO.SOUND["ui_click"]["name"],
        "sfx_gain": AUDIO.SOUND["ui_click"]["gain"],
        "bgm_name": AUDIO.SOUND["bgm_3"]["name"],
        "bgm_gain": AUDIO.SOUND["bgm_3"]["gain"]
    },
    {
        "name": "BRAZIL",
        "level": 5,
        "img_name": "icon5.png",
        "center_x": 370 / 1280 * SCREEN_WIDTH,
        "center_y": 180 * GLOBAL_SCALE,
        "assets": ["cactus256.png", "tree.png"],
        "enemy": ENEMY_LIST["tank"],
        "player": "donky",
        "sfx_click": AUDIO.SOUND["ui_click"]["name"],
        "sfx_gain": AUDIO.SOUND["ui_click"]["gain"],
        "bgm_name": AUDIO.SOUND["bgm_3"]["name"],
        "bgm_gain": AUDIO.SOUND["bgm_3"]["gain"]
    },
    {
        "name": "USA",
        "level": 6,
        "img_name": "icon6.png",
        "center_x": 140 / 1280 * SCREEN_WIDTH,
        "center_y": 340 * GLOBAL_SCALE,
        "assets": ["cactus256.png", "tree.png"],
        "enemy": ENEMY_LIST["tank"],
        "player": "donky",
        "sfx_click": AUDIO.SOUND["ui_click"]["name"],
        "sfx_gain": AUDIO.SOUND["ui_click"]["gain"],
        "bgm_name": AUDIO.SOUND["bgm_3"]["name"],
        "bgm_gain": AUDIO.SOUND["bgm_3"]["gain"]
    },
]

# TODO: Add missing details
GOLD_LIST = [
    {
        "name": "Gold",
        "img_name": "",
        "value": 10,
        "sfx_pickup": AUDIO.SOUND["gold_pickup_1"]["name"],
        "sfx_pickup_gain": AUDIO.SOUND["gold_pickup_1"]["gain"]
    }
]

# Scaling
CHARACTER_SCALING = 1 * GLOBAL_SCALE
BULLET_SCALING = 1 * GLOBAL_SCALE
# This scales enemy sprites, always multiply by SCREEN_HEIGHT
ENEMY_SCALING = 0.001*SCREEN_HEIGHT
BG_SCALING = 1.0 * GLOBAL_SCALE
GOLD_SCALING = 0.5 * GLOBAL_SCALE
WEAPON_SCALING = 0.1 * GLOBAL_SCALE

# Sprite Angle
SPRITE_PLAYER_INIT_ANGLE = 0
WEAPON_INIT_ANGLE = -90


class LEVEL1:
    assets = ["tree.png", "bush.png", "cactus256.png", "tree2.png"]


# Player
class PLAYER:
    MAX_HP = 3
    START_HP = 3
    DEATH_HP = 0
    SFX_DEATH = {
        "name": AUDIO.SOUND["player_death"]["name"],
        "gain": AUDIO.SOUND["player_death"]["gain"]
    }
    SFX_HIT = {
        "name": AUDIO.SOUND["player_hit"]["name"],
        "gain": AUDIO.SOUND["player_hit"]["gain"]
    }


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
        "reload_rate": 1,
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

# GUI
GUI = {
    "Weapon": {
        "center_x": (SCREEN_WIDTH / 5) + 500,
        "center_y": SCREEN_HEIGHT - 90
    }
}

# Speed
SPEED_SCROLLING = -10
SPEED_PLAYER = 8


class DEATH:
    """ Reasons for death/despawn """
    OOB = 0
    COLLISION = 1
    KILLED = 2
    PICKED_UP = 3


# Menu
MENU_BACKGROUND_COLOR = arcade.csscolor.DIM_GREY
MENU_FONT_SIZE = 30

# Game View
GAME_BACKGROUND_COLOR = arcade.csscolor.DARK_GREEN


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
