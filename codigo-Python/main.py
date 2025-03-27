import os
import pandas as pd
import numpy as np
from algoritmos.aStar import A_estrela
from algoritmos.dynamic_AStar import DynamicAStar
from algoritmos.anytime_DStar import AnytimeDStar
from importar_grafo import importar_grafo

def main():
    csv_file = "cities_nodes_special.csv"

    if not os.path.exists(csv_file):
        print(f"Erro ao abrir o ficheiro {csv_file}")
        return
    
    adj_matrix, cities = importar_grafo(csv_file)

    print("\nLista de cidades disponíveis: ")
    for i, city in enumerate(sorted(cities)):
        print(f"{i}: {city}")

    print("\nEscolha o algoritmo: ")
    print("1 - A*")
    print("2 - Dynamic A*")
    print("3 - Anytime D*")

    algoritmo = input("Digite o número do algoritmo desejado: ").strip()
    
    start_city = input("Introduza a cidade de origem: ").strip()
    end_city = input("Introduza a cidade de destino: ").strip()

    if start_city not in cities or end_city not in cities:
        print("A cidade introduzida não existe.")
        return

    if algoritmo == "1":
        nome_algoritmo = "A*"
        algoritmo_escolhido = A_estrela(adjacency_matrix=adj_matrix, cities=cities)
        resultado = algoritmo_escolhido.a_star_algorithm(start_city, end_city)
    
    elif algoritmo == "2":
        nome_algoritmo = "Dynamic A*"
        algoritmo_escolhido = DynamicAStar(adjacency_matrix=adj_matrix, cities=cities)
        resultado = algoritmo_escolhido.find_path(start_city, end_city)
    
    elif algoritmo == "3":
        nome_algoritmo = "Anytime D*"
        algoritmo_escolhido = AnytimeDStar(adjacency_matrix=adj_matrix, cities=cities)
        resultado = algoritmo_escolhido.find_path(start_city, end_city)

    else:
        print("Opção inválida! Escolha 1, 2 ou 3.")
        return
    
    print(f"\nExecutando {nome_algoritmo}...\n")

    if not resultado:
        print(f"\nNenhum caminho encontrado entre {start_city} e {end_city}.")
        return

    # Se for apenas um caminho e um único custo total
    if isinstance(resultado, tuple) and len(resultado) == 2:
        caminho, custo_total = resultado
        print("\nMelhor Caminho Encontrado:")
        print(f"Caminho: {caminho}")
        print(f"Custo total: {custo_total}")
        return

    # Se for uma lista de múltiplos caminhos
    melhor_caminho = None
    menor_custo_total = float('inf')

    print("Caminhos possíveis:")
    for i, (path, custos) in enumerate(resultado):
        if isinstance(custos, (int, float)):  
            distancia, combustivel, portagem = custos, 0, 0  
        elif len(custos) == 3:  
            distancia, combustivel, portagem = custos
        else:
            print(f"⚠️ Formato inesperado de custo: {custos}")
            continue

        custo_total = distancia + combustivel + portagem

        print(f"  {i+1}. Caminho: {path}")
        print(f"Distância: {distancia} km")
        print(f"Combustível: {combustivel} L")
        print(f"Portagem: {portagem} €")
        print(f"Custo total: {custo_total}")
        print("-" * 40)

            # Seleciona o melhor caminho baseado no menor custo total
        if custo_total < menor_custo_total:
            menor_custo_total = custo_total
            melhor_caminho = (path, custos)

    if melhor_caminho:
        print("\nMelhor Caminho Encontrado:")
        print(f"Caminho: {melhor_caminho[0]}")
        print(f"Distância: {melhor_caminho[1][0]} km")
        print(f"Combustível: {melhor_caminho[1][1]} L")
        print(f"Portagens: {melhor_caminho[1][2]} €")
    else:
        print(f"\nNenhum caminho encontrado entre {start_city} e {end_city}.")

if __name__ == "__main__":
    main()



"""2º comentário - código para os três"""        
"""
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

    if algoritmo == "1":
        algorithm = A_estrela(adjacency_matrix=adj_matrix, cities=cities)
        result = algorithm.a_star_algorithm(start_city, end_city)
    elif algoritmo == "2":
        algorithm = DynamicAStar(adjacency_matrix=adj_matrix, cities=cities)
        result = algorithm.find_path(start_city, end_city)
    elif algoritmo == "3":
        algorithm = AnytimeDStar(adjacency_matrix=adj_matrix, cities=cities)
        result = algorithm.find_path(start_city, end_city)

    else:
        print("Opção inválida! Escolha 1, 2 ou 3.")
        return
    
    if result:
        path, cost = result
        print(f"\nCaminho encontrado entre {start_city} e {end_city} utilizando {algoritmo}: {path}")
        print(f"Custo total do caminho: {cost}")
    else:
        print(f"Nenhum caminho encontrado entre {start_city} e {end_city}.")

if __name__ == "__main__":
    main()
"""









"""1º comentário - código inicial para fazer com o grafo"""
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