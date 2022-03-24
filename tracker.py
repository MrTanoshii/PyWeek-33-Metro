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
        Decremenet the game score
    """

    # Gold class attribute
    gold = 0

    # Score class attribute
    score = 0

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
    def reset_trackers(cls):
        cls.score = 0
        cls.gold = 0
