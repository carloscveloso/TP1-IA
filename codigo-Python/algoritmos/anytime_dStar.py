import heapq

class AnytimeDStar:
    def __init__(self, adjacency_matrix, cities):
        self.adjacency_matrix = adjacency_matrix  
        self.cities = cities  
        self.g = {}  
        self.rhs = {}  
        self.open_list = []
        self.epsilon = 2.5
        self.parents = {}
    

    def initialize(self, start_city, goal_city):
        """Inicializa os valores e a fila de prioridade"""
        for city in self.cities:
            self.g[city] = float('inf')
            self.rhs[city] = float('inf')
            self.parents[city] = None
        self.rhs[goal_city] = 0
        heapq.heappush(self.open_list, (self.h(start_city, goal_city), start_city))

    def h(self, city, goal_city):
        return 1

    def update_vertex(self, city):
        if city != self.start_city:
            self.rhs[city] = min(self.g[neighbor] + cost for neighbor, cost in self.get_neighbors(city))
        if city in self.open_list:
            self.open_list.remove(city)
        if self.g[city] != self.rhs[city]:
            heapq.heappush(self.open_list, (self.rhs[city] + self.epsilon * self.h(city, self.goal_city), city))

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

    def improve_solution(self):
        self.epsilon *= 0.9  # Reduzir epsilon para melhorar caminho
        self.compute_shortest_path()

    def find_path(self, start_city, goal_city):
        self.start_city = start_city
        self.goal_city = goal_city
        self.initialize(start_city, goal_city)
        self.compute_shortest_path()

        path = []
        city = start_city
        if self.g[start_city] == float('inf'):
            print("Caminho não encontrado!")
            return None, float('inf')

        while city != goal_city:
            path.append(city)
            city = min(self.get_neighbors(city), key=lambda x: self.g[x[0]])[0]

        path.append(goal_city)
        print(f"Caminho inicial encontrado: {path}, Custo total: {self.g[start_city]}")

        # Melhorar a solução iterativamente
        for _ in range(10):  
            self.improve_solution()
            print(f"Nova solução encontrada com ε = {self.epsilon:.2f}: {path}, Custo total: {self.g[start_city]}")

        return path, self.g[start_city]