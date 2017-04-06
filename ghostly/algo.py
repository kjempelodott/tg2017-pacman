from queue import PriorityQueue


class DeltaPath:
    def __init__(self, tile, move, distance):
        self.tile = tile
        self.move = move
        self.distance = distance
    def __eq__(self, other):
        return self.distance == other.distance                
    def __lt__(self, other):
        return self.distance < other.distance
 
def manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def Astar(player, m, target=None, badtiles=None, constraint=None):

    x0 = x1 = y0 = y1 = None
    if constraint:
        x0, x1, y0, y1 = constraint

    cur = DeltaPath(m[player.x, player.y], b'', 0)
    visited = {cur.tile}
    if badtiles:
        visited.update(badtiles)
    came_from = {}

    queue = PriorityQueue()
    queue.put(cur)

    while not queue.empty():
        cur = queue.get()
        tile = cur.tile

        # If target specified
        if target:
            if tile.x == target.x and tile.y == target.y:
                break
        # Else target is nearest pellet
        elif tile.weight < 0:
            if not constraint:
                player.target = tile
                break
            if x0 <= tile.x <= x1 and y0 <= tile.y <= y1:
                player.target = tile
                break

        visited.add(tile)
        d = cur.distance + 1

        for mv, xy in tile.valid_moves.items():
            x, y = xy
            t = m[x, y]

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
