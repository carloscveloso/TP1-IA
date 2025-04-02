import pandas as pd
import numpy as np

# Função para importar o CSV para uma matriz de adjacência com três variáveis
def importar_grafo(csv_file):
    # Carregar o CSV (ajuste conforme necessário se o delimitador for diferente)
    df = pd.read_csv(csv_file, delimiter=',')
    df.columns = df.columns.str.strip()

    print("Colunas do DataFrame:", df.columns.tolist())

    df["origin_city"] = df["origin_city"].str.strip()
    df["destination_city"] = df["destination_city"].str.strip()

    df["distance_km"] = pd.to_numeric(df["distance_km"], errors='coerce').astype(np.float64)
    df["fuel"] = pd.to_numeric(df["fuel"], errors='coerce').astype(np.float64)
    df["toll"] = pd.to_numeric(df["toll"], errors='coerce').astype(np.float64)
    
    # Verificar se o CSV foi carregado corretamente
    print("Dados carregados:")
    print(df.head())

    df = df.fillna({
        "distance_km": np.nan,
        "fuel": np.nan,
        "toll": np.nan
    })
    
    # Criar lista única de cidades
    cities = sorted(set(df["origin_city"].tolist() + df["destination_city"].tolist()))
    n = len(cities)

    # Criar matriz de adjacência inicializada com infinito (sem conexão)
    adj_matrix = np.full((n, n, 3), np.nan)  
    np.fill_diagonal(adj_matrix[:, :, 0], 0.0)  
    np.fill_diagonal(adj_matrix[:, :, 1], 0.0)  
    np.fill_diagonal(adj_matrix[:, :, 2], 0.0)     
    
    # Criar mapeamento de índices das cidades
    city_to_index = {city: i for i, city in enumerate(cities)}
    
    # Preencher a matriz com distâncias, combustível e portagens
    for _, row in df.iterrows():
        i, j = city_to_index[row["origin_city"]], city_to_index[row["destination_city"]]
        
        # Debug: Mostrar o que está sendo atribuído
        print(f"Processando: {row['origin_city']} -> {row['destination_city']} | Distância: {row['distance_km']} | Combustível: {row['fuel']} | Portagens: {row['toll']}")
        
        adj_matrix[i, j] = [row["distance_km"], row["fuel"], row["toll"]]
        adj_matrix[j, i] = [row["distance_km"], row["fuel"], row["toll"]] 
    
    return adj_matrix, cities
