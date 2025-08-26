'''
__     __  _         _    
\ \   / / / \       / \   
 \ \ / / / _ \     / _ \  
  \ V / / ___ \ _ / ___ \  _
   \_(_)_/   \_(_)_/   \_\(_)
       
       Autor: Gustavo Mathias
       Versão: 0.0.1v 2025
'''


# Caminho da pasta
DB_PATH = 'C:/Users/integral/Desktop/M2 Python Gustavo/bancodados.db'


# Consulta Vingadores
consulta01 = "SELECT * FROM vingadores"
# Query grafico 1
consulta02 = """
            SELECT country, total_litres_of_pure_alcohol
            FROM bebidas
            ORDER BY total_litres_of_pure_alcohol DESC
            LIMIT 10                            
                               """
                               
consulta03 = """
DROP TABLE IF EXISTS vingadores

"""