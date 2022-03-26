import json
from tracker import Tracker


class GameData:
    gold = None
    level_data = None
    loadout = None

    def __init__(self):
        pass

    # Load game data
    @classmethod
    def read_data(cls):
        try:
            with open("resources/gamedata.json", "r") as file:
                _data = json.load(file)
        except FileNotFoundError:
            print("ERROR 0: Regenerating game data")
            cls.reset_data()
            _data = False

        if _data:

            try:
                cls.gold = _data["coins"]
                if cls.gold is None:
                    print("ERROR 2: Regenerating level data")
                    cls.reset_data(gold=True, level=False, loadout=False)
                    cls.read_data()
            except KeyError:
                print("ERROR 1: Regenerating level data")
                cls.reset_data(gold=True, level=False, loadout=False)
                cls.read_data()

            try:
                cls.level_data = _data["leveldata"]
                if cls.level_data is None:
                    print("ERROR 2: Regenerating level data")
                    cls.reset_data(gold=False, level=True, loadout=False)
                    cls.read_data()
            except KeyError:
                print("ERROR 1: Regenerating level data")
                cls.reset_data(gold=False, level=True, loadout=False)
                cls.read_data()

            try:
                cls.loadout = _data["loadout"]
                if cls.loadout is None:
                    print("ERROR 2: Regenerating loadout")
                    cls.reset_data(gold=False, level=False, loadout=True)
                    cls.read_data()
            except KeyError:
                print("ERROR 1: Regenerating loadout")
                cls.reset_data(gold=False, level=False, loadout=True)
                cls.read_data()

        else:
            cls.read_data()

    # Save game data
    @classmethod
    def write_data(cls):
        with open("resources/gamedata.json", "w") as file:
            _data = json.dumps({
                "coins": cls.gold,
                "leveldata": cls.level_data,
                "loadout": cls.loadout})
            file.write(_data)

    @classmethod
    def reset_data(cls, gold=True, level=True, loadout=True):
        # Reset all data
        if gold:
            cls.gold = 100

        if level:
            cls.level_data = {
                1: {"score": 0, "passed": 0, "locked": 0},
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

            if cls.level_data[str(level)]["score"] > 100:
                # player passed the level
                cls.level_data[str(level)]["passed"] = 1

                cls.level_data[str(level+1)]["locked"] = 0

                # Update map icons
                from mapview import MapView
                MapView.update_monument_list()

            # Write changes
            cls.write_data()

    @classmethod
    def update_loadout(cls, name, lvl):
        for saved_weapon in cls.loadout:
            if saved_weapon == name:
                cls.loadout[saved_weapon]["lvl"] = lvl
                break

        # Write changes
        cls.write_data()
