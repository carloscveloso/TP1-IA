import numpy as np
import csv
import heapq
from algoritmos import aStar, dynamic_aStar, anytime_DStar

def carregar_grafo():
    nome_arquivo = "cities_nodes_special.csv"
    with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        dados = [row for row in reader][1:] 
    
    cidades = {}
    index = 0
    edges = []
    
    for row in dados:
        origem, destino, _, _, distancia = row
        if origem not in cidades:
            cidades[origem] = index
            index += 1
        if destino not in cidades:
            cidades[destino] = index
            index += 1
        edges.append((origem, destino, float(distancia)))
    
    adjacency_list = {cidade: [] for cidade in cidades}
    for origem, destino, distancia in edges:
        adjacency_list[origem].append((destino, distancia))
        adjacency_list[destino].append((origem, distancia))  
    
    return cidades, adjacency_list

def main():
    cidades, adjacency_list = carregar_grafo()
    
    print("Escolha o algoritmo:")
    print("1 - A*")
    opcao = input("Opção: ")
    
    if opcao != "1":
        print("Opção inválida!")
        return
    
    print("Cidades disponíveis:")
    for cidade in cidades.keys():
        print(cidade)
    
    inicio = input("Digite a cidade inicial: ")
    objetivo = input("Digite a cidade objetivo: ")
    
    if inicio not in cidades or objetivo not in cidades:
        print("Cidades inválidas!")
        return
    
    caminho, custo = aStar(adjacency_list, inicio, objetivo)
    
    if caminho:
        print("\nCaminho encontrado:", " -> ".join(caminho))
        print(f"Custo total: {custo:.2f} km")
    else:
        print("Nenhum caminho encontrado.")

if __name__ == "__main__":
    main()
