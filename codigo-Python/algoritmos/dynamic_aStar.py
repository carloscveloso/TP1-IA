import heapq
import math

def heuristic(node, goal):
    return math.sqrt((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2)

def dynamic_aStar(graph, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    goal_score = {node: float('inf') for node in graph}
    goal_score[start] = 0  

    in_open_set = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, goal_score[goal]

        for neighbor, distancia, _, _ in graph[current]:
            tentative_g_score = goal_score[current] + distancia

            if tentative_g_score < goal_score[neighbor]:
                came_from[neighbor] = current
                goal_score[neighbor] = tentative_g_score
                if neighbor not in in_open_set or tentative_g_score < in_open_set[neighbor]:
                    heapq.heappush(open_set, (tentative_g_score + heuristic(neighbor, goal), neighbor))
                    in_open_set[neighbor] = tentative_g_score

    return None, None  

def update_graph(graph, origem, destino, nova_distancia, novo_combustivel, novo_tempo):
    if origem in graph:
        for i, (n, d, c, t) in enumerate(graph[origem]):
            if n == destino:
                graph[origem][i] = (destino, nova_distancia, novo_combustivel, novo_tempo)

    if destino in graph:
        for i, (n, d, c, t) in enumerate(graph[destino]):
            if n == origem:
                graph[destino][i] = (origem, nova_distancia, novo_combustivel, novo_tempo)