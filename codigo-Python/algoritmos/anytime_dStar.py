import heapq

class AnytimeDStar:
    def __init__(self, adjacency_matrix, cities):
        self.adjacency_matrix = adjacency_matrix  
        self.cities = cities  
        self.g_values = {}  
        self.rhs_values = {}  
        self.parents = {}  
        self.open_list = []
        self.goal = None  

    def get_neighbors(self, city):
        index = self.cities.index(city)
        neighbors = []
        for i, costs in enumerate(self.adjacency_matrix[index]):
            if costs[0] != float('inf') and i != index:  
                neighbors.append((self.cities[i], costs[0]))  
        return neighbors

    def h(self, city):
        return 1  

    def initialize(self, start_city, goal_city):
        self.goal = goal_city  

        self.g_values = {city: float('inf') for city in self.cities}
        self.rhs_values = {city: float('inf') for city in self.cities}
        self.parents = {city: None for city in self.cities}

        self.rhs_values[goal_city] = 0
        heapq.heappush(self.open_list, (self.calculate_key(goal_city), goal_city))

    def update_vertex(self, city):
        if city != self.goal:
            self.rhs_values[city] = min(
                [self.g_values[neighbor] + cost for neighbor, cost in self.get_neighbors(city)] or [float('inf')]
            )

        if city in self.open_list:
            self.open_list = [(key, c) for key, c in self.open_list if c != city]
            heapq.heapify(self.open_list)

        if self.g_values[city] != self.rhs_values[city]:
            heapq.heappush(self.open_list, (self.calculate_key(city), city))

    def calculate_key(self, city):
        g_rhs_min = min(self.g_values[city], self.rhs_values[city])
        return (g_rhs_min + self.h(city), g_rhs_min)  

    def find_path(self, start_city, goal_city):
        self.initialize(start_city, goal_city)

        while self.open_list and (self.open_list[0][0] < self.calculate_key(start_city) or self.rhs_values[start_city] != self.g_values[start_city]):
            _, current_city = heapq.heappop(self.open_list)

            if self.g_values[current_city] > self.rhs_values[current_city]:
                self.g_values[current_city] = self.rhs_values[current_city]
            else:
                self.g_values[current_city] = float('inf')
                self.update_vertex(current_city)

            for neighbor, _ in self.get_neighbors(current_city):
                self.update_vertex(neighbor)

        return self.reconstruct_path(start_city, goal_city)

    def reconstruct_path(self, start, goal):
        path = []
        current = start
        while current is not None and current != goal:
            path.append(current)
            current = self.parents[current] if self.parents[current] in self.cities else None

        path.append(goal)
        total_cost = self.g_values[start]
        return path, total_cost