import heapq

class AnytimeDStar:
    def __init__(self, adjacency_matrix, cities, toll_weight=1.0, fuel_weight=1.0, distance_weight=1.0):
        self.adjacency_matrix = adjacency_matrix
        self.cities = cities
        self.toll_weight = toll_weight
        self.fuel_weight = fuel_weight
        self.distance_weight = distance_weight

    def find_path(self, start_city, end_city):
        open_set = {start_city}
        came_from = {}
        g_score = {city: float('inf') for city in self.cities}
        g_score[start_city] = 0
        f_score = {city: float('inf') for city in self.cities}
        f_score[start_city] = self.heuristic(start_city, end_city)

        while open_set:
            current_city = min(open_set, key=lambda city: f_score[city])

            if current_city == end_city:
                return self.reconstruct_path(came_from, current_city)

            open_set.remove(current_city)

            for neighbor, costs in self.adjacency_matrix.get(current_city, {}).items():
                tentative_g_score = g_score[current_city] + self.calculate_cost(costs)

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_city
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, end_city)
                    open_set.add(neighbor)

        return None

    def calculate_cost(self, costs):
        return (self.toll_weight * costs['toll'] +
                self.fuel_weight * costs['fuel'] +
                self.distance_weight * costs['distance_km'])

    def reconstruct_path(self, came_from, current_city):
        total_toll = 0
        total_fuel = 0
        total_distance = 0
        path = []

        while current_city in came_from:
            path.append(current_city)
            costs = self.adjacency_matrix[came_from[current_city]][current_city]
            total_toll += costs['toll']
            total_fuel += costs['fuel']
            total_distance += costs['distance_km']
            current_city = came_from[current_city]

        path.append(current_city)  
        path.reverse()  
        return path, total_toll, total_fuel, total_distance

    def heuristic(self, city1, city2):
        return 0  