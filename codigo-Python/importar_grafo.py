import csv
import numpy as np

def importar_grafo(nome_arquivo):
    indices = {}
    contador = 0

    # Primeira leitura para mapear os nós (origem e destino)
    with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  

        for row in reader:
            if len(row) >= 5:  
                origem, destino, *_ = row  
                if origem not in indices:
                    indices[origem] = contador
                    contador += 1
                if destino not in indices:
                    indices[destino] = contador
                    contador += 1

    tamanho = len(indices)
    matriz = np.full((tamanho, tamanho, 3), np.inf)  

    # Segunda leitura para preencher a matriz com distâncias, combustível e tempo
    with open(nome_arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  

        for row in reader:
            if len(row) >= 5:  
                origem, destino, toll, combustivel, distancia = row  
                origem_index = indices[origem]
                destino_index = indices[destino]
                matriz[origem_index, destino_index, 0] = float(distancia)  # Quilômetros
                matriz[origem_index, destino_index, 1] = float(combustivel)  # Litros de combustível
                minutos_estimados = float(distancia) / float(combustivel)  
                matriz[origem_index, destino_index, 2] = minutos_estimados  # Tempo em minutos
    return indices, matriz

