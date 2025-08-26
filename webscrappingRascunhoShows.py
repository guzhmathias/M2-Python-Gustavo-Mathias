import requests, pandas as pd, time, random, sqlite3, datetime, math
from bs4 import BeautifulSoup as bs

headers = {
    'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36'
}

baseURL = "https://www.sampaingressos.com.br/templates/ajax/lista_espetaculo.php"
shows = []
data_hoje = datetime.date.today().strftime("%d-%m-%Y")
agora = datetime.datetime.now()
pgLimite = 1
card_temp_min = 1
card_temp_max = 3
pag_temp_min = 2
pag_tempo_max = 5
bancoDados = "C:/Users/integral/Desktop/M2 Python Gustavo/banco_shows.db"
saidaCSV = f"C:/Users/integral/Desktop/M2 Python Gustavo/shows_sampaingressos_{data_hoje}.csv"

for pagina in range (1, pgLimite + 1):
    url = f"{baseURL}?pagina={pagina}&tipoEspetaculo=shows"
    print(f"Coletando dados da página {pagina}: \n{url}")
    resposta = requests.get(url, headers=headers)
    soup = bs(resposta.text, "html.parser")
    
    if resposta.status_code != 200 :
        print(f"Erro ao carregar a página {pagina}. \nCódigo do Erro {resposta.status_code}")
        continue
    cards = soup.find_all("div", id="box_espetaculo")
    for card in cards :
        try:
            titulo_tag = card.find("b", class_="titulo")
            local_tag = card.find("span", class_="local")
            horario_tag = card.find("span", class_="horario")
            
            titulo = titulo_tag.text.strip() if titulo_tag else "N/A"
            local = local_tag.text.strip() if local_tag else "N/A"
            horario = horario_tag.text.strip() if horario_tag else "N/A"
            if titulo != "N/A" :
                shows.append({
                    "Titulo": titulo,
                    "Local": local,
                    "Horario": horario   
                })
            else:
                print("Card sem título")
            
            tempo = random.uniform(card_temp_min, card_temp_max)
            time.sleep(tempo)
        except Exception as e:
            print(f"Erro ao processor o show {titulo}. \nErro: {e}")
            
    tempopg = random.uniform(pag_temp_min, pag_tempo_max)
    time.sleep(tempopg)
            

df = pd.DataFrame(shows)
print(shows)
print(df.head())

df.to_csv(saidaCSV, index=False, encoding="utf-8-sig", quotechar="'", quoting=1)

conn = sqlite3.connect(bancoDados)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS shows(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Titulo TEXT,
        Local TEXT,
        Horario TEXT
    ) 
''')

for show in shows:
    try:
        cursor.execute('''
            INSERT INTO shows (Titulo, Local, Horario) VALUES (?,?,?)
        ''',(
            show['Titulo'],
            show['Local'],
            show['Horario']
        ))
    except Exception as e:
        print(f"Erro ao inserir show {show['Titulo']} no banco de dados. \n Código de identificação do erro: {e}")
        
conn.commit()
conn.close()

print("------------------------------------")
print("Dados raspados e salvos com sucesso!")
print(f"\n Arquivo salvo em {saidaCSV}\n")
print(f"Obrigado por usar o Sistema de Bot do GMS")
print("------------------------------------")