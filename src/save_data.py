import json

import src.const as C

from src.tracker import Tracker

from src.view.map import MapView


class GameData:
    gold = None
    level_data = {}
    loadout = {}
    story = {}

    def __init__(self):
        pass

    # Load game data
    @classmethod
    def read_data(cls):
        try:
            with open("src/resources/gamedata.json", "r", encoding="utf-8") as file:
                _data = json.load(file)
        except FileNotFoundError:
            print("ERROR 0: Regenerating game data")
            cls.reset_data(gold=True, level=True, loadout=True, story=True)
            _data = False

        if _data:

            try:
                cls.gold = _data["coins"]
                if cls.gold is None:
                    print("ERROR 2: Regenerating level data")
                    cls.reset_data(gold=True)
                    cls.read_data()
            except KeyError:
                print("ERROR 1: Regenerating level data")
                cls.reset_data(gold=True)
                cls.read_data()

            try:
                cls.level_data = _data["leveldata"]
                if cls.level_data is None:
                    print("ERROR 2: Regenerating level data")
                    cls.reset_data(level=True)
                    cls.read_data()
            except KeyError:
                print("ERROR 1: Regenerating level data")
                cls.reset_data(level=True)
                cls.read_data()

            try:
                cls.loadout = _data["loadout"]
                if cls.loadout is None:
                    print("ERROR 2: Regenerating loadout")
                    cls.reset_data(loadout=True)
                    cls.read_data()
            except KeyError:
                print("ERROR 1: Regenerating loadout")
                cls.reset_data(loadout=True)
                cls.read_data()

            try:
                cls.story = _data["story"]
                if cls.story is None:
                    print("ERROR 2: Regenerating story")
                    cls.reset_data(story=True)
                    cls.read_data()
            except KeyError:
                print("ERROR 1: Regenerating story")
                cls.reset_data(story=True)
                cls.read_data()

        else:
            cls.read_data()

    # Save game data
    @classmethod
    def write_data(cls):
        with open("src/resources/gamedata.json", "w", encoding="utf-8") as file:
            _data = json.dumps({
                "coins": cls.gold,
                "leveldata": cls.level_data,
                "loadout": cls.loadout,
                "story": cls.story})
            file.write(_data)

    @classmethod
    def reset_data(cls, gold=False, level=False, loadout=False, story=False):
        # Reset all data
        if gold:
            cls.gold = 100

        if level:
            cls.level_data = {
                1: {"score": 0, "passed": 0, "locked": 1},
                2: {"score": 0, "passed": 0, "locked": 1},
                3: {"score": 0, "passed": 0, "locked": 1},
                4: {"score": 0, "passed": 0, "locked": 1},
                5: {"score": 0, "passed": 0, "locked": 1},
                6: {"score": 0, "passed": 0, "locked": 1},
            }

        if loadout:
            cls.loadout = {
                "Revolver": {
                    "lvl": 1
                },
                "Rifle":  {
                    "lvl": 0
                },
                "Shotgun":  {
                    "lvl": 0
                },
                "RPG":  {
                    "lvl": 0
                }
            }

        if story:
            cls.story = {"0": 1, "1": 0, "2": 0,
                         "3": 0, "4": 0, "5": 0, "6": 0}

        # Write changes
        cls.write_data()

    @classmethod
    def update_gold(cls, amount):

        cls.gold = amount

        # Write changes
        cls.write_data()

    @classmethod
    def deposit_gold(cls):

        current_gold = cls.gold

        if current_gold != Tracker.gold:
            cls.gold += Tracker.gold

            Tracker.gold = 0

            # Write changes
            cls.write_data()

    @classmethod
    def update_highscore(cls, level):

        current_highscore = cls.level_data[str(level)]["score"]

        if Tracker.score > current_highscore:
            cls.level_data[str(level)]["score"] = Tracker.score

            if cls.level_data[str(level)]["score"] > 100 * level:
                cls.level_data[str(level)]["passed"] = 1
                cls.story[str(level)] = 1
                if level < len(C.MAP_MONUMENTS_LIST):
                    cls.level_data[str(level+1)]["locked"] = 0
                cls.story[str(level)] = 1

                # Update map icons
                MapView.update_monument_list()
                MapView.update_step_list()

            # Write changes
            cls.write_data()

    @classmethod
    def update_loadout(cls, name, lvl):
        for saved_weapon in cls.loadout:
            if saved_weapon == name:
                cls.loadout[saved_weapon]["lvl"] = lvl
                # Write changes
                cls.write_data()
                break

    @classmethod
    def update_steps(cls, story_id: str, status: int):

        current_story_status = cls.story[story_id]

        if current_story_status != status:
            cls.story[story_id] = status

            # update levels
            cls.update_levels(int(story_id)+1)

            # Write changes
            cls.write_data()

    @classmethod
    def update_levels(cls, level: int):
        # player passed the level

        if level <= 6:

            cls.level_data[str(level)]["locked"] = 0

        # Write changes
        cls.write_data()
