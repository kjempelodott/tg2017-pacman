class Player:
    def __init__(self, id=None, tile=None, score=None, isdangerous=None):
        self.id = id
        self.tile = tile
        self.score = score
        self.bad = isdangerous
    def up(self):
        try:
            assert(self.tile.up() in self.tile.valid_moves)
        except:
            raise InvalidMove
    def down(self):
        try:
            assert(self.tile.down() in self.tile.valid_moves)
        except:
            raise InvalidMove
    def left(self):
        try:
            assert(self.tile.left() in self.tile.valid_moves)
        except:
            raise InvalidMove
    def right(self):
        try:
            assert(self.tile.right() in self.tile.valid_moves)
        except:
            raise InvalidMove
