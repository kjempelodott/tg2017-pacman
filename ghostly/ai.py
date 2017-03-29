import heapq
from collections import deque, namedtuple
from random import choice
import numpy as np
from ghostly import Player


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
        return b''
        if len(self.path) < 2:
            self.think()
            
        #if not any(ass.bad for ass in self.assholes):
        self.last_pos = self.point
        print(self.path[-1].direction.value)
        return self.path[-1].direction.value
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
                    block = self.gamemap.weightmap[sq[0]:sq[1], sq[2]:sq[3]]
                    if np.any(block < 0):
                        # Add penalty to corners (smaller block)
                        score = np.ma.masked_invalid(block).sum()/(1 + np.sqrt(block.size))
                        print(score, sq)
                        if score < best_score:
                            best_score = score
                            best_square = sq

                if best_score != np.inf:
                    break
                bs += 1
                
            return best_square

        def Astar_pellet(minimap):
            


        
        # find path to nearest pellet in chosen block


        
        # destination = None
        # min_dist = np.inf
        # for x, y in self.gamemap.superpellets:
        #     estimate = manhattan_distance(self.x, self.y, x, y)
        #     if estimate < min_dist:
        #         min_dist = estimate
        #         destination = (x, y)

        # if destination:

        #     priority = distance(self.x, self.y, *destination)
        #     queue = PriorityQueue((priority, Move(*destination, '')))
        #     to = {}

        #     scores = {destination: 0}

        #     BLOCKSIZE = 5
            
        #     for i in range(BLOCKSIZE):
        #         current = queue.get_nowait() # fml, get == pop
        #         if current.x == self.x and current.y == self.y:
        #             construct_path

        #         for nb in self.gamemap.neighbors[destination]:
        #             score = scores[current] + self.gamemap.weightedmap[(nb.x, nb.y)]
        #             queue.put_nowait((score, nb))
                    




















            
            
            
            # def get_paths(*path):
            #     moves = [Move(d, tile)
            #              for d, tile in path[-1].tile.valid_moves.items()
            #              if (tile not in seen_tiles and
            #                  not tile.tiletype == TileType.Player)]
            #     last = next((m for m in moves if m.tile == self.tile), None)
            #     if last:
            #         yield [*path, last]
            #     else:
            #         for move in moves:
            #             seen_tiles.add(move.tile)
            #             yield from get_paths(*path, move)

            # seen_tiles = {()} # HAHA VAGINA
            # idx = 0
            # while 1:
            #     try:
            #         current = queue[idx]
            #         c = current.counter + 1
            #         moves = [Move(d, tile, c)
            #                  for d, tile in current.tile.valid_moves.items()
            #                  if tile not in seen_tiles]

            #         last = next((m for m in moves if m.tile == self.tile), None)
            #         if last:
            #             queue.append(last)
            #             break

            #         seen_tiles.update((m.tile for m in moves))
            #         queue.extend(moves)
            #         idx += 1
            #     except IndexError: # Impossible path!
            #         return b''

            # shortest_path = min(list(get_paths(end)), key=lambda p: len(p))
            # self.plan = shortest_path
