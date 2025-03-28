import heapq

class DynamicAStar:
    def __init__(self, adjacency_matrix, cities):
        self.adjacency_matrix = adjacency_matrix  
        self.cities = cities  
        self.g_values = {}  
        self.f_values = {}  
        self.parents = {}  

    def get_neighbors(self, city):
        index = self.cities.index(city)
        neighbors = []
        for i, costs in enumerate(self.adjacency_matrix[index]):
            if costs[0] != float('inf') and i != index:  
                neighbors.append((self.cities[i], costs[0]))  
        return neighbors

    def h(self, city, goal_city):
        return 1  

    def update_graph(self, updated_edges):
        """
        Atualiza dinamicamente os pesos das arestas.
        updated_edges: lista de tuplas (cidade1, cidade2, novo_custo)
        """
        for city1, city2, new_cost in updated_edges:
            i, j = self.cities.index(city1), self.cities.index(city2)
            self.adjacency_matrix[i][j] = (new_cost,)  
            self.adjacency_matrix[j][i] = (new_cost,)  

    def find_path(self, start_city, goal_city):
        open_list = []
        closed_list = set()

        self.g_values = {city: float('inf') for city in self.cities}
        self.f_values = {city: float('inf') for city in self.cities}
        self.parents = {city: None for city in self.cities}

        self.g_values[start_city] = 0
        self.f_values[start_city] = self.h(start_city, goal_city)

        heapq.heappush(open_list, (self.f_values[start_city], start_city))

        while open_list:
            _, current_city = heapq.heappop(open_list)

            if current_city == goal_city:
                return self.reconstruct_path(start_city, goal_city)

            closed_list.add(current_city)

            for neighbor, cost in self.get_neighbors(current_city):
                if neighbor in closed_list:
                    continue

                new_g = self.g_values[current_city] + cost

                if new_g < self.g_values[neighbor]:
                    self.parents[neighbor] = current_city
                    self.g_values[neighbor] = new_g
                    self.f_values[neighbor] = new_g + self.h(neighbor, goal_city)

                    heapq.heappush(open_list, (self.f_values[neighbor], neighbor))

        return None  

    def reconstruct_path(self, start, goal):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = self.parents[current]
        path.reverse()
        total_cost = self.g_values[goal]
        return path, total_cost