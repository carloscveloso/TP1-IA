import heapq

class RealTimeAdaptativeAStar:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        self.heuristic = {node: 1 for node in self.adjacency_list}

    def get_neighbors(self, node):
        return self.adjacency_list.get(node, [])
    
    def h(self, node):
        return self.heuristic[node]
    
    def update_heuristic(self, visited, g):
        for node in visited:
            self.heuristic[node] = g[node]

    def a_star_step(self, start_node, stop_node, search_depth=3):
        open_list = [(self.h(start_node), start_node)]  
        closed_list = set()
        g = {start_node: 0}
        parents = {start_node: None}
        steps = 0

        while open_list and steps < search_depth:
            _, n = heapq.heappop(open_list)  

            if n == stop_node:
                path = []
                while n:
                    path.append(n)
                    n = parents[n]
                path.reverse()
                return path, g[stop_node]

            closed_list.add(n)

            for (m, weight) in self.get_neighbors(n):
                if m in closed_list:
                    continue

                new_cost = g[n] + weight

                if m not in g or new_cost < g[m]:  
                    g[m] = new_cost
                    parents[m] = n
                    heapq.heappush(open_list, (g[m] + self.h(m), m))  

            steps += 1

        self.update_heuristic(closed_list, g)

        if not closed_list:
            return None, float('inf')

        best_node = min(closed_list, key=lambda node: g[node] + self.h(node))
        return [best_node], g[best_node]
    
    def rtaa_star_algorithm(self, start_node, stop_node):
        """Executa o algoritmo Real Time Adaptative A*."""
        current_node = start_node
        total_path = [current_node]
        total_cost = 0
        visited_nodes = set()

        while current_node != stop_node:
            if current_node in visited_nodes:
                print("Loop infinito encontrado!")
                return None, float('inf')

            visited_nodes.add(current_node)  

            path, cost = self.a_star_step(current_node, stop_node)

            if not path or cost == float('inf'):
                print("Nenhum caminho encontrado.")
                return None, float('inf')

            current_node = path[-1]  
            total_path.extend(path[1:])  
            total_cost += cost

        return total_path, total_cost