import heapq

class AnytimeDStar:
    def __init__(self, adjacency_matrix, cities):
        self.adjacency_matrix = adjacency_matrix  
        self.cities = cities  
        self.g_score = {city: float('inf') for city in cities}  
        self.rhs = {city: float('inf') for city in cities}  
        self.open_list = [] 
        self.km = 0  
        self.goal_city = None  

    def get_neighbors(self, city):
        if city not in self.adjacency_matrix:
            print(f"Erro: cidade {city} não encontrada no grafo.")
            return []

        return [(neighbor, costs) for neighbor, costs in self.adjacency_matrix[city].items()]

    def h(self, city):
        return 1  

    def update_vertex(self, city):
        """ Atualiza o vertex na open list. """
        if self.g_score[city] != self.rhs[city]:
            heapq.heappush(self.open_list, (self.calculate_key(city), city))

    def calculate_key(self, city):
        return (min(self.g_score[city], self.rhs[city]) + self.h(city), min(self.g_score[city], self.rhs[city]))

    def compute_shortest_path(self):
        while self.open_list:
            key, n = heapq.heappop(self.open_list)

            if self.rhs[n] > self.g_score[n]:
                self.g_score[n] = self.rhs[n]
                for neighbor, costs in self.get_neighbors(n):
                    toll, fuel, distance_km = costs['toll'], costs['fuel'], costs['distance_km']
                    if neighbor in self.g_score:
                        self.rhs[neighbor] = min(self.rhs[neighbor], self.g_score[n] + toll + fuel + distance_km)
                    self.update_vertex(neighbor)

            elif self.g_score[n] > self.rhs[n]:
                self.g_score[n] = float('inf')
                self.update_vertex(n)
                for neighbor, costs in self.get_neighbors(n):
                    toll, fuel, distance_km = costs['toll'], costs['fuel'], costs['distance_km']
                    self.rhs[neighbor] = min(self.rhs[neighbor], self.g_score[n] + toll + fuel + distance_km)
                    self.update_vertex(neighbor)

    def find_path(self, start_city, goal_city):
        self.goal_city = goal_city
        self.rhs[start_city] = 0
        self.update_vertex(start_city)

        self.compute_shortest_path()

        if self.g_score[goal_city] == float('inf'):
            print('Caminho não encontrado!')
            return None, float('inf'), float('inf'), float('inf')

        path = []
        current_city = goal_city
        while current_city != start_city:
            path.append(current_city)
            min_cost = float('inf')
            next_city = None
            for neighbor, costs in self.get_neighbors(current_city):
                toll, fuel, distance_km = costs['toll'], costs['fuel'], costs['distance_km']
                cost = self.g_score[neighbor] + toll + fuel + distance_km
                if cost < min_cost:
                    min_cost = cost
                    next_city = neighbor
            if next_city is None:
                break
            current_city = next_city

        path.append(start_city)
        path.reverse()
        total_toll = sum(self.adjacency_matrix[path[i]][path[i + 1]]['toll'] for i in range(len(path) - 1))
        total_fuel = sum(self.adjacency_matrix[path[i]][path[i + 1]]['fuel'] for i in range(len(path) - 1))
        total_distance_km = sum(self.adjacency_matrix[path[i]][path[i + 1]]['distance_km'] for i in range(len(path) - 1))

        return path, total_toll, total_fuel, total_distance_km