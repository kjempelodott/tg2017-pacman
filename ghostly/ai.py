from collections import namedtuple
from random import choice
from queue import PriorityQueue
import numpy as np
from ghostly import Player, MoveType


class ProteusV:
    
    def __init__(self, gamemap):
        self.path = [None]
        self.gamemap = gamemap
        self.last_pos = None

    def update(self, me, others):
        p = Player(**me)
        self.x, self.y = p.x, p.y
        self.score = p.score
        self.bad = p.bad

        self.assholes = [Player(**p) for p in others]
        for asshole in self.assholes:
            self.gamemap.place_player(asshole)

    def move(self):
        if self.last_pos != (self.x, self.y):
            # Last move succeeded
            self.path.pop()
            
        if not self.path:
            self.think()

        return self.path[-1].move.value
            
        #if not any(ass.bad for ass in self.assholes):
        #self.last_pos = self.point
        #print(self.path[-1].direction.value)
        #return self.path[-1].direction.value
        #else:
            # check that im not moving towards any
         #   pass
            
    def think(self):

        class PathDelta:
            def __init__(self, tile, move, distance):
                self.tile = tile
                self.move = move
                self.distance = distance
            def __eq__(self, other):
                return self.distance == other.distance                
            def __lt__(self, other):
                return self.distance < other.distance
        
        def manhattan_distance(x0, y0, x1, y1):
            return abs(x0 - x1) + abs(y0 - y1)

        def get_general_direction():

            """
            Divide surrounding map into four blocks, and
            identify blocks with at least one pellet. From those,
            choose the block with least cost. Increment blocksize
            until at least one block contains a pellet.
            """
        
            bs = 5
            best_square = None
            best_score = np.inf
            while 1:
                squares = ((max(0, self.x - bs), self.x, max(0, self.y - bs), self.y),
                           (max(0, self.x - bs), self.x, self.y, self.y + bs),
                           (self.x, self.x + bs, max(0, self.y - bs), self.y),
                           (self.x, self.x + bs, self.y, self.y + bs))

                for sq in squares:
                    block = self.gamemap.tiles[sq[0]:sq[1], sq[2]:sq[3]]
                    if np.any(t.weight < 0 for t in block):
                        # Add penalty to corners (smaller block)
                        norm = (1 + np.sqrt(block.size))
                        score = np.sum(block)/norm
                        if score < best_score:
                            best_score = score
                            best_square = sq

                if best_score != np.inf:
                    break
                bs += 1
                
            return best_square

        def Astar_to_nearest_pellet(x0, x1, y0, y1):

            cur = PathDelta(self.gamemap.tiles[self.x, self.y], b'', 0)
            visited = {(cur.tile)}
            came_from = {}
            
            queue = PriorityQueue()
            queue.put(cur)

            while not queue.empty():
                cur = queue.get()
                tile = cur.tile
                if tile.weight < 0: # Negative cost: pellet
                    break

                visited.add(tile)
                d = cur.distance + 1
                for mv, t in tile.valid_moves.items():
                    if not (x0 <= t.x <= x1 and y0 <= t.y <= y1):
                        d += 1

                    if t in visited:
                        continue

                    if t in came_from and came_from[t].distance < d:
                        continue

                    pd = PathDelta(tile, mv, d)
                    came_from[t] = pd
                    queue.put(PathDelta(t, mv, d))

            path = []
            while cur.tile in came_from:
                cur = came_from[cur.tile]
                path.append(cur)

            return path

        print('thinking')
        square = get_general_direction()
        self.path = Astar_to_nearest_pellet(*square)
