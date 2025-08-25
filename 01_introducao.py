import pandas as pd

# Armazena a string do caminho
caminho = 'C:/Users/integral/Desktop/M2 Python Gustavo/01_base_vendas.xlsx'

# Lendo excel, é necessário especificar a planilha que você quer analisar com o pandas
df1 = pd.read_excel(caminho, sheet_name='Relatório de Vendas')
df2 = pd.read_excel(caminho, sheet_name='Relatório de Vendas1')

print(f'Primeiro relatório de vendas: \n{df1.head()}\nSegundo Relatório de vendas: \n{df2.head()}')

# Juntando 2 tabelas/dataframes em um único dataframe consolidado (Concatenar)
# o ignore index vai farantir que o indice seja reordenado após a junção
dfConsolidado = pd.concat([df1,df2], ignore_index=True)

print(f'Df Consolidado {dfConsolidado.head()}')

# Verifica quantos dados duplicados existem dentro do relatório
print(f'Duplicados no novo relatório de vendas: \n {dfConsolidado.duplicated().sum()}')