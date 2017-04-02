from collections import namedtuple
from random import choice
from queue import PriorityQueue
import numpy as np
from ghostly import Player, MoveType, TileType


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
        self.path = ['dummy']
        
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

        def manhattan_distance(other):
            return abs(self.x - other.x) + abs(self.y - other.y)
        
        def get_general_direction():

            bs = 6
            h = 3
            best_square = None
            best_score = np.inf

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
                    if any([t.weight > 5 for t in block]):
                        continue
                    if not any([t.weight < 0 for t in block]):
                        continue
                    score = sum(block)
                    if score < best_score:
                        best_score = score
                        best_square = sq

                if best_score < np.inf:
                    break

                bs += 2
                h += 1
                    
            return best_square

        def Astar_to_nearest_pellet(square=None):

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
                        break
                    if x0 <= tile.x <= x1 and y0 <= tile.y <= y1:
                        self.target = tile
                        break

                visited.add(tile)
                d = cur.distance + 1

                for mv, xy in tile.valid_moves.items():
                    x, y = xy
                    t = self.gamemap.state[x, y]
                    
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
                path.append(cur.move.value)

            return path

        if any([a.bad and manhattan_distance(a) < 4 for a in self.assholes]):
            square = get_general_direction()
            self.path = Astar_to_nearest_pellet(square)

        if self.path:
            return self.path[-1]

        self.path = Astar_to_nearest_pellet()
        return self.path[-1]
