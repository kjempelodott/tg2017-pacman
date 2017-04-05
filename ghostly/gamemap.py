import copy
from enum import Enum
import numpy as np
import numpy.ma as ma


class TileType(Enum):
    Pellet      = -1
    SuperPellet = -5
    Wall        = np.inf
    Floor       = 0
    Door        = 0
    Player      = 1
    BadPlayer   = 30
    Monster     = 20
    iPlayer     = -20
    iBadPlayer  = 1


class MoveType(Enum):
    Up = b'UP'
    Down = b'DOWN'
    Left = b'LEFT'
    Right = b'RIGHT'

    
class Tile:

    CHAR_TO_TILETYPE = {
        '.' : TileType.Pellet,
        'o' : TileType.SuperPellet,
        '|' : TileType.Wall,
        '_' : TileType.Floor,
        '-' : TileType.Door
    }

    def __init__(self, x, y, char):
        self._tiletype = Tile.CHAR_TO_TILETYPE[char]
        self.weight = self._tiletype.value
        self.x, self.y = x, y
        self.valid_moves = {}

    def get_type(self):
        return self._tiletype
        
    def set_type(self, tt):
        self._tiletype = tt
        self.weight = tt.value
        
    tiletype = property(get_type, set_type)
        
    def __add__(self, num):
        return self.weight + num

    def __radd__(self, num):
        return self.weight + num
        
    def set_valid_moves(self, grid):

        w, h = grid.shape
        x, y = self.x, self.y
        
        if y < h - 1:
            if not ma.is_masked(grid[x, y+1]):
                self.valid_moves[MoveType.Down] = (x, y+1)
        if x < w - 1:
            if not ma.is_masked(grid[x+1, y]):
                self.valid_moves[MoveType.Right] = (x+1, y)
        if y:
            if not ma.is_masked(grid[x, y-1]):
                self.valid_moves[MoveType.Up] = (x, y-1)
        if x:
            if not ma.is_masked(grid[x-1, y]):
                self.valid_moves[MoveType.Left] = (x-1, y)

        
class Map:
    def __init__(self, content=None, width=None, height=None, pelletsleft=0):
        
        self.prev = content
        self.w, self.h = width, height
        self.pellets = pelletsleft

        self.state = ma.array(np.zeros((width, height), dtype=object))

        for x in range(self.w):
            for y in range(self.h):
                char = content[y][x]
                tile = Tile(x, y, char)
                if tile.tiletype == TileType.Wall:
                    self.state[x, y] = ma.masked
                else:
                    self.state[x, y] = tile

        for t in self.state[~self.state.mask]:
            t.set_valid_moves(self.state)
        
    def update(self, content):
        for x in range(self.w):
            for y in range(self.h):
                char = content[y][x]
                tt = Tile.CHAR_TO_TILETYPE[char]
                if tt != TileType.Wall:
                    self.state[x, y].tiletype = tt

    def place_player(self, player, youbad):
        tt = None
        if youbad:
            tt = TileType.iBadPlayer if player.bad else TileType.iPlayer
        else:
            tt = TileType.BadPlayer if player.bad else TileType.Player
        self.state[player.x, player.y].tiletype = tt
