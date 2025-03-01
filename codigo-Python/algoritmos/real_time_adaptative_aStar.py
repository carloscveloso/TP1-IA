from collections import deque

class RealTimeAdaptativeAStar:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        self.heuristic = {node: 1 for node in adjacency_list}

    def get_neighbors(self, v):
        return self.adjacency_list[v]
    
    def h(self, n):
        return self.heuristic[n]
    
    def update_heuristic(self, visited, g):
        for node in visited:
            self.heuristic[node] = g[node]

    def a_star_step(self, start_node, stop_node, search_depth=3):
        open_list = set([start_node])
        closed_list =set([])
        g = {start_node: 0}
        parents = {start_node: start_node}
        steps = 0

        while open_list and steps < search_depth:
            n = None

            for v in open_list:
                if n is None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v

            if n is None:
                return None, float('inf')
            
            if n == stop_node:
                path = []
                total_cost = g[n]

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.append(start_node)
                path.reverse()
                return path, total_cost
            
            for (m, weight) in self.get_neighbors(n):
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n
                        
                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)
            steps += 1

        self.update_heuristic(closed_list, g)

        best_node = min(closed_list, key=lambda node: g[node] + self.h(node))
        return [best_node], g[best_node]
    
    def rtaa_star_algorithm(self, start_node, stop_node):
        current_node = start_node
        total_path = [current_node]
        total_cost = 0

        while current_node != stop_node:
            path, cost = self.a_star_step(current_node, stop_node)

            if not path:
                print("Nenhum caminho encontrado.")
                return None, float('inf')
            
            current_node = path[-1]
            total_path.extend(path[1:])
            total_cost += cost
            
        return total_path, total_cost