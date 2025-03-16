from collections import deque

def a_star(adjacency_list, start_node, stop_node):
    open_list = set([start_node])  
    closed_list = set([]) 

    g = {node: float('inf') for node in adjacency_list}
    g[start_node] = 0  
    parents = {start_node: None}  

    def h(n):  
        return 0  

    while open_list:
        n = min(open_list, key=lambda v: g[v] + h(v))

        if n == stop_node:
            path = []
            total_cost = g[n]  

            while n is not None:
                path.append(n)
                n = parents[n]

            path.reverse()
            return path, total_cost

        open_list.remove(n)
        closed_list.add(n)

        for (neighbor, weight) in adjacency_list[n]:
            if neighbor in closed_list:
                continue

            tentative_g = g[n] + weight

            if neighbor not in open_list:
                open_list.add(neighbor)
            elif tentative_g >= g[neighbor]:
                continue

            parents[neighbor] = n
            g[neighbor] = tentative_g

    return None, float('inf')