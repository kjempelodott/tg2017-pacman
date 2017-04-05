from collections import namedtuple
from random import choice
from queue import PriorityQueue
import numpy as np
from ghostly import Player, MoveType, TileType
from ghostly import Astar, manhattan_distance

class DeltaPath:
    def __init__(self, tile, move, distance):
        self.tile = tile
        self.move = move
        self.distance = distance
    def __eq__(self, other):
        return self.distance == other.distance                
    def __lt__(self, other):
        return self.distance < other.distance


class ProteusV:
    
    def __init__(self, gamemap):
        self.gamemap = gamemap
        self.path = [None]
        self.target = None
        self.x = self.y = None
        
    def update(self, me, others):
        p = Player(**me)
        if not (self.x == p.x and self.y == p.y):
            self.path.pop()
            self.x, self.y = p.x, p.y
        self.score = p.score

        self.bad = p.bad
        self.assholes = [Player(**p) for p in others]
        for asshole in self.assholes:
            self.gamemap.place_player(asshole, self.bad)

    def move(self):

        # squares = []
        # if self.target == None: # First move
        #     get_xy(self)
        #     squares = self.get_general_direction()
        #     squares = [k for k, v in sorted(squares.items(), key=lambda x: x[1])]

        badtiles = {()}
        nearby = [a for a in self.assholes if a.bad and manhattan_distance(self, a) <= 5]
        for asshole in nearby:
            print('nearby', asshole)
            badtiles.update(dp.tile for dp in Astar(asshole, self.gamemap.state, target=self))

        while 1:
            if self.path and self.target.weight < 0:
                return self.path[-1].move.value

            #sq = None if not squares else squares.pop()
            self.path = Astar(self, self.gamemap.state, badtiles=badtiles)
            
    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
        
    def get_general_direction(self):

        bs = 6
        h = 3
        scores = {}
        
        while bs < 20:
            squares = (
                (max(0, self.x-bs), self.x, max(0, self.y-bs), self.y),
                (max(0, self.x-bs), self.x, max(0, self.y-h), self.y+h),
                (max(0, self.x-bs), self.x, self.y, self.y+bs),
                (max(0, self.x-h), self.x+h, max(0, self.y-bs), self.y),
                (max(0, self.x-h), self.x+h, self.y, self.y+bs),
                (self.x, self.x+bs, max(0, self.y-bs), self.y),
                (self.x, self.x+bs, max(0, self.y-h), self.y+h),
                (self.x, self.x+bs, self.y, self.y+bs),
            )                
            for sq in squares:
                block = self.gamemap.state[sq[0]:sq[1], sq[2]:sq[3]].compressed()
                if any([t.weight > 10 for t in block]) or \
                   not any([t.weight < 0 for t in block]):
                    continue
                scores[sq] = sum(block)

            if scores:
                break

            bs += 2
            h += 1

        return scores

    def Astar_to_nearest_pellet(self, square=None):

        x0 = x1 = y0 = y1 = None
        if square:
            x0, x1, y0, y1 = square

        cur = DeltaPath(self.gamemap.state[self.x, self.y], b'', 0)
        visited = {(cur.tile)}
        came_from = {}

        queue = PriorityQueue()
        queue.put(cur)

        while not queue.empty():
            cur = queue.get()
            tile = cur.tile
            # Found pellet inside best square?
            if tile.weight < 0:
                if not square:
                    self.target = tile
                    break
                if x0 <= tile.x <= x1 and y0 <= tile.y <= y1:
                    self.target = tile
                    break

            visited.add(tile)
            d = cur.distance + 1

            for mv, xy in tile.valid_moves.items():
                x, y = xy
                t = self.gamemap.state[x, y]

                if t.weight > 0 and d <= 3:
                    continue
                
                if t in visited:
                    continue

                if t in came_from and came_from[t].distance < d:
                    continue

                pd = DeltaPath(tile, mv, d)
                came_from[t] = pd
                queue.put(DeltaPath(t, mv, d))

        path = []
        while cur.tile in came_from:
            cur = came_from[cur.tile]
            path.append(cur)

        return path
