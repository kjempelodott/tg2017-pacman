from collections import namedtuple
from enum import Enum
import numpy as np
 
class MoveType(Enum):
    Up = b'UP'
    Down = b'DOWN'
    Left = b'LEFT'
    Right = b'RIGHT'

Tile = namedclass('TileCOnfig', (char, weight))
class TileType(Enum):
    Pellet      = TileConfig('.', -1)
    SuperPellet = TileConfig('o', -5)
    Wall        = TileConfig('|', np.inf)
    Floor       = TileConfig('_', 0)
    Door        = TileConfig('-', 0)
    Player      = TileConfig('@', 1)
    BadPlayer   = TileConfig('#', 10)
    Monster     = TileConfig('<', 5)

class Map:
    def __init__(self, content=None, width=None, height=None, pelletsleft=0):
        self.prev = content
        self.w, self.h = width, height
        self.pellets = pelletsleft

        self.weightmap = np.zeros((width, height), dtype=float)
        self.neighbors = np.zeros((width, height), dtype=object)
        self.superpellets = []

        for x in range(self.w):
            for y in range(self.h):
                char = content[y][x]
                tt = next(t for t in TileType if char == t.value.char)
                self.weightmap[x, y] = tt.value.weight

                if tt == TileType.SuperPellet:
                    self.superpellets.append((x, y))
                if tt != TileType.Wall:
                    self.neighbors[x, y] = [c, m for c, m in self.get_neighboors(x, y)
                                            if self.wrightmap[*c] != np.inf]
                    
    def update(self, content):
        changed_rows = ((j, r) for j, r in enumerate(zip(content, self.prev)) if r[0] != r[1])
        for j, row in changed_rows:
            changed_tiles = ((i, j) for i, t in enumerate(zip(*row)) if t[0] != t[1])
            for i, j in changed_tiles:
                self.weightmap[i, j] = TileType.Floor.weight
                if (i, j) in self.superpellets:
                    self.superpellets.remove((i, j))
                
        self.prev = content

    def place_player(self, player):
        if player.bad:
            self.weightmap[player.x, player.y] = TileType.Monster.weight
        else:
            self.weightmap[player.x, player.y] = TileType.Player.weight

    @staticmethod
    def get_neighboors(x, y):
        return (((x, y - 1), MoveType.Up),
                ((x, y + 1), MoveType.Down),
                ((x - 1, y), MoveType.Left),
                ((x + 1, y), MoveType.Right))
    
