import arcade
import random
import constants as C


class Audio():
    """
    Audio Class

    ...

    Attributes
    ----------
    bgm_list: list
        List of all background music sounds

    Class Methods
    -------
    load_sfx_ui()
        Load all ui sfx
    load_bgm()
        Load all background music sounds
    load_sfx_gold_pickup()
        Load all gold pickup sfx
    load_sfx_player_weapon_shoot()
        Load all player weapon shoot sfx
    load_sfx_enemy_weapon_shoot()
        Load all enemy weapon shoot sfx
    load_sfx_player_death()
        Load all player death sfx
    load_sfx_enemy_death()
        Load all enemy death sfx
    load_sfx_player_hit()
        Load all player hit sfx
    load_sfx_enemy_hit()
        Load all enemy hit sfx
    play_sound(cls, requested_sound: arcade.Sound) -> Player | None
        Play sound
    play_rand_sound(cls, requested_sound_list: list) -> Player | None
        Play random sound from list
    stop_sound(requested_stream)
        Stop sound playback

    Method
    ------
    find_gain(requested_sound: arcade.Sound, sound_list: list, master_list: list)
        Find the sound from the list and return gain
    """

    # Volume class attribute
    master_volume = C.AUDIO.MASTER_VOLUME
    bgm_volume = C.AUDIO.BGM_VOLUME
    sfx_volume = C.AUDIO.SFX_VOLUME

    # Master sound list class attribute
    master_list = []
    bgm_list = []
    sfx_list = []
    check_list = [
        [bgm_list, bgm_volume],
        [sfx_list, sfx_volume]
    ]

    # UI sound list class attribute
    sfx_ui_list = []

    # Gold sound list class attribute
    sfx_gold_pickup_list = []

    # Player sound list class attribute
    sfx_player_weapon_shoot_list = []
    sfx_player_hit_list = []
    sfx_player_death_list = []

    # Enemy sound list class attribute
    sfx_enemy_weapon_shoot_list = []
    sfx_enemy_hit_list = []
    sfx_enemy_death_list = []

    @classmethod
    def __init__(cls):
        """ Initialize and load all sounds """

        cls.load_sfx_ui()
        cls.load_bgm()

        cls.load_sfx_gold_pickup()

        cls.load_sfx_player_weapon_shoot()
        cls.load_sfx_enemy_weapon_shoot()

        cls.load_sfx_player_death()
        cls.load_sfx_enemy_death()

        cls.load_sfx_player_hit()
        cls.load_sfx_enemy_hit()

    @classmethod
    def load_sfx_ui(cls):
        """ Load all ui sfx """

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Loading: UI sfx")
        for monument in C.MAP_MONUMENTS_LIST:
            sound = None
            file_name = "ui/" + monument["sfx_click"]
            for sfx_dict in cls.sfx_list:
                if sfx_dict["file_name"] == file_name:
                    sound = sfx_dict["sound"]
                    break
            if sound is None:
                sound = arcade.load_sound(
                    C.AUDIO.FOLDER + file_name)

            sfx_dict = {
                "sound": sound,
                "file_name": file_name
            }
            cls.sfx_list.append(sfx_dict)

            # Append sound and gain to master list
            master_sound_dict = {
                "sound": sound,
                "gain": monument["sfx_gain"]
            }
            cls.master_list.append(master_sound_dict)

            # Append monument name and sound to ui list
            sound_dict = {
                "ui_name": monument["name"],
                "sound": sound
            }
            cls.sfx_ui_list.append(sound_dict)
        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Master sound list: ", cls.master_list)
            print("SFX list: ", cls.sfx_list)
            print("SFX UI list: ", cls.sfx_ui_list)
            print("Complete: UI sfx")

    @classmethod
    def load_bgm(cls):
        """ Load all background music sounds """

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Loading: BGM")
        for view in C.VIEW_LIST:
            sound = arcade.load_sound(
                C.AUDIO.FOLDER + "bgm/" + view["bgm_name"])

            # Append sound and gain to master list
            master_sound_dict = {
                "sound": sound,
                "gain": view["bgm_gain"]
            }
            cls.master_list.append(master_sound_dict)

            # Append map and sound to bgm list
            sound_dict = {
                "view_name": view["name"],
                "sound": sound
            }
            cls.bgm_list.append(sound_dict)

        for monument in C.MAP_MONUMENTS_LIST:
            sound = arcade.load_sound(
                C.AUDIO.FOLDER + "bgm/" + monument["bgm_name"])

            # Append sound and gain to master list
            master_sound_dict = {
                "sound": sound,
                "gain": monument["bgm_gain"]
            }
            cls.master_list.append(master_sound_dict)

            # Append map and sound to bgm list
            sound_dict = {
                "view_name": monument["name"],
                "sound": sound
            }
            cls.bgm_list.append(sound_dict)

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Master sound list: ", cls.master_list)
            print("BGM list: ", cls.bgm_list)
            print("Complete: BGM")

    @classmethod
    def load_sfx_gold_pickup(cls):
        """" Load all gold pickup sfx """

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Loading: Gold pickup sfx")
        for gold in C.GOLD_LIST:
            sound = None
            file_name = "gold/" + gold["sfx_pickup"]
            for sfx_dict in cls.sfx_list:
                if sfx_dict["file_name"] == file_name:
                    sound = sfx_dict["sound"]
                    break
            if sound is None:
                sound = arcade.load_sound(
                    C.AUDIO.FOLDER + file_name)

            # Append weapon name and sound to gold pickup list
            sound_dict = {
                "gold_name": gold["name"],
                "sound": sound
            }
            cls.sfx_gold_pickup_list.append(sound_dict)

            sfx_dict = {
                "sound": sound,
                "file_name": file_name
            }
            cls.sfx_list.append(sfx_dict)

            # Append sound and gain to master list
            master_sound_dict = {
                "sound": sound,
                "gain": gold["sfx_pickup_gain"]
            }
            cls.master_list.append(master_sound_dict)
        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Master sound list: ", cls.master_list)
            print("SFX list: ", cls.sfx_list)
            print("SFX Gold pickup list: ", cls.sfx_gold_pickup_list)
            print("Complete: Gold pickup sfx")

    @classmethod
    def load_sfx_player_weapon_shoot(cls):
        """ Load all player weapon shoot sfx """

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Loading: Player weapon shoot sfx")
        for weapon in C.WEAPON_LIST:
            sound_list = []
            for i in range(0, len(weapon["sfx_single_shot_list"])):
                sound = None
                file_name = "weapon/" + weapon["img_name"] + "/" + \
                    weapon["sfx_single_shot_list"][i]
                for sfx_dict in cls.sfx_list:
                    if sfx_dict["file_name"] == file_name:
                        sound = sfx_dict["sound"]
                        break
                if sound is None:
                    sound = arcade.load_sound(
                        C.AUDIO.FOLDER + file_name)

                sfx_dict = {
                    "sound": sound,
                    "file_name": file_name
                }
                sound_list.append(sound)
                cls.sfx_list.append(sfx_dict)

                # Append sound and gain to master list
                master_sound_dict = {
                    "sound": sound,
                    "gain": weapon["sfx_single_shot_vol_gain_list"][i]
                }
                cls.master_list.append(master_sound_dict)

            # Append weapon name and sound to player weapon shoot list
            sound_dict = {
                "weapon_name": weapon["name"],
                "sound": sound_list
            }
            cls.sfx_player_weapon_shoot_list.append(sound_dict)
        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Master sound list: ", cls.master_list)
            print("SFX list: ", cls.sfx_list)
            print("SFX Player weapon shoot list: ",
                  cls.sfx_player_weapon_shoot_list)
            print("Complete: Player weapon shoot sfx")

    @classmethod
    def load_sfx_enemy_weapon_shoot(cls):
        """ Load all enemy weapon shoot sfx """

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Loading: Enemy weapon shoot sfx")
        for weapon in C.ENEMY_WEAPON_LIST:
            sound_list = []
            for i in range(0, len(weapon["sfx_single_shot_list"])):
                sound = None
                file_name = "weapon/" + weapon["folder_name"] + "/" + \
                    weapon["sfx_single_shot_list"][i]
                for sfx_dict in cls.sfx_list:
                    if sfx_dict["file_name"] == file_name:
                        sound = sfx_dict["sound"]
                        break
                if sound is None:
                    sound = arcade.load_sound(
                        C.AUDIO.FOLDER + file_name)

                sfx_dict = {
                    "sound": sound,
                    "file_name": file_name
                }
                sound_list.append(sound)
                cls.sfx_list.append(sfx_dict)

                # Append sound and gain to master list
                master_sound_dict = {
                    "sound": sound,
                    "gain": weapon["sfx_single_shot_vol_gain_list"][i]
                }
                cls.master_list.append(master_sound_dict)

            # Append weapon name and sound to enemy weapon shoot list
            sound_dict = {
                "weapon_name": weapon["name"],
                "sound": sound_list
            }
            cls.sfx_enemy_weapon_shoot_list.append(sound_dict)
        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Master sound list: ", cls.master_list)
            print("SFX list: ", cls.sfx_list)
            print("SFX Enemy weapon shoot list: ",
                  cls.sfx_enemy_weapon_shoot_list)
            print("Complete: Enemy weapon shoot sfx")

    @classmethod
    def load_sfx_player_death(cls):
        """ Load all player death sfx """

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Loading: Player death sfx")
        sound = None
        file_name = "death/" + C.PLAYER.SFX_DEATH["name"]
        for sfx_dict in cls.sfx_list:
            if sfx_dict["file_name"] == file_name:
                sound = sfx_dict["sound"]
                break
        if sound is None:
            sound = arcade.load_sound(
                C.AUDIO.FOLDER + file_name)

        sfx_dict = {
            "sound": sound,
            "file_name": file_name
        }
        cls.sfx_player_death_list.append(sound)
        cls.sfx_list.append(sfx_dict)

        # Append sound and gain to master list
        master_sound_dict = {
            "sound": sound,
            "gain": C.PLAYER.SFX_DEATH["gain"]
        }
        cls.master_list.append(master_sound_dict)
        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Master sound list: ", cls.master_list)
            print("SFX list: ", cls.sfx_list)
            print("SFX Player death list: ",
                  cls.sfx_player_death_list)
            print("Complete: Player death sfx")

    @classmethod
    def load_sfx_enemy_death(cls):
        """ Load all enemy death sfx """

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Loading: Enemy death sfx")
        for enemy in C.ENEMY_LIST.values():
            sound_list = []
            for i in range(0, len(enemy["sfx_death"])):
                sound = None
                file_name = "death/" + enemy["sfx_death"][i]
                for sfx_dict in cls.sfx_list:
                    if sfx_dict["file_name"] == file_name:
                        sound = sfx_dict["sound"]
                        break
                if sound is None:
                    sound = arcade.load_sound(
                        C.AUDIO.FOLDER + file_name)

                sfx_dict = {
                    "sound": sound,
                    "file_name": file_name
                }
                sound_list.append(sound)
                cls.sfx_list.append(sfx_dict)

                # Append sound and gain to master list
                master_sound_dict = {
                    "sound": sound,
                    "gain": enemy["sfx_death_gain"][i]
                }
                cls.master_list.append(master_sound_dict)

            # Append weapon name and sound to enemy death list
            sound_dict = {
                "enemy_name": enemy["name"],
                "sound": sound_list
            }
            cls.sfx_enemy_death_list.append(sound_dict)
        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Master sound list: ", cls.master_list)
            print("SFX list: ", cls.sfx_list)
            print("SFX Enemy death list: ",
                  cls.sfx_enemy_death_list)
            print("Complete: Enemy death sfx")

    @classmethod
    def load_sfx_player_hit(cls):
        """ Load all player hit sfx """

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Loading: Player hit sfx")
        sound = None
        file_name = "hit/player/" + C.PLAYER.SFX_HIT["name"]
        for sfx_dict in cls.sfx_list:
            if sfx_dict["file_name"] == file_name:
                sound = sfx_dict["sound"]
                break
        if sound is None:
            sound = arcade.load_sound(
                C.AUDIO.FOLDER + file_name)

        sfx_dict = {
            "sound": sound,
            "file_name": file_name
        }
        cls.sfx_player_hit_list.append(sound)
        cls.sfx_list.append(sfx_dict)

        # Append sound and gain to master list
        master_sound_dict = {
            "sound": sound,
            "gain": C.PLAYER.SFX_HIT["gain"]
        }
        cls.master_list.append(master_sound_dict)
        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Master sound list: ", cls.master_list)
            print("SFX list: ", cls.sfx_list)
            print("SFX Player hit list: ",
                  cls.sfx_player_hit_list)
            print("Complete: Player hit sfx")

    @classmethod
    def load_sfx_enemy_hit(cls):
        """ Load all enemy hit sfx """

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Loading: Enemy hit sfx")
        for enemy in C.ENEMY_LIST.values():
            sound_list = []
            for i in range(0, len(enemy["sfx_hit"])):
                sound = None
                file_name = "hit/enemy/" + enemy["sfx_hit"][i]
                for sfx_dict in cls.sfx_list:
                    if sfx_dict["file_name"] == file_name:
                        sound = sfx_dict["sound"]
                        break
                if sound is None:
                    sound = arcade.load_sound(
                        C.AUDIO.FOLDER + file_name)

                sfx_dict = {
                    "sound": sound,
                    "file_name": file_name
                }
                sound_list.append(sound)
                cls.sfx_list.append(sfx_dict)

                # Append sound and gain to master list
                master_sound_dict = {
                    "sound": sound,
                    "gain": enemy["sfx_hit_gain"][i]
                }
                cls.master_list.append(master_sound_dict)

            # Append enemy name and sound to enemy hit list
            sound_dict = {
                "enemy_name": enemy["name"],
                "sound": sound_list
            }
            cls.sfx_enemy_hit_list.append(sound_dict)
        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Master sound list: ", cls.master_list)
            print("SFX list: ", cls.sfx_list)
            print("SFX Enemy hit list: ",
                  cls.sfx_enemy_hit_list)
            print("Complete: Enemy hit sfx")

    @classmethod
    def play_sound(cls, requested_sound: arcade.Sound):
        """ Play sound """

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Music request: ", requested_sound)
            print("Master sound list: ", cls.master_list)
        # Find & play sound
        for check_item in cls.check_list:
            sound_gain = cls.find_gain(
                requested_sound, check_item[0], cls.master_list)
            if not sound_gain is None:
                return arcade.play_sound(requested_sound, min(sound_gain + check_item[1], 1) * cls.master_volume)

    @classmethod
    def play_rand_sound(cls, requested_sound_list: list):
        """ Play random sound from list """

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Music request: ", requested_sound_list)
            print("Master sound list: ", cls.master_list)
        rand_index = random.randint(
            0, len(requested_sound_list) - 1)
        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Selected music: ", cls.requested_sound_list[rand_index])
        return Audio.play_sound(requested_sound_list[rand_index])

    @classmethod
    def stop_sound(cls, requested_stream):
        """ Stop sound playback """

        if C.DEBUG.ALL or C.DEBUG.AUDIO:
            print("Music stop request: ", requested_stream)
        arcade.stop_sound(requested_stream)
        requested_stream = None

    def find_gain(requested_sound: arcade.Sound, sound_list: list, master_list: list):
        """ Find the sound from the list and return gain """

        for sfx_dict in sound_list:
            if requested_sound == sfx_dict["sound"]:
                for dict_item in master_list:
                    if dict_item["sound"] == requested_sound:
                        return dict_item["gain"]
        return None
