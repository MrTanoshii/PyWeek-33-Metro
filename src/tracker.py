class Tracker():
    """
    Tracker Class

    ...

    Attributes
    ----------
    gold : int
        Hold the gold amount
    score : int
        Hold the game score

    Class Methods
    -------------
    increment_gold(value: int)
        Increment the gold amount
    decrement_gold(value: int)
        Decrement the gold amount
    increment_score(value: int)
        Increment the game score
    decrement_score(value: int)
        Decrement the game score
    trigger_easter_egg()
        Trigger easter egg reward
    reset()
        Reset all tracked values
    """

    # Gold class attribute
    gold = 0

    # Score class attribute
    score = 0

    # Score class attribute
    kills = 0

    # Easter egg class attribute
    easter_egg_found = False

    @classmethod
    def increment_gold(cls, value):
        cls.gold += value

    @classmethod
    def decrement_gold(cls, value):
        cls.gold -= value

    @classmethod
    def increment_score(cls, value):
        cls.score += value

    @classmethod
    def decrement_score(cls, value):
        cls.score -= value

    @classmethod
    def add_kill(cls):
        cls.kills += 1

    @classmethod
    def reset_trackers(cls):
        cls.score = 0
        cls.gold = 0
        cls.kills = 0

    @classmethod
    def trigger_easter_egg(cls):
        if not cls.easter_egg_found:
            cls.easter_egg_found = True
            cls.increment_gold(100)

    @classmethod
    def reset(cls):
        cls.gold = 0
        cls.score = 0
        cls.kills = 0
        cls.easter_egg_found = False
