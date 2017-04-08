from ghostly import Player, MoveType, TileType
from ghostly import Astar, manhattan_distance


class ProteusV:
    
    def __init__(self, gamemap):
        self.reset(gamemap)
        self.paranoia = 4

    def die(self):
        self.paranoia += 2
        
    def reset(self, gamemap):
        self.gamemap = gamemap
        self.path = None
        self.target = None
        self.panic = False
        self.first_move = True
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
        constr = None

        if self.first_move:
            self.first_move = False;
            xc = yc = None
            if self.x >= (self.gamemap.w - 1)/2:
                xc = [self.x, self.gamemap.w - 1]
            else:
                xc = [0, self.x]
            if self.y >= (self.gamemap.h - 1)/2:
                yc = [self.y, self.gamemap.h - 1]
            else:
                yc = [0, self.y]
            constr = xc + yc
        elif self.bad:
            self.panic = False
        else:
            nearby = [a for a in self.assholes
                      if a.bad and manhattan_distance(self, a) <= self.paranoia]
            if nearby:
                self.path = None
                self.panic = True
                for asshole in nearby:
                    asspath = Astar(asshole, self.gamemap.state, target=self)
                    avoid.update([dp.tile for dp in asspath])
            elif self.panic:
                if not any(a for a in self.assholes
                           if a.bad and manhattan_distance(self, a) <= self.paranoia + 4):
                    self.panic = False
                    self.path = None

        if not self.path or self.target.weight >= 0:
             self.path = Astar(self, self.gamemap.state, badtiles=avoid, constraint=constr)
        try:
            return self.path.pop().move.value
        except:
            return b''

     # def get_general_direction(self):

     #    bs = 6
     #    h = 3
     #    scores = {}
        
     #    while bs < 20:
     #        squares = (
     #            (max(0, self.x-bs), self.x, max(0, self.y-bs), self.y),
     #            (max(0, self.x-bs), self.x, max(0, self.y-h), self.y+h),
     #            (max(0, self.x-bs), self.x, self.y, self.y+bs),
     #            (max(0, self.x-h), self.x+h, max(0, self.y-bs), self.y),
     #            (max(0, self.x-h), self.x+h, self.y, self.y+bs),
     #            (self.x, self.x+bs, max(0, self.y-bs), self.y),
     #            (self.x, self.x+bs, max(0, self.y-h), self.y+h),
     #            (self.x, self.x+bs, self.y, self.y+bs),
     #        )
     #        for sq in squares:
     #            block = self.gamemap.state[sq[0]:sq[1], sq[2]:sq[3]].compressed()
     #            if any([t.weight > 10 for t in block]) or \
     #               not any([t.weight < 0 for t in block]):
     #                continue
     #            scores[sq] = sum(block)

     #        if scores:
     #            break

     #        bs += 2
     #        h += 1

     #    return scores
