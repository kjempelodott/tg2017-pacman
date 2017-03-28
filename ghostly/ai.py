import heapq
from collections import deque, namedtuple
from random import choice
import numpy as np
from ghostly import Player, TileType, Move


class ProteusV(Player):
    
    def __init__(self, gamemap, **kwargs):
        self.plan = [None]
        super().__init__(**kwargs)
        self.gamemap = gamemap
        self.gamemap.place_player(self)
        self.last_pos = self.point

    def update_self(self, **kwargs):
        p = Player(**kwargs)
        self.x, self.y = p.x, p.y
        self.score = p.score
        self.bad = p.bad
        if self.point != self.last_pos:
            self.plan.pop()

    def observe(self, others):
        self.assholes = [Player(**p) for p in others]
        for asshole in self.assholes:
            self.gamemap.place_player(asshole)

    def startround(self):
        self.make_plan()

    def move(self):
        if len(self.plan) < 2:
            self.make_plan()
            
        #if not any(ass.bad for ass in self.assholes):
        self.last_pos = self.point
        print(self.plan[-1].direction.value)
        return self.plan[-1].direction.value
        #else:
            # check that im not moving towards any
         #   pass
            
    def make_plan(self):

        def manhattan_distance(x0, y0, x1, y1):
            return abs(x0 - x1) + abs(y0 - y1)
        
        destination = None
        min_dist = np.inf
        for x, y in self.gamemap.superpellets:
            estimate = manhattan_distance(self.x, self.y, x, y)
            if estimate < min_dist:
                min_dist = estimate
                destination = (x, y)

        if destination:

            priority = distance(self.x, self.y, *destination)
            queue = PriorityQueue((priority, Move(*destination, '')))
            to = {}

            scores = {destination: 0}

            BLOCKSIZE = 5
            
            for i in range(BLOCKSIZE):
                current = queue.get_nowait() # fml, get == pop
                if current.x == self.x and current.y == self.y:
                    construct_path

                for nb in self.gamemap.neighbors[destination]:
                    score = scores[current] + self.gamemap.weightedmap[(nb.x, nb.y)]
                    queue.put_nowait((score, nb))
                    




















            
            
            
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

            shortest_path = min(list(get_paths(end)), key=lambda p: len(p))
            self.plan = shortest_path
