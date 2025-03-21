from importar_grafo import importar_grafo
from algoritmos import aStar, anytime_DStar, dynamic_AStar
import numpy as np

def escolher_algoritmo():
    print("\nEscolha o algoritmo de busca:")
    print("1 - A* (A estrela)")
    print("2 - Anytime D*")
    print("3 - Dynamic A*")
    
    while True:
        escolha = input("Digite o número do algoritmo: ")
        if escolha in ["1", "2", "3"]:
            return escolha
        else:
            print("Escolha inválida! Tente novamente.")

def escolher_nodo(indices):
    print("\nNós disponíveis:", list(indices.keys()))
    
    while True:
        escolha = input("Digite o nome do nodo: ")
        if escolha in indices:
            return escolha
        else:
            print("Nodo inválido! Tente novamente.")

def main():
    nome_arquivo = "cities_nodes_special.csv"
    
    print("\nImportando o gráfico...")
    indices, matriz = importar_grafo(nome_arquivo)
    print(matriz)
    algoritmo = escolher_algoritmo()
    
    print("\nEscolha o nodo de origem:")
    origem = escolher_nodo(indices)
    
    print("\nEscolha o nodo de destino:")
    destino = escolher_nodo(indices)

    if algoritmo == "1":
        print(f"\nCaminho de {origem} para {destino} usando A*...")
        caminho, custo = aStar.aStar(indices, matriz, origem, destino)
    
    elif algoritmo == "2":
        print(f"\nCaminho de {origem} para {destino} usando Anytime D*...")
        caminho, custo = anytime_DStar(indices, matriz, origem, destino)
    
    elif algoritmo == "3":
        print(f"\nCaminho de {origem} para {destino} usando Dynamic A*...")
        caminho, custo = dynamic_AStar(indices, matriz, origem, destino)

    if caminho:
        print("\nCaminho encontrado:", " → ".join(caminho))
        print(f"Custo total: {custo}")
    else:
        print("\nNão foi possível encontrar um caminho.")

if __name__ == "__main__":
    main()