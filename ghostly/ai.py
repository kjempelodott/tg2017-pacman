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
        self.path = None
        self.target = None
        self.panic = False
        self.x = self.y = None
        
    def update(self, me, others):
        p = Player(**me)
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
        avoid = set()
        
        if self.bad:
            self.panic = False
        elif not self.panic:
            nearby = [a for a in self.assholes if a.bad and manhattan_distance(self, a) <= 4]
            if nearby:
                self.path = None
                self.panic = True
                for asshole in nearby:
                    asspath = Astar(asshole, self.gamemap.state, target=self)
                    avoid.update([dp.tile for dp in asspath])
        else:
            if not any(a for a in self.assholes if a.bad and manhattan_distance(self, a) <= 8):
                self.panic = False
                self.path = None
        
        if not self.path or self.target.weight >= 0:
             self.path = Astar(self, self.gamemap.state, badtiles=avoid)
        try:
            return self.path.pop().move.value
        except:
            return b''


            







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
