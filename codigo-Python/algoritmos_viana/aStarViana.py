from collections import deque

class A_estrela:
    def __init__(self, adjacency_matrix, cities):
        self.adjacency_matrix = adjacency_matrix  
        self.cities = cities  
    
    def get_neighbors(self, city):
        if city not in self.adjacency_matrix:
            print(f"Erro: cidade {city} não encontrada no grafo.")
            return []
        return [(neighbor, costs) for neighbor, costs in self.adjacency_matrix[city].items()]
    
    def h(self, city):
        return 1  # Heurística simplificada (pode ser melhorada)

    def a_star_algorithm(self, start_city, goal_city):
        open_list = set([start_city])
        closed_list = set([])
        parents = {start_city: start_city}

        g_unlevel = {start_city: 0}
        g_duration = {start_city: 0}
        g_distance = {start_city: 0}

        def total_cost(city):
            return g_unlevel[city] + g_duration[city] + g_distance[city]

        while open_list:
            n = None
            for city in open_list:
                if n is None or (total_cost(city) + self.h(city)) < (total_cost(n) + self.h(n)):
                    n = city

            if n is None:
                print('Caminho não encontrado!')
                return None, float('inf'), float('inf'), float('inf'), float('inf')

            if n == goal_city:
                path = []
                total_unlevel = g_unlevel[n]
                total_duration = g_duration[n]
                total_distance = g_distance[n]

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.append(start_city)
                path.reverse()

                total = total_unlevel + total_duration + total_distance
                return path, total_unlevel, total_duration, total_distance, total

            for neighbor, costs in self.get_neighbors(n):
                unlevel = costs.get('unlevel_percent', 0)
                duration = costs.get('duration_minutes', 0)
                distance = costs.get('distance_meters', 0)

                if neighbor not in open_list and neighbor not in closed_list:
                    open_list.add(neighbor)
                    parents[neighbor] = n
                    g_unlevel[neighbor] = g_unlevel[n] + unlevel
                    g_duration[neighbor] = g_duration[n] + duration
                    g_distance[neighbor] = g_distance[n] + distance
                else:
                    if total_cost(neighbor) > total_cost(n) + unlevel + duration + distance:
                        g_unlevel[neighbor] = g_unlevel[n] + unlevel
                        g_duration[neighbor] = g_duration[n] + duration
                        g_distance[neighbor] = g_distance[n] + distance
                        parents[neighbor] = n

                        if neighbor in closed_list:
                            closed_list.remove(neighbor)
                            open_list.add(neighbor)

            open_list.remove(n)
            closed_list.add(n)

        print('Caminho não encontrado!')
        return None, float('inf'), float('inf'), float('inf'), float('inf')