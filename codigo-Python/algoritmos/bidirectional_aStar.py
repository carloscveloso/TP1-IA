import heapq

class BidirectionalAStar:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list  

    def heuristic(self, node, goal):
        return 1  

    def bidirectional_a_star(self, start, goal):
        forward_open = [(0, 0, start)]  
        backward_open = [(0, 0, goal)]

        forward_g = {start: 0}
        backward_g = {goal: 0}

        forward_parents = {start: None}
        backward_parents = {goal: None}

        forward_visited = set()
        backward_visited = set()

        counter = 0  

        while forward_open and backward_open:
            _, _, current_forward = heapq.heappop(forward_open)
            forward_visited.add(current_forward)

            if current_forward in backward_visited:
                return self.reconstruct_path(current_forward, forward_parents, backward_parents, forward_g, backward_g)

            for neighbor, weight in self.adjacency_list.get(current_forward, []):  
                if neighbor in forward_visited:
                    continue

                new_cost = forward_g[current_forward] + weight
                if neighbor not in forward_g or new_cost < forward_g[neighbor]:
                    forward_g[neighbor] = new_cost
                    counter += 1
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heapq.heappush(forward_open, (priority, counter, neighbor))
                    forward_parents[neighbor] = current_forward

            _, _, current_backward = heapq.heappop(backward_open)
            backward_visited.add(current_backward)

            if current_backward in forward_visited:
                return self.reconstruct_path(current_backward, forward_parents, backward_parents, forward_g, backward_g)

            for neighbor, weight in self.adjacency_list.get(current_backward, []):  
                if neighbor in backward_visited:
                    continue

                new_cost = backward_g[current_backward] + weight
                if neighbor not in backward_g or new_cost < backward_g[neighbor]:
                    backward_g[neighbor] = new_cost
                    counter += 1
                    priority = new_cost + self.heuristic(neighbor, start)
                    heapq.heappush(backward_open, (priority, counter, neighbor))
                    backward_parents[neighbor] = current_backward

        return None  

    def reconstruct_path(self, meeting_point, forward_parents, backward_parents, forward_g, backward_g):
        """Reconstroi o caminho mais curto a partir do ponto inicial até ao objetivo da pesquisa."""
        path = []

        node = meeting_point
        while node is not None:
            path.append(node)
            node = forward_parents[node]
        path.reverse()

        node = backward_parents[meeting_point]
        while node is not None:
            path.append(node)
            node = backward_parents[node]

        total_cost = forward_g[meeting_point] + backward_g[meeting_point]
        return path, total_cost