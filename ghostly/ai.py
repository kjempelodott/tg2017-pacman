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
        print(p.x, p.y)
        self.score = p.score
        self.bad = p.bad

        self.assholes = [Player(**p) for p in others]
        for asshole in self.assholes:
            self.gamemap.place_player(asshole)

    def move(self):
        if self.last_pos != (self.x, self.y):
            # Last move succeeded
            self.path.pop()
            
        if not len(self.path):
            self.think()

        return self.path[-1].direction.value
            
        #if not any(ass.bad for ass in self.assholes):
        #self.last_pos = self.point
        #print(self.path[-1].direction.value)
        #return self.path[-1].direction.value
        #else:
            # check that im not moving towards any
         #   pass
            
    def think(self):

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
            print(self.x, self.y)
            while 1:
                squares = ((max(0, self.x - bs), self.x, max(0, self.y - bs), self.y),
                           (max(0, self.x - bs), self.x, self.y, self.y + bs),
                           (self.x, self.x + bs, max(0, self.y - bs), self.y),
                           (self.x, self.x + bs, self.y, self.y + bs))

            
                for sq in squares:
                    block = self.gamemap.tiles[sq[0]:sq[1], sq[2]:sq[3]]
                    if np.any(t.type.value < 0 for x in block):
                        # Add penalty to corners (smaller block)
                        _sum =  sum(t.type.value for t in block
                                    if t.type != TileType.Wall)
                        score = _sum/(1 + np.sqrt(block.size))
                        print(score, sq)
                        if score < best_score:
                            best_score = score
                            best_square = sq

                if best_score != np.inf:
                    break
                bs += 1
                
            return best_square

        def Astar_to_nearest_pellet(x0, x1, y0, y1):

            MoveDist = namedtuple('MoveDist', ('move', 'dist'))
            
            cur = Move(self.x, self.y, MoveType.Down)
            visited = {(cur)}
            came_from = {}
            
            queue = PriorityQueue()
            queue.put((0, cur))

            while not queue.empty():
                d, cur = queue.get()
                if self.gamemap.weight[cur.x, cur.y] < 0: # Negative cost: pellet
                    break

                visited.add(cur)
                d += 1
                for nb in self.gamemap.neighbors[cur.x, cur.y]:
                    if x0 <= nb.x <= x1 and y0 <= nb.y <= y1:
                        if nb in visited:
                            continue

                        if nb in came_from and came_from[nb].dist < d:
                            continue

                        came_from[nb] = MoveDist(cur, d)
                        queue.put((d, nb))
                    
            path = [cur]
            while path[-1] in came_from:
                path.append(came_from[path[-1]].move)
                
            return path[1::-1] # Remove current position

        square = get_general_direction()
        self.path = Astar_to_nearest_pellet(*square)
