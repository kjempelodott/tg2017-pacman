from enum import Enum
 

class Tile:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))
    def init_valid_moves(self):
        self.valid_moves = []
    def up(self):
        return Tile(self.x, self.y - 1)
    def down(self):
        return Tile(self.x, self.y + 1)
    def left(self):
        return Tile(self.x - 1, self.y)
    def right(self):
        return Tile(self.x + 1, self.y)


class TileType(Enum):
    Pellet = '.'
    SuperPellet = 'o'
    Wall = '|'
    Floor = '_'
    Door = '-'
    Player = '@'


class Map:
    def __init__(self, content=None, width=None, height=None, pelletsleft=0):
        self.prev = content
        self.w, self.h = width, height
        self.pellets = pelletsleft
        self.tiles = {}

        for x in xrange(self.w):
            for y in xrange(self.h)
                char = m[x][y]
                tt = next(t for t in TileType if char == t)
                self.tiles[Tile(x, y)] = tt

        validpos = [p for p, tt in self.tiles.items() if
                    tt in (TileType.Pellet, TileType.SuperPellet,
                           TileType.Floor, TileType,Door)]

        for pos in validpos:
            pos.init_valid_moves()
            for move in (pos.up(), pos.down(), pos.left(), pos.right()):
                if move in validpos:
                    pos.valid_moves.append(move)

    def update(self, content):
        changed_rows = ((j, r) for j, r in enumerate(zip(content, self.prev)) if r[0] != r[1])
        for j, row in changed_rows:
            changed_tiles = ((i, j) for i, t in enumerate(zip(row)) if t[0] != t[1])
            for i, j in changed_tiles:
                # Pellet eaten
                self.tiles[Tile(i, j)] = TileType.Floor
                
        self.prev = m

    def place_player(self, player)
        self.tiles[player.tile] = TileType.Player
