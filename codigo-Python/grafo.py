from aStar import A_estrela  
from dijkstra import Dijkstra  

class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def find_path(self, start, goal, algorithm):
        if algorithm == "a_star":
            graph = A_estrela(self.adjacency_list)
            return graph.a_star_algorithm(start, goal)
        elif algorithm == "dijkstra":
            graph = Dijkstra.build_graph(self.adjacency_list)
            alg = Dijkstra(graph, start, goal)
            return alg.dijkstra_algorithm()
        else:
            raise ValueError("Invalid algorithm. Choose 'a_star' or 'dijkstra'.")

adjacency_list = {
    'A': [('B', 5), ('F', 3)],
    'B': [('A', 5), ('B', 2), ('G', 3)],
    'C': [('B', 2), ('D', 6), ('H', 10)],
    'D': [('C', 6), ('E', 3)],
    'E': [('D', 3), ('F', 8), ('H', 5)],
    'F': [('A', 3), ('E', 8), ('G', 7)],
    'G': [('B', 3), ('F', 7), ('H', 2)],
    'H': [('C', 10), ('E', 5), ('G', 2)],
}

algorithm = input("Choose an algorithm (a_star/dijkstra): ").strip().lower()

while algorithm not in ["a_star", "dijkstra"]:
    print("Invalid choice. Please enter 'a_star' or 'dijkstra'.")
    algorithm = input("Choose an algorithm (a_star/dijkstra): ").strip().lower()

start = input("Enter the start node: ").strip().upper()
goal = input("Enter the goal node: ").strip().upper()

graph = Graph(adjacency_list)
path, cost = graph.find_path(start, goal, algorithm)

if path:
    print(f"Path from {start} to {goal} using {algorithm.upper()}: {path}")
    print(f"Total path cost: {cost}")
else:
    print(f"No path found from {start} to {goal}.")