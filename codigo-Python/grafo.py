from algoritmos.aStar import A_estrela
from algoritmos.dijkstra import Dijkstra
from algoritmos.bidirectional_aStar import BidirectionalAStar
from algoritmos.real_time_adaptative_aStar import RealTimeAdaptativeAStar

class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def find_path(self, start, goal, algorithm):
        if algorithm == "as":
            graph = A_estrela(self.adjacency_list)
            return graph.a_star_algorithm(start, goal)
        
        elif algorithm == "d":
            graph = Dijkstra.build_graph(self.adjacency_list)
            alg = Dijkstra(graph, start, goal)
            return alg.dijkstra_algorithm()
        
        elif algorithm == "bas":
            graph = BidirectionalAStar(self.adjacency_list)
            return graph.bidirectional_a_star(start, goal)
        elif algorithm == "rta":
            graph = RealTimeAdaptativeAStar(self.adjacency_list)
            return graph.rtaa_star_algorithm(start, goal)
        else:
            raise ValueError("Invalid algorithm. Choose 'a_star' or 'dijkstra' or 'bidirectional_aStar' or 'real_time_adaptative_aStar'.")

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

algorithm = input("Choose an algorithm (as/d/bas/rta): ").strip().lower()

while algorithm not in ["as", "d", "bas", "rta"]:
    print("Invalid choice. Please enter 'a_star' or 'dijkstra' or 'bidirectional_aStar' or 'real_time_adaptative_aStar'.")
    algorithm = input("Choose an algorithm (AS/D/BAS/RTA): ").strip().lower()

start = input("Enter the start node: ").strip().upper()
goal = input("Enter the goal node: ").strip().upper()

graph = Graph(adjacency_list)
path, cost = graph.find_path(start, goal, algorithm)

if path:
    print("")
    print(f"Path from {start} to {goal} using {algorithm.upper()}: {path}")
    print(f"Total path cost: {cost}")
else:
    print(f"No path found from {start} to {goal}.")