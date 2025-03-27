import heapq

class DynamicAStar:
    def __init__(self, adjacency_matrix, cities):
        self.adjacency_matrix = adjacency_matrix
        self.cities = cities
        self.g = {}
        self.rhs = {}
        self.open_list = []
        self.parents = {}

    
    def h(self, city, goal_city):
        return 1
    
    def initialize(self, start_city, goal_city):
        for city in self.cities:
            self.g[city] = float('inf')
            self.rhs[city] = float('inf')
            self.parents[city] = None
        self.rhs[goal_city] = 0
        heapq.heappush(self.open_list, (self.h(start_city, goal_city), start_city))

    def update_vertex(self, city):
        if city != self.start_city:
            self.rhs[city] = min(self.g[neighbor] + cost for neighbor, cost in self.get_neighbors(city))
        if city in self.open_list:
            self.open_list.remove(city)
        if self.g[city] != self.rhs[city]:
            heapq.heappush(self.open_list, (self.rhs[city] + self.h(city, self.goal_city), city))

    def compute_shortest_path(self):
        while self.open_list and (self.open_list[0][0] < self.g[self.start_city] or self.rhs[self.start_city] != self.g[self.start_city]):
            _, city = heapq.heappop(self.open_list)
            if self.g[city] > self.rhs[city]:
                self.g[city] = self.rhs[city]
                for neighbor, _ in self.get_neighbors(city):
                    self.update_vertex(neighbor)
            else:
                self.g[city] = float('inf')
                for neighbor, _ in self.get_neighbors(city) + [(city, 0)]:
                    self.update_vertex(neighbor)

    def get_neighbors(self, city):
        index = self.cities.index(city)
        neighbors = []
        for i, costs in enumerate(self.adjacency_matrix[index]):
            if costs[0] != float('inf') and i != index:  
                neighbors.append((self.cities[i], costs[0]))  
        return neighbors
    
    def find_path(self, start_city, goal_city):
        self.start_city = start_city
        self.goal_city = goal_city
        self.initialize(start_city, goal_city)
        self.compute_shortest_path()

        if self.g[start_city] == float('inf'):
            return None, float('inf')
        
        path = []
        city = start_city

        while city != goal_city:
            path.append(city)
            neighbors = self.get_neighbors(city)

            if not neighbors:
                return None, float('inf')
            
            city = min(neighbors, key=lambda x: self.g[x[0]])[0]
    
        path.append(goal_city)
        return path, self.g[start_city]
