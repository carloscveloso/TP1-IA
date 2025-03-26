import os
import pandas as pd
import numpy as np
from algoritmos.aStar import A_estrela
from algoritmos.dynamic_AStar import DStar
from algoritmos.anytime_DStar import AnytimeDStar
from importar_grafo import importar_grafo

def main():
    csv_file = "cities_nodes_special.csv"

    if not os.path.exists(csv_file):
        print(f"Erro ao abrir o ficheiro {csv_file}")
        return
    
    adj_matrix, cities = importar_grafo(csv_file)

    print("\nLista de cidades disponíveis: ")
    for i, city in enumerate(cities):
        print(f"{i}: {city}")

    print("\nEscolha o algoritmo: ")
    print("1")
    algoritmo = input("Digite o número do algoritmo desejado: ")
    
    start_city = input("Introduza a cidade de origem: ").strip()
    end_city = input("Introduza a cidade de destino: ").strip()

    if start_city not in cities or end_city not in cities:
        print("A cidade introduzida não existe.")
        return
    
    adjacency_list = {}
    n = len(cities)
    city_index = {city: i for i, city in enumerate(cities)}

    for i in range(n):
        city = cities[i]
        neighbors = []
        for j in range(n):
            if not np.any(adj_matrix[i, j] == np.inf) and i != j:
                neighbors.append((cities[j], adj_matrix[i, j]))
        adjacency_list[city] = neighbors

    a_star = A_estrela(adjacency_matrix=adj_matrix, cities=cities)
    result = a_star.a_star_algorithm(start_city, end_city)

    if result:
        path, cost = result
        print(f"\nCaminho encontrado entre {start_city} e {end_city} utilizando {algoritmo}: {path}")
        print(f"Custo total do caminho: {cost}")
    else:
        print(f"Nenhum caminho encontrado ente {start_city} até {end_city}.")

if __name__ == "__main__":
    main()


"""
class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def find_path(self, start, goal, algorithm):
        if algorithm == "as":
            graph = A_estrela(self.adjacency_list)
            return graph.a_star_algorithm(start, goal)
        
        elif algorithm == "d":
            graph = DStar.build_graph(self.adjacency_list)
            alg = DStar(graph, start, goal)
            return alg.dijkstra_algorithm()
        
        elif algorithm == "bas":
            graph = AnytimeDStar(self.adjacency_list)
            return graph.bidirectional_a_star(start, goal)
        else:
            raise ValueError("Escolha inválida.  Introduza 'as', 'd', 'bas' ou 'rta'.")

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

algorithm = input("Escolga um algoritmo (as/d/bas/rta): ").strip().lower()

while algorithm not in ["as", "d", "bas", "rta"]:
    print("Escolha inválida.  Introduza 'as', 'd', 'bas' ou 'rta'.")
    algorithm = input("Escolha um algoritmo (AS/D/BAS/RTA): ").strip().lower()

start = input("Introduza o node inicial: ").strip().upper()
goal = input("Introduza o node objetivo: ").strip().upper()

graph = Graph(adjacency_list)
result = graph.find_path(start, goal, algorithm)

if result:
    path, cost = result
    print(f"\nCaminho encontrado entre {start} e {goal} utilizando {algorithm.upper()}: {path}")
    print(f"Custo total do caminho: {cost}")
else:
    print(f"Nenhum caminho encontrado ente {start} até {goal}.")"
    """