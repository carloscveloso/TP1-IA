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

    df["distance_km"] = pd.to_numeric(df["distance_km"], errors='coerce')
    df["fuel"] = pd.to_numeric(df["fuel"], errors='coerce')
    df["toll"] = pd.to_numeric(df["toll"], errors='coerce')
    
    # Verificar se o CSV foi carregado corretamente
    print("Dados carregados:")
    print(df.head())

    df = df.fillna({
        "distance_km": np.inf,
        "fuel": np.inf,
        "toll": np.inf
    })
    
    # Criar lista única de cidades
    cities = list(set(df["origin_city"].tolist() + df["destination_city"].tolist()))
    n = len(cities)

    # Criar matriz de adjacência inicializada com infinito (sem conexão)
    adj_matrix = np.full((n, n, 3), np.inf)  
    np.fill_diagonal(adj_matrix[:, :, 0], 0)  
    np.fill_diagonal(adj_matrix[:, :, 1], 0)  
    np.fill_diagonal(adj_matrix[:, :, 2], 0) 
    
    # Criar mapeamento de índices das cidades
    city_to_index = {city: i for i, city in enumerate(cities)}
    
    # Verificar se as cidades estão corretas
    print("Cidades detectadas:")
    print(cities)
    
    # Preencher a matriz com distâncias, combustível e portagens
    for _, row in df.iterrows():
        i, j = city_to_index[row["origin_city"]], city_to_index[row["destination_city"]]
        
        # Debug: Mostrar o que está sendo atribuído
        print(f"Processando: {row['origin_city']} -> {row['destination_city']} | Distância: {row['distance_km']} | Combustível: {row['fuel']} | Portagens: {row['toll']}")
        
        adj_matrix[i, j] = [row["distance_km"], row["fuel"], row["toll"]]
        adj_matrix[j, i] = [row["distance_km"], row["fuel"], row["toll"]] 
    
    # Converter a matriz para DataFrame para melhor visualização
    adj_matrix_df = pd.DataFrame(adj_matrix[:, :, 0], index=cities, columns=cities)
    print("\nMatriz de Distância (km):")
    print(adj_matrix_df)
    
    adj_matrix_df_fuel = pd.DataFrame(adj_matrix[:, :, 1], index=cities, columns=cities)
    print("\nMatriz de Combustível (litros):")
    print(adj_matrix_df_fuel)
    
    adj_matrix_df_toll = pd.DataFrame(adj_matrix[:, :, 2], index=cities, columns=cities)
    print("\nMatriz de Pedágio (toll):")
    print(adj_matrix_df_toll)
    
    return adj_matrix, cities
