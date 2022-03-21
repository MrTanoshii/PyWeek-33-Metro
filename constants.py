""" Include all constant values """

# Window Size and Title
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "REVƎЯ"

# Scaling
CHARACTER_SCALING = 1
BULLET_SCALING = 0.3
ENEMY_SCALING = 1
BG_SCALING = 1.0
GOLD_SCALING = 1.0

# Sprite Angle
SPRITE_PLAYER_INIT_ANGLE = 90


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

# Speed
SPEED_SCROLLING = -10


class DEATH:
    """ Reasons for death/despawn """
    OOB = 0
    COLLISION = 1
    KILLED = 2
