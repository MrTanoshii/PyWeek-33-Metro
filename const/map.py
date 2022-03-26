from const.scale import *
from const.audio import *
from const.enemy import *


# TODO: Refactor LEVEL1 class into MAP_MONUMENTS_LIST
class LEVEL1:
    assets = ["tree.png", "bush.png", "cactus256.png", "tree2.png"]


# TODO: Refactor SPEED_SCROLLING into MAP_MONUMENTS_LIST
SPEED_SCROLLING = -10

MAP = {
    "Cursor": {
        "offset_x": 20,
        "offset_y": -20
    }
}

MAP_MONUMENTS_LIST = [
    {
        "name": "EGYPT",
        "level": 1,
        "img_name": "icon1.png",
        "center_x": 650,
        "center_y": 325,
        "assets": ["pyramids.png", "cactus.png"],
        "enemy": [ENEMY_LIST["tank green"], ENEMY_LIST["soldier desert"]],
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
        "center_x": 700,
        "center_y": 480,
        "assets": ["tree.png", "tree2.png"],
        "enemy": [ENEMY_LIST["tank grey burning"], ENEMY_LIST["soldier forest"], ENEMY_LIST["bear ak"]],
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
        "center_x": 870,
        "center_y": 420,
        "assets": ["cactus256.png", "tree.png"],
        "enemy": [ENEMY_LIST["tank grey"], ENEMY_LIST["soldier polar"], ENEMY_LIST["martial artist"]],
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
        "center_x": 1206,
        "center_y": 169,
        "assets": ["cactus256.png", "tree.png"],
        "enemy": [ENEMY_LIST["bear polar"], ENEMY_LIST["soldier ocean"], ENEMY_LIST["orca"]],
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
        "center_x": 370,
        "center_y": 180,
        "assets": ["cactus256.png", "tree.png"],
        "enemy": [ENEMY_LIST["tank green"], ENEMY_LIST["soldier forest"], ENEMY_LIST["soldier desert"]],
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
        "center_x": 140,
        "center_y": 340,
        "assets": ["cactus256.png", "tree.png"],
        "enemy": [ENEMY_LIST["tank green"], ENEMY_LIST["soldier forest"], ENEMY_LIST["tank grey"]],
        "player": "donky",
        "sfx_click": AUDIO.SOUND["ui_click"]["name"],
        "sfx_gain": AUDIO.SOUND["ui_click"]["gain"],
        "bgm_name": AUDIO.SOUND["bgm_3"]["name"],
        "bgm_gain": AUDIO.SOUND["bgm_3"]["gain"]
    },
]

MAP_STEP_LIST = [
    {
        "type": "story",
        "story": 1,
        "center_x": 551,
        "center_y": 279,
    },
    {
        "type": "step",
        "center_x": 591,
        "center_y": 287,
    },
    # 2
    {
        "type": "step",
        "center_x": 694,
        "center_y": 360,
    },
    {
        "type": "step",
        "center_x": 650,
        "center_y": 381,
    },
    {
        "type": "story",
        "story": 2,
        "center_x": 608,
        "center_y": 400,
    },
    {
        "type": "step",
        "center_x": 631,
        "center_y": 424,
    },
    {
        "type": "step",
        "center_x": 655,
        "center_y": 436,
    },
    # 3
    {
        "type": "step",
        "center_x": 755,
        "center_y": 485,
    },    {
        "type": "step",
        "center_x": 772,
        "center_y": 449,
    },
    {
        "type": "step",
        "center_x": 761,
        "center_y": 418,
    },
    {
        "type": "story",
        "story": 3,
        "center_x": 784,
        "center_y": 390,
    },
    {
        "type": "step",
        "center_x": 820,
        "center_y": 392,
    },
    # 4
    {
        "type": "step",
        "center_x": 918,
        "center_y": 402,
    },
    {
        "type": "step",
        "center_x": 953,
        "center_y": 378,
    },
    {
        "type": "step",
        "center_x": 961,
        "center_y": 349,
    },
    {
        "type": "step",
        "center_x": 920,
        "center_y": 330,
    },
    {
        "type": "step",
        "center_x": 913,
        "center_y": 305,
    },
    {
        "type": "story",
        "story": 4,
        "center_x": 928,
        "center_y": 262,
    },
    {
        "type": "step",
        "center_x": 976,
        "center_y": 259,
    },
    {
        "type": "step",
        "center_x": 1022,
        "center_y": 270,
    },
    {
        "type": "step",
        "center_x": 1072,
        "center_y": 270,
    },
    {
        "type": "step",
        "center_x": 1119,
        "center_y": 246,
    },
    {
        "type": "step",
        "center_x": 1153,
        "center_y": 219,
    },
    # 5
    {
        "type": "step",
        "center_x": 1267,
        "center_y": 121,
    },
    {
        "type": "step",
        "center_x": 10,
        "center_y": 107,
    },
    {
        "type": "step",
        "center_x": 78,
        "center_y": 93,
    },
    {
        "type": "step",
        "center_x": 141,
        "center_y": 78,
    },
    {
        "type": "step",
        "center_x": 217,
        "center_y": 74,
    },
    {
        "type": "story",
        "story": 5,
        "center_x": 284,
        "center_y": 78,
    },
    {
        "type": "step",
        "center_x": 328,
        "center_y": 93,
    },
    {
        "type": "step",
        "center_x": 358,
        "center_y": 121,
    },
    # 6
    {
        "type": "step",
        "center_x": 313,
        "center_y": 227,
    },
    {
        "type": "step",
        "center_x": 267,
        "center_y": 244,
    },
    {
        "type": "story",
        "story": 6,
        "center_x": 235,
        "center_y": 260,
    },
    {
        "type": "step",
        "center_x": 179,
        "center_y": 286,
    },
    # 7
    {
        "type": "step",
        "center_x": 177,
        "center_y": 387,
    },
    {
        "type": "step",
        "center_x": 215,
        "center_y": 407,
    },
    {
        "type": "story",
        "story": 7,
        "center_x": 231,
        "center_y": 445,
    },
]

STEP_CONFS = {
    "step_scale": 0.3,
    "story_scale": 0.5,
    "story_scale_big": 0.7,
    "locked": (255, 64, 64),
    "unlocked": (64, 255, 64),
    "passed": (255, 255, 64),
}
