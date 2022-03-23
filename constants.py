import arcade

""" Include all constant values """

# Window Size and Title
SCREEN_WIDTH = 1240
SCREEN_HEIGHT = 720
SCREEN_TITLE = "REVƎЯ"
FULLSCREEN = False
CENTER_WINDOW = True

CURSOR_VISIBLE = False

DEBUG = False

GLOBAL_SCALE = SCREEN_WIDTH / 1280

MAP_MONUMENTS_LIST = [
    {
        "name": "EGYPT",
        "level": 1,
        "img_name": "icon1.png",
        "center_x": 650 * GLOBAL_SCALE,
        "center_y": 325 * GLOBAL_SCALE,
        "assets": ["pyramids.png", "cactus.png"],
        "enemy": "tank",
        "player": "donky"
    },
    {
        "name": "MOSCOW",
        "level": 2,
        "img_name": "icon2.png",
        "center_x": 700 / 1280 * SCREEN_WIDTH,
        "center_y": 480 * GLOBAL_SCALE,
        "assets": ["tree.png", "tree2.png"],
        "enemy": "tank",
        "player": "donky"
    },
    {
        "name": "CHINA",
        "level": 3,
        "img_name": "icon3.png",
        "center_x": 870 / 1280 * SCREEN_WIDTH,
        "center_y": 420 * GLOBAL_SCALE,
        "assets": ["cactus256.png", "tree.png"],
        "enemy": "tank",
        "player": "donky"
    },
    {
        "name": "OCEAN",
        "level": 4,
        "img_name": "icon4.png",
        "center_x": 1206 / 1280 * SCREEN_WIDTH,
        "center_y": 169 * GLOBAL_SCALE,
        "assets": ["cactus256.png", "tree.png"],
        "enemy": "tank",
        "player": "donky"
    },
    {
        "name": "BRAZIL",
        "level": 5,
        "img_name": "icon5.png",
        "center_x": 370 / 1280 * SCREEN_WIDTH,
        "center_y": 180 * GLOBAL_SCALE,
        "assets": ["cactus256.png", "tree.png"],
        "enemy": "tank",
        "player": "donky"
    },
    {
        "name": "USA",
        "level": 6,
        "img_name": "icon6.png",
        "center_x": 140 / 1280 * SCREEN_WIDTH,
        "center_y": 340 * GLOBAL_SCALE,
        "assets": ["cactus256.png", "tree.png"],
        "enemy": "tank",
        "player": "donky"
    },
]

ENEMIES = {
    "tank": {
        "animation_speed": 0.02,
        "scale": 1*GLOBAL_SCALE,
        "speed": -2,
        "spawn_rate": 1,
        "health": 10,
        "weapon": "RPG",
        "shooting_speed": 5,  # in seconds
        "bullet_scale": 1,
        "bullet_speed": 20,
        "damage": 1,
        "barrel": (0, 80)
    },
}

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
PLAYER_MAX_HP = 3
PLAYER_START_HP = PLAYER_MAX_HP
PLAYER_DEATH_HP = 0

# Player Weapon

FIRE_MODE = {
    "SEMI_AUTO": 0,
    "FULL_AUTO": 1,
    "BURST": 2,
}

FIRE_TYPE = {
    "LINE": 0,
    "CONE": 1
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
        "fire_mode": FIRE_MODE["FULL_AUTO"],
        "fire_type": FIRE_TYPE["LINE"],
        "max_ammo": 30,
        "bullet_texture_amount": 39,
        "bullet_speed": 25,
        "bullet_damage": 3,
        "bullet_scale": .3,
        "shoot_time": 0.1,
        "reload_time": 1.5,
        "reload_rate": 30
    },
    {
        "name": "Shotgun",
        "img_name": "weapon_ak",
        "width": 640,
        "height": 360,
        "scale": 3*WEAPON_SCALING,
        "center_x": 0,
        "center_y": 0,
        "fire_mode": FIRE_MODE["FULL_AUTO"],
        "fire_type": FIRE_TYPE["CONE"],
        "max_ammo": 8,
        "bullet_texture_amount": 1,
        "bullet_speed": 18,
        "bullet_damage": 2,
        "bullet_scale": .5,
        "shoot_time": 0.3,
        "reload_time": 0.8,
        "reload_rate": 1
    },
    {
        "name": "RPG",
        "img_name": "weapon_rpg",
        "width": 640,
        "height": 360,
        "scale": 3*WEAPON_SCALING,
        "center_x": 0,
        "center_y": 0,
        "fire_mode": FIRE_MODE["SEMI_AUTO"],
        "fire_type": FIRE_TYPE["LINE"],
        "max_ammo": 1,
        "bullet_texture_amount": 24,
        "bullet_speed": 21,
        "bullet_damage": 15,
        "bullet_scale": 2,
        "shoot_time": 0.3,
        "reload_time": 2.5,
        "reload_rate": 1
    }
]

# GUI
GUI = {
    "Weapon": {
        "center_x": (SCREEN_WIDTH / 5) + 500,
        "center_y": SCREEN_HEIGHT - 90
    }
}

PLAYER_GUN_MAX_AMMO = 1000
PLAYER_GUN_BULLET_SPEED = 20
PLAYER_GUN_SHOOT_SPEED = 0.1
PLAYER_GUN_RELOAD_TIME = 3
PLAYER_GUN_DAMAGE = 1

# Speed
SPEED_SCROLLING = -10
SPEED_PLAYER = 8


class DEATH:
    """ Reasons for death/despawn """
    OOB = 0
    COLLISION = 1
    KILLED = 2
    PICKED_UP = 3


# Audio
MASTER_VOLUME = 0.1
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
