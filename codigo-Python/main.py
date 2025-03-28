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
            print(f"Formato inesperado de custo: {custos}")
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
