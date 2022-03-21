class Tracker():
    def __init__(self):
        self.score = 0

    def increment_score(self, value):
        self.score += value

    def decrement_score(self, value):
        self.score -= value
