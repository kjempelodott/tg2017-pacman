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
