import arcade

""" Include all constant values """

# Window Size and Title
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "REVƎЯ"
CENTER_POINTS = [[700, 450], [900, 450]]
DICT1 = {'EGYPT': [700, 450], 'INDIA': [900, 450]}
LIST1 = ['EGYPT', 'INDIA']


# Scaling
CHARACTER_SCALING = 1
BULLET_SCALING = 0.15
# This scales enemy sprites, always multiply by SCREEN_HEIGHT
ENEMY_SCALING = 0.0005*SCREEN_HEIGHT
BG_SCALING = 1.0
GOLD_SCALING = 0.5

# Sprite Angle
SPRITE_PLAYER_INIT_ANGLE = 0


class LEVEL1:
    assets = ["tree.png", "bush.png"]


# Player
PLAYER_MAX_HP = 3
PLAYER_START_HP = PLAYER_MAX_HP
PLAYER_DEATH_HP = 0

# Player Gun
PLAYER_GUN_MAX_AMMO = 1000
PLAYER_GUN_BULLET_SPEED = 20
PLAYER_GUN_SHOOT_SPEED = 0.1
PLAYER_GUN_RELOAD_TIME = 3
PLAYER_GUN_DAMAGE = 1


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
