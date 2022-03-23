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
            cls.gold = 0
            Tracker.gold = cls.gold

        if level:
            cls.level_data = {
                1: {"score": 0, "passed": 0},
                2: {"score": 0, "passed": 0},
                3: {"score": 0, "passed": 0},
                4: {"score": 0, "passed": 0},
                5: {"score": 0, "passed": 0},
                6: {"score": 0, "passed": 0},
            }

        if loadout:
            cls.loadout = {"rifle": 0, "Shotgun": 0, "RGB": 0}

        # Write changes
        cls.update_data()

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

        if Tracker.score < current_highscore:
            cls.level_data[level]["score"] = Tracker.score

            # Write changes
            cls.write_data()

    @classmethod
    def update_loadout(cls, weapon, gun_level):

        current_gun_level = cls.level_data[weapon]

        if current_gun_level != gun_level:
            cls.level_data[weapon] = gun_level

            # Write changes
            cls.write_data()



