import csv
import numpy as np

def importar_grafo(arquivo):
    nodes = {}
    index = 0

    edges = []
    
    # Lendo o CSV e coletando dados
    with open(arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            origem, destino, kms, litros, minutos = row[0], row[1], int(row[2]), int(row[3]), int(row[4])
            
            # Atribuir índices aos nós
            if origem not in nodes:
                nodes[origem] = index
                index += 1
            if destino not in nodes:
                nodes[destino] = index
                index += 1
            
            edges.append((origem, destino, kms, litros, minutos))
    
    # Criar matriz de adjacência
    n = len(nodes)
    matriz_adjacencia = np.full((n, n), np.inf) 
    
    for origem, destino, kms, _, _ in edges:
        i, j = nodes[origem], nodes[destino]
        matriz_adjacencia[i][j] = kms
        matriz_adjacencia[j][i] = kms 
    
    return nodes, matriz_adjacencia

arquivo = "cities.nodes_special.csv"  
nodes, matriz = importar_grafo(arquivo)

# Imprimir a matriz
print("Nodos:", nodes)
print("Matriz de Adjacência:")
print(matriz)  
