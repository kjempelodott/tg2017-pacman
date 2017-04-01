from enum import Enum
import numpy as np


class TileType(Enum):
    Pellet      = -1
    SuperPellet = -5
    Wall        = np.inf
    Floor       = 0
    Door        = 1
    Player      = 3
    BadPlayer   = 10
    Monster     = 10


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

    def __init__(self, char, x, y):
        self.type = Tile.CHAR_TO_TILETYPE[char]
        self.x, self.y = x, y
        self.valid_moves = {}

    def set_valid_moves(self, grid):

        if self.type == TileType.Wall:
            return
        
        w, h = grid.shape
        x, y = self.x, self.y
        
        if y < h - 1:
            if grid[x, y+1] != TileType.Wall:
                self.valid_moves[MoveType.Down] = (x, y+1)
        if x < w - 1:
            if grid[x+1, y] != TileType.Wall:
                self.valid_moves[MoveType.Right] = (x+1, y)
        if y:
            if grid[x, y-1] != TileType.Wall:
                self.valid_moves[MoveType.Up] = (x, y-1)
        if x:
            if grid[x-1, y] != TileType.Wall:
                self.valid_moves[MoveType.Left] = (x-1, y)

        
class Map:
    def __init__(self, content=None, width=None, height=None, pelletsleft=0):
        self.prev = content
        self.w, self.h = width, height
        self.pellets = pelletsleft

        self.tiles = np.zeros((width, height), dtype=object)
        self.superpellets = []

        for x in range(self.w):
            for y in range(self.h):
                char = content[y][x]
                tile = Tile(char, x, y)
                self.tiles[x, y] = tile
                
                if tile.type == TileType.SuperPellet:
                    self.superpellets.append((x, y))

        for x in range(self.w):
            for y in range(self.h):
                self.tiles[x, y].set_valid_moves(self.tiles)
                
    def update(self, content):
        changed_rows = ((j, r) for j, r in enumerate(zip(content, self.prev)) if r[0] != r[1])
        for j, row in changed_rows:
            changed_tiles = ((i, j) for i, t in enumerate(zip(*row)) if t[0] != t[1])
            for i, j in changed_tiles:
                self.tiles[i, j].type = TileType.Floor
                if (i, j) in self.superpellets:
                    self.superpellets.remove((i, j))

        self.prev = content

    def place_player(self, player):
        tt = TileType.BadPlayer if player.bad else TileType.Player
        self.tiles[player.x, player.y].type = tt
