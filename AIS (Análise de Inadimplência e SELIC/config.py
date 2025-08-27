'''
Autor: Gustavo Mathias
Data: 27/08/2025
Versão: v1.0.0

'''

# Caminho do banco de dados
DB_PATH = "bancodedadosAIS.db"
FLASK_DEBUG = True
FLASK_HOST = '127.0.0.1'
FLASK_PORT = 5000
ROTAS = ['/',
         '/upload',
         '/consultar',
         '/graficos',
         '/editar_inadimplencia',
         '/editar_selic',
         '/correlacao',
         '/grafico_3d']