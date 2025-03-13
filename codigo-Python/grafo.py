import csv
import heapq

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

print(f"Ficheiro '{filename}' criado com sucesso!")


# Função para carregar o grafo a partir do CSV
def load_graph_from_csv(filename):
    graph = {}
    
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for row in reader:
            origem, destino = row[0], row[1]
            distancia = int(row[2])
            combustivel = int(row[3])
            tempo = int(row[4])

            # Adicionar ao grafo bidirecional
            if origem not in graph:
                graph[origem] = []
            if destino not in graph:
                graph[destino] = []
                
            graph[origem].append((destino, distancia, combustivel, tempo))
            graph[destino].append((origem, distancia, combustivel, tempo))  # Se for bidirecional

    return graph


# Heurística simples (para melhorar, poderia ser a distância real)
def heuristic(nodo, destino):
    return 0


# Algoritmo A* padrão
def a_star(graph, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, start, goal, g_score)

        for neighbor, distancia, _, _ in graph[current]:
            tentative_g_score = g_score[current] + distancia

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                heapq.heappush(open_set, (tentative_g_score + heuristic(neighbor, goal), neighbor))

    return None


# Algoritmo Dynamic A* (D*)
def d_star(graph, start, goal):
    return a_star(graph, start, goal)  # Neste caso, estamos usando A* como base


# Função para reconstruir o caminho e calcular o custo total
def reconstruct_path(came_from, start, goal, g_score):
    path = []
    current = goal
    total_cost = g_score[goal]

    while current in came_from:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()
    
    return path, total_cost


# Carregar o grafo
grafo = load_graph_from_csv(filename)

# Escolher o algoritmo
print("\nEscolha o algoritmo:")
print("1 - A*")
print("2 - Dynamic A* (D*)")

alg_opcao = input("Opção: ")

# Escolher pontos do grafo
start = input("Digite o ponto inicial: ").strip().upper()
goal = input("Digite o ponto final: ").strip().upper()

if start in grafo and goal in grafo:
    if alg_opcao == "1":
        path, cost = a_star(grafo, start, goal)
        print(f"\nCaminho encontrado (A*): {path}")
        print(f"Custo total: {cost} km")

    elif alg_opcao == "2":
        path, cost = d_star(grafo, start, goal)
        print(f"\nCaminho encontrado (D*): {path}")
        print(f"Custo total: {cost} km")

    else:
        print("Opção inválida!")

else:
    print("Pontos inválidos!")