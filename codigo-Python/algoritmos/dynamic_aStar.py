import heapq

class DynamicAStar:
    def __init__(self, adjacency_matrix, cities):
        self.graph = adjacency_matrix 
        self.cities = cities
        self.cost_updates = {}  

    def heuristic(self, city1, city2):
        """ Heurística baseada na distância em linha reta, se disponível """
        if city1 in self.graph and city2 in self.graph[city1]:
            return self.graph[city1][city2].get('distance_km', float('inf'))
        return float('inf')  

    def update_graph(self, origin, destination, new_costs):
        """ Atualiza dinamicamente os custos de uma aresta no grafo. """
        if origin in self.graph and destination in self.graph[origin]:
            for key in ['toll', 'fuel', 'distance_km']:
                if key in new_costs:
                    self.graph[origin][destination][key] = new_costs[key]
                    self.graph[destination][origin][key] = new_costs[key]  
                    self.cost_updates[(origin, destination, key)] = new_costs[key]
                    self.cost_updates[(destination, origin, key)] = new_costs[key]

    def find_path(self, start, goal):
        """ Dynamic A* para encontrar o menor caminho, considerando custos de portagens, combustível e distância. """
        open_list = []
        heapq.heappush(open_list, (0, start))
        
        came_from = {}  
        g_score = {city: float('inf') for city in self.cities}
        g_score[start] = 0

        f_score = {city: float('inf') for city in self.cities}
        f_score[start] = self.heuristic(start, goal)

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.graph.get(current, {}):
                edge = self.graph[current][neighbor]

                cost_toll = edge.get('toll', 0)
                cost_fuel = edge.get('fuel', 0)
                cost_distance = edge.get('distance_km', float('inf'))

                cost_toll = self.cost_updates.get((current, neighbor, 'toll'), cost_toll)
                cost_fuel = self.cost_updates.get((current, neighbor, 'fuel'), cost_fuel)
                cost_distance = self.cost_updates.get((current, neighbor, 'distance_km'), cost_distance)

                total_cost = cost_distance + cost_fuel + cost_toll

                tentative_g_score = g_score[current] + total_cost

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = (current, cost_toll, cost_fuel, cost_distance)
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return None  

    def reconstruct_path(self, came_from, current):
        """ Reconstrói o caminho e calcula os custos acumulados de portagens, combustível e distância. """
        path = [current]
        total_toll = 0.0
        total_fuel = 0.0
        total_distance = 0.0

        while current in came_from:
            prev_city, toll, fuel, distance = came_from[current]
            total_toll += toll
            total_fuel += fuel
            total_distance += distance
            path.append(prev_city)
            current = prev_city

        path.reverse()

        total_cost = total_distance + total_fuel + total_toll
        
        return path, total_toll, total_fuel, total_distance, total_cost