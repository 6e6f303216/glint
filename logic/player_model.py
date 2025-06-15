class PlayerModel:
    def __init__(self):
        self.score_diffs = []

    def update(self, score_diff):
        self.score_diffs.append(score_diff)
        if len(self.score_diffs) > 20:
            self.score_diffs.pop(0)

    def average_score_diff(self):
        return sum(self.score_diffs) / len(self.score_diffs) if self.score_diffs else 0

    def get_engine_level(self):
        avg = self.average_score_diff()
        if avg > 100:
            return 1
        elif avg > 50:
            return 5
        elif avg > 0:
            return 10
        elif avg > -50:
            return 15
        else:
            return 20
