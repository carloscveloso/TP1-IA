import os
import pandas as pd
import numpy as np
from algoritmos.aStar import A_estrela
from algoritmos.dynamic_aStar import DynamicAStar
from algoritmos.anytime_DStar import AnytimeDStar
from importar_grafo import importar_grafo

def main():
    csv_file = "cities_nodes_special.csv"

    if not os.path.exists(csv_file):
        print(f"Erro ao abrir o ficheiro {csv_file}")
        return
    
    adj_matrix, cities = importar_grafo(csv_file)

    print("\nEscolha o algoritmo: ")
    print("1 - A*")
    print("2 - Dynamic A*")
    print("3 - Anytime D*")

    algoritmo = input("Digite o número do algoritmo desejado: ").strip()

    print("\nLista de cidades disponíveis: ")
    for i, city in enumerate(sorted(cities)):
        print(f"{i}: {city}")


    try:
        start_index = int(input("Escolha o número da cidade de origem: ").strip())
        end_index = int(input("Escolha o número da cidade de destino: ").strip())

        # Verificar se os índices estão dentro do intervalo válido
        if start_index < 0 or start_index >= len(cities) or end_index < 0 or end_index >= len(cities):
            print("Índice inválido. Por favor, escolha um número dentro da lista de cidades.")
            return

        start_city = cities[start_index]
        end_city = cities[end_index]
        
    except ValueError:
        print("Por favor, insira um número válido para as cidades.")
        return

    if algoritmo == "1":
        algoritmo_escolhido = A_estrela(adjacency_matrix=adj_matrix, cities=cities)
        resultado = algoritmo_escolhido.a_star_algorithm(start_city, end_city)
    
    elif algoritmo == "2":
        algoritmo_escolhido = DynamicAStar(adjacency_matrix=adj_matrix, cities=cities)
        resultado = algoritmo_escolhido.find_path(start_city, end_city)
    
    elif algoritmo == "3":
        algoritmo_escolhido = AnytimeDStar(adjacency_matrix=adj_matrix, cities=cities)
        resultado = algoritmo_escolhido.find_path(start_city, end_city)

    else:
        print("Opção inválida! Escolha 1, 2 ou 3.")
        return

    if not resultado:
        print(f"\nNenhum caminho encontrado entre {start_city} e {end_city}.")
        return

    if algoritmo == "1":  # A*
        path, total_toll, total_fuel, total_distance = resultado
        print(f"\nCaminho encontrado: {path}")
        print(f"Custo total de portagens: {total_toll}")
        print(f"Custo total de combustível: {total_fuel}")
        print(f"Distância total: {total_distance}")

    elif algoritmo == "2":  # Dynamic A*
        path, total_toll, total_fuel, total_distance = resultado
        print(f"\nCaminho encontrado: {path}")
        print(f"Custo total de portagens: {total_toll}")
        print(f"Custo total de combustível: {total_fuel}")
        print(f"Distância total: {total_distance}")

    elif algoritmo == "3":  # Anytime D*
        path, total_toll, total_fuel, total_distance = resultado
        print(f"\nCaminho encontrado: {path}")
        print(f"Custo total de portagens: {total_toll}")
        print(f"Custo total de combustível: {total_fuel}")
        print(f"Distância total: {total_distance}")
    else:
        print(f"\nCaminho encontrado: {resultado}")

if __name__ == "__main__":
    main()
