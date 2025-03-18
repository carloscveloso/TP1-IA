import heapq
import numpy as np

def heuristic(node, goal):
    return np.linalg.norm(node - goal)

def aStar(indices, matriz, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    goal_score = {node: float('inf') for node in indices}
    goal_score[start] = 0

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

        for neighbor_index in range(len(indices)): 
            distancia = matriz[current, neighbor_index, 0]  

            if distancia == np.inf:
                continue

            tentative_goal_score = goal_score[current] + distancia

            if tentative_goal_score < goal_score[neighbor_index]:
                came_from[neighbor_index] = current
                goal_score[neighbor_index] = tentative_goal_score
                heapq.heappush(open_set, (tentative_goal_score + heuristic(neighbor_index, goal), neighbor_index))

    return None