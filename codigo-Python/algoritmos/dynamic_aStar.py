import csv
import heapq

filename = "trajetos.csv"

with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(["A", "F", 30, 4, 5])
    writer.writerow(["F", "B", 20, 3, 4])
    writer.writerow(["B", "C", 15, 2, 3])
    writer.writerow(["C", "D", 25, 4, 6])
    writer.writerow(["D", "E", 10, 1, 2])
    writer.writerow(["E", "A", 35, 5, 7])

    print(f"Ficheiro '{filename}' criado com sucesso!")

def load_graph(filename):
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

def heuristic(node, destino):
    return 0

def dynamic_aStar(graph, start, goal, max_cost):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    goal_score = {node: float('inf') for node in graph}
    goal_score = [start] = 0

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        for neighbor, distancia, _, _ in graph[current]: 
            tentative_g_score = goal_score[current] + distancia

            if tentative_g_score < goal_score[neighbor]:
                came_from[neighbor] = current
                goal_score[neighbor] = tentative_g_score
                heapq.heappush(open_set, (tentative_g_score + heuristic(neighbor, goal), neighbor))

    return None  

def update_graph(graph, origem, destino, nova_distancia, novo_combustivel, novo_tempo):
    if origem in graph:
        for i, (n, d, c, t) in enumerate(graph[origem]):
            if n == destino:
                graph[origem][i] = (destino, nova_distancia, novo_combustivel, novo_tempo)

    if destino in graph:
        for i, (n, d, c, t) in enumerate(graph[destino]):
            if n == origem:
                graph[destino][i] = (origem, nova_distancia, novo_combustivel, novo_tempo)

grafo = load_graph(filename)

caminho = dynamic_aStar(grafo, "A", "E", 100)
print(f"Caminho inicial de A para E: {caminho}")

update_graph(grafo, "A", "E", 50, 3, 4)

novo_caminho = dynamic_aStar(grafo, "A", "E", 100)
print(f"Caminho atualizado de A para E: {novo_caminho}")

