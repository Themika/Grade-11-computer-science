import heapq

class AStar:
    WATER_TILES = ['Tilemap_Flat_46']
    AVOID_TILE = 40

    def __init__(self, start, goal, tilemap):
        self.start = start
        self.goal = goal
        self.tilemap = tilemap
        self.g = {start: 0}  # Cost from start to the current node
        self.f = {start: self.heuristic(start, goal)}  # Estimated cost from start to goal through the current node
        self.open_list = [(self.f[start], start)]  # Priority queue of nodes to be evaluated
        self.open_set = {start}  # Set of nodes to be evaluated
        self.came_from = {}  # Map of navigated nodes
        self.valid_tile_cache = {}  # Cache for valid tiles
        self.water_tile_cache = {}  # Cache for water tiles

    def heuristic(self, a, b):
        # Heuristic function for A* (Manhattan distance)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, s):
        # Get all valid neighboring tiles
        x, y = s
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if self.is_valid_tile(neighbor):
                neighbors.append(neighbor)
        return neighbors

    def is_valid_tile(self, tile):
        # Check if a tile is valid (not out of bounds and not a water tile)
        if tile in self.valid_tile_cache:
            return self.valid_tile_cache[tile]
        x, y = tile
        if y < 0 or y >= len(self.tilemap) or x < 0 or x >= len(self.tilemap[0]):
            self.valid_tile_cache[tile] = False
            return False
        result = not self.is_water_tile(x, y)
        self.valid_tile_cache[tile] = result
        return result

    def is_water_tile(self, x, y):
        # Check if a tile is a water tile
        tile = (x, y)
        if tile in self.water_tile_cache:
            return self.water_tile_cache[tile]
        if y < 0 or y >= len(self.tilemap) or x < 0 or x >= len(self.tilemap[0]):
            self.water_tile_cache[tile] = True
            return True
        tile_value = self.tilemap[y][x]
        result = tile_value in self.WATER_TILES or tile_value[0] == self.AVOID_TILE
        self.water_tile_cache[tile] = result
        return result

    def find_path(self):
        # Main A* algorithm to find the path
        while self.open_list:
            _, current = heapq.heappop(self.open_list)
            self.open_set.remove(current)
            if current == self.goal:
                return self.reconstruct_path(current)
            for neighbor in self.get_neighbors(current):
                tentative_g_score = self.g[current] + 1
                if tentative_g_score < self.g.get(neighbor, float('inf')):
                    self.came_from[neighbor] = current
                    self.g[neighbor] = tentative_g_score
                    self.f[neighbor] = tentative_g_score + self.heuristic(neighbor, self.goal)
                    if neighbor not in self.open_set:
                        heapq.heappush(self.open_list, (self.f[neighbor], neighbor))
                        self.open_set.add(neighbor)
        return None

    def reconstruct_path(self, current):
        # Reconstruct the path from start to goal
        path = [current]
        while current in self.came_from:
            current = self.came_from[current]
            path.append(current)
        path.reverse()
        return path