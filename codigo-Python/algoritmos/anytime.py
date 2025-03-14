import heapq

class AnytimeDStar:
    def __init__(self, graph, heuristic, epsilon=2.5):
        self.graph = graph  # O grafo
        self.heuristic = heuristic  # A heurística
        self.epsilon = epsilon  # Fator de inflação
        self.g_values = {node: float('inf') for node in graph}  # Custo acumulado
        self.rhs_values = {node: float('inf') for node in graph}  # Melhor estimativa de custo
        self.OPEN = []  # Fila de prioridade
        self.parents = {}  # Para reconstrução do caminho
        self.km = 0  # Número de mudanças

    def initialize(self, start, goal):
        """Inicializa os valores e a fila de prioridade"""
        self.g_values[goal] = float('inf')
        self.rhs_values[goal] = 0
        heapq.heappush(self.OPEN, (self.compute_key(goal), goal))
        self.g_values[start] = 0  # A inicialização de A deve ser 0, não inf
        heapq.heappush(self.OPEN, (self.compute_key(start), start))  # Incluir A na fila
        print(f"Inicialização do nó de destino: {goal}, Chave: {self.compute_key(goal)}")

    def compute_key(self, node):
        """Calcula a chave de prioridade do nó"""
        min_g_rhs = min(self.g_values[node], self.rhs_values[node])
        return (min_g_rhs + self.epsilon * self.heuristic[node], min_g_rhs)

    def update_vertex(self, node):
        """Atualiza o nó e suas conexões na fila OPEN"""
        if node in self.OPEN:
            self.OPEN.remove((self.compute_key(node), node))
            heapq.heapify(self.OPEN)
        
        if self.g_values[node] != self.rhs_values[node]:
            heapq.heappush(self.OPEN, (self.compute_key(node), node))

    def improve_path(self, start):
        """Melhoria do caminho"""
        while self.OPEN:
            # Print para depuração
            print(f"\nOPEN: {self.OPEN}")

            _, current = heapq.heappop(self.OPEN)

            if self.g_values[current] > self.rhs_values[current]:
                self.g_values[current] = self.rhs_values[current]
            else:
                self.g_values[current] = float('inf')
                self.update_vertex(current)

            for neighbor, cost in self.graph.get(current, []):
                print(f"Vizinhos de {current}: {neighbor}, Custo: {cost}")
                if neighbor != current:
                    # Atualiza rhs para o vizinho
                    if self.rhs_values[neighbor] > self.g_values[current] + cost:
                        self.rhs_values[neighbor] = self.g_values[current] + cost
                        self.parents[neighbor] = current
                    self.update_vertex(neighbor)

    def replan(self, start, goal):
        """Executa o algoritmo Anytime D*"""
        print(f"Iniciando replanejamento de {start} a {goal}")
        self.initialize(start, goal)
        self.improve_path(start)

        path = self.reconstruct_path(start, goal)
        return path, self.g_values[start]

    def reconstruct_path(self, start, goal):
        """Reconstrói o caminho mais curto"""
        print(f"Reconstruindo caminho de {start} a {goal}")
        path = [start]
        current = start
        while current != goal:
            if current not in self.parents:
                print(f"Sem caminho encontrado para {current}")
                return None  # Sem caminho possível
            current = self.parents.get(current)
            path.append(current)
        return path

    def update_cost(self, node1, node2, new_cost):
        """Atualiza o custo de uma aresta"""
        print(f"Atualizando custo de {node1} para {node2} para {new_cost}")
        for i, (neighbor, _) in enumerate(self.graph[node1]):
            if neighbor == node2:
                self.graph[node1][i] = (neighbor, new_cost)
        for i, (neighbor, _) in enumerate(self.graph[node2]):
            if neighbor == node1:
                self.graph[node2][i] = (neighbor, new_cost)

        self.km += 1
        self.update_vertex(node1)
        self.update_vertex(node2)

# ====== TESTE ======
graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('D', 5)],
    'C': [('A', 2), ('D', 8), ('E', 10)],
    'D': [('B', 5), ('C', 8), ('F', 6)],
    'E': [('C', 10), ('F', 3)],
    'F': [('D', 6), ('E', 3)],
}

heuristic = {'A': 10, 'B': 8, 'C': 7, 'D': 5, 'E': 3, 'F': 0}

dstar = AnytimeDStar(graph, heuristic, epsilon=2.5)
best_path, best_cost = dstar.replan('A', 'F')

print(f"\nCaminho inicial: {best_path}, Custo: {best_cost}")

print("\n\n\n\n\n\n\n\n")
exit()
# Simulando mudança de custo
dstar.update_cost('C', 'D', 3)
best_path, best_cost = dstar.replan('A', 'F')

print(f"\nCaminho atualizado após mudança: {best_path}, Custo: {best_cost}")