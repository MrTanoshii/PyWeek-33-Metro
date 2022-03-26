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
