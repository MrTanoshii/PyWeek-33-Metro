class Tracker():
    gold = 0
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
