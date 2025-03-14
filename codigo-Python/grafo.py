import csv
import heapq
from algoritmos import aStar, dynamic_aStar, anytime_DStar

# Nome do ficheiro CSV
filename = "trajetos.csv"

# Criar e escrever no ficheiro CSV
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Escrever as linhas no formato: origem, destino, kms, litros, minutos
    writer.writerow(["A", "F", 30, 4, 5])
    writer.writerow(["F", "B", 20, 3, 4])
    writer.writerow(["B", "C", 15, 2, 3])
    writer.writerow(["C", "D", 25, 4, 6])
    writer.writerow(["D", "E", 10, 1, 2])
    writer.writerow(["E", "A", 35, 5, 7])   
    writer.writerow(["B", "F", 10, 1, 2])
    writer.writerow(["C", "F", 10, 1, 2])

print(f"Ficheiro '{filename}' criado com sucesso!")


# Função para carregar o grafo a partir do CSV
def load_graph_from_csv(filename):
    graph = {}
    
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for row in reader:
            origem, destino = row[0], row[1]
            distancia = int(row[2])
            
            if origem not in graph:
                graph[origem] = []
            if destino not in graph:
                graph[destino] = []
                
            graph[origem].append((destino, distancia))
            graph[destino].append((origem, distancia)) 

    return graph

# Carregar o grafo
grafo = load_graph_from_csv(filename)

# Escolher o algoritmo
print("\nEscolha o algoritmo:")
print("1 - A*")
print("2 - Dynamic A* (D*)")
print("3 - Anytime D*")

alg_opcao = input("Opção: ")

# Escolher pontos do grafo
start = input("Digite o ponto inicial: ").strip().upper()
goal = input("Digite o ponto final: ").strip().upper()

if start in grafo and goal in grafo:
    if alg_opcao == "1":
        path, cost = aStar(grafo, start, goal)
        print(f"\nCaminho encontrado (A*): {path}")
        print(f"Custo total: {cost} km")

    elif alg_opcao == "2":
        path, cost = dynamic_aStar(grafo, start, goal)
        print(f"\nCaminho encontrado (D*): {path}")
        print(f"Custo total: {cost} km")
    
    elif alg_opcao == "3":
        path, cost = anytime_DStar(grafo, start, goal)
        print(f"\nCaminho encontrado (Anytime D*): {path}")
        print(f"Custo total: {cost} km")
    
    else:
        print("Opção inválida!")

else:
    print("Pontos inválidos!")