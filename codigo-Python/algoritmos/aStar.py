from collections import deque

class A_estrela:
    def __init__(self, adjacency_matrix, cities):
        self.adjacency_matrix = adjacency_matrix  
        self.cities = cities  

    def get_neighbors(self, city):
        index = self.cities.index(city)
        neighbors = []
        for i, costs in enumerate(self.adjacency_matrix[index]):
            if costs[0] != float('inf') and i != index:  
                neighbors.append((self.cities[i], costs[0]))  
        return neighbors

    def h(self, city):
        return 1  

    def a_star_algorithm(self, start_city, goal_city):
        open_list = set([start_city])
        closed_list = set([])
        g = {start_city: 0}  
        parents = {start_city: start_city}

        while open_list:
            n = None

            for city in open_list:
                if n is None or g[city] + self.h(city) < g[n] + self.h(n):
                    n = city

            if n is None:
                print('Caminho não encontrado!')
                return None, float('inf')

            if n == goal_city:
                path = []
                total_cost = g[n]

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.append(start_city)
                path.reverse()
                print(f"Caminho encontrado: {path}, Custo total: {total_cost}")
                return path, total_cost

            for neighbor, cost in self.get_neighbors(n):
                if neighbor not in open_list and neighbor not in closed_list:
                    open_list.add(neighbor)
                    parents[neighbor] = n
                    g[neighbor] = g[n] + cost
                else:
                    if g[neighbor] > g[n] + cost:
                        g[neighbor] = g[n] + cost
                        parents[neighbor] = n
                        if neighbor in closed_list:
                            closed_list.remove(neighbor)
                            open_list.add(neighbor)

            open_list.remove(n)
            closed_list.add(n)

        print('Caminho não encontrado!')
        return None, float('inf')