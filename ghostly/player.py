class Player:
    def __init__(self, id, x, y, score, isdangerous):
        self.id = id
        self.x, self.y = x, y
        self.score = score
        self.bad = isdangerous

    def __str__(self):
        return '%s (%i, %i)' % (self.id, self.x, self.y)
