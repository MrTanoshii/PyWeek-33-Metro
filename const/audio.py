_PLAYER_WEAPON = {
    "weapon_revolver_1": {
        "name": "522270__filmmakersmanual__gun-firing-from-a-distance-15.wav",
        "gain": -0.7
    },
    "weapon_revolver_2": {
        "name": "522495__filmmakersmanual__gun-shots-from-a-distance-14.wav",
        "gain": -0.7
    },
    "weapon_revolver_3": {
        "name": "522541__filmmakersmanual__gun-shots-from-a-distance-20.wav",
        "gain": -0.7
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

_PLAYER_SFX = {
    "player_death": {
        "name": "396798__scorpion67890__male-death-1.ogg",
        "gain": -0.3
    },
    "player_hit": {
        "name": "553285__nettoi__hurt4.ogg",
        "gain": -0.1
    },
}

_ENEMY_WEAPON = {
    "weapon_tank_1": {
        "name": "127845__garyq__tank-fire-mixed.wav",
        "gain": -0.4
    },
    "weapon_heli_1": {
        "name": "522470__filmmakersmanual__heavy-machine-gun.wav",
        "gain": 0
    },
    "weapon_orca_1": {
        "name": "411852__devilfish101__monotron-whalesong.wav",
        "gain": .4
    }
}

_ENEMY_DEATH = {
    "enemy_death_tank_1": {
        "name": "587183__derplayer__explosion-03.wav",
        "gain": -0.85
    },
    "enemy_death_tank_2": {
        "name": "587184__derplayer__explosion-02.wav",
        "gain": -0.85
    },
    "soldier_death_1": {
        "name": "396799__scorpion67890__male-death-2.ogg",
        "gain": -0.85
    },
    "soldier_death_2": {
        "name": "396801__scorpion67890__male-death-4.ogg",
        "gain": -0.85
    },
    "orca_death_1": {
        "name": "88449__davidou__baleines.wav",
        "gain": -0.65
    },
    "bear_death_1": {
        "name": "49464__enochrooted__toni-deepgrowl.wav",
        "gain": -0.4
    }
}

_ENEMY_HIT = {
    "enemy_hit_1": {
        "name": "260435__roganmcdougald__metal-impact-ceramic-piece-in-sink.wav",
        "gain": -0.7
    },
    "bear_hit_1": {
        "name": "253471__groadr__growl.mp3",
        "gain": -0.7
    }
}

_BGM = {
    "bgm_1": {
        "name": "427441__kiluaboy__clouds.wav",
        "gain": 0
    },
    "bgm_2": {
        "name": "428857__supervanz__arpegio01-loop.wav",
        "gain": -0.5
    },
    "bgm_3": {
        "name": "428858__supervanz__duskwalkin-loop.wav",
        "gain": -0.5
    },
}

_UI_SFX = {
    "ui_click": {
        "name": "388713__totalcult__finger-click-02.wav",
        "gain": -.9
    },
    "ui_meow": {
        "name": "415209__inspectorj__cat-screaming-a.wav",
        "gain": -.5
    }
}

_GOLD_SFX = {
    "gold_pickup_1": {
        "name": "402767__matrixxx__retro-coin-03.wav",
        "gain": -0.73
    },
}


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

    SOUND = {}

    @classmethod
    def _add_dict(cls, sound_dict_list: list):
        for sound_dict in sound_dict_list:
            for key, value in sound_dict.items():
                cls.SOUND[key] = value


AUDIO._add_dict([_BGM, _ENEMY_WEAPON, _PLAYER_WEAPON,
                _ENEMY_DEATH, _ENEMY_HIT, _GOLD_SFX, _PLAYER_SFX, _UI_SFX])
