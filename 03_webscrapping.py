# Introdução ao WebScrapping -> Aplicável a qualquer cenário
# Bibliotecas: beautifulsoup e pyautogui
# https://www.adorocinema.com -> Site de referência

import requests, pandas as pd, time, random, sqlite3, datetime, math
from bs4 import BeautifulSoup as bs
# Beautiful Soup ->  Biblioteca para passar (analisar) HTML e extrair informações

# Headers para simular um navegador real (alguns sites bloqueim "bots", então fingimos ser o Google Chrome)
headers = {
    'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36'
}

baseURL = "https://www.adorocinema.com/filmes/melhores/"
filmes = [] # Lista que vai armazenar os dados coletados de cada filme
data_hoje = datetime.date.today().strftime("%d-%m-%Y")
agora = datetime.datetime.now()
pgLimite = int(input("Insira quantas páginas deseja realizar a operação \n"))


card_temp_min = 1
card_temp_max = 3
pag_temp_min = 2
pag_tempo_max = 5
bancoDados = "C:/Users/integral/Desktop/M2 Python Gustavo/banco_filmes.db"
saidaCSV = f"filmes_adorocinema_{data_hoje}.csv"



for pagina in range (1, pgLimite + 1):
    url = f"{baseURL}/?page={pagina}"
    print(f"Coletando dados da página {pagina}: \n{url}")
    resposta = requests.get(url, headers=headers)
    soup = bs(resposta.text, "html.parser")
    
        # Se o site não responder, pula para a próxima página
    if resposta.status_code != 200 :
        print(f"Erro ao carregar a página {pagina}. \nCódigo do Erro {resposta.status_code}")
        continue
    
    # Cada filme aparece em uma div(card) com a classe abaixo
    cards = soup.find_all("div", class_="card entity-card entity-card-list cf")
    # Iteramos por cada card(div) de filme
    for card in cards :
        try:
            # Capturar o título e link da página do filme
            titulo_tag = card.find("a", class_="meta-title-link")
            titulo = titulo_tag.text.strip().title() if titulo_tag else "N/A"
            link = "https://www.adorocinema.com" + titulo_tag["href"] if titulo_tag else None
            
            # Capturar a nota do filme
            nota_tag = card.find("span", class_="stareval-note")
            nota = nota_tag.text.strip().replace(",",".") if nota_tag else "N/A"
            
            # Caso exista o link -> Acessar a página individual do site
            if link:
                filme_resposta = requests.get(link, headers=headers)
                filme_soup = bs(filme_resposta.text,"html.parser")
                
                # Capturando o diretor do filme
                diretor_tag = filme_soup.find("div",class_="meta-body-item meta-body-direction meta-body-oneline")
                if diretor_tag:
                    # Limpando o texto do diretor
                    diretor = diretor_tag.text.strip().replace("Direção:","").replace(",",".").replace("|","")
                else:
                    diretor = "N/A"
                diretor = diretor.replace("\n","").replace("\r","").strip()
                
            # Captura dos gêneros
            genero_block = filme_soup.find("div", class_="meta-body-info")
            if genero_block :
                generos_links = genero_block.find_all("a")
                generos = [g.text.strip() for g in generos_links]
                categoria = ",".join(generos[:3]) if generos else "N/A"
            else:
                categoria = "N/A"
                
            # Captura do Ano de Lançamento
            ano_tag = genero_block.find("span", class_="date") if genero_block else None
            ano = ano_tag.text.strip() if ano_tag else "N/A"
            
            # Só adiciona o filme se todos os dados principais existirem
            if titulo != "N/A" and link != "N/A" and nota != "N/A":
                filmes.append({
                    "Titulo": titulo,
                    "Direção": diretor,
                    "Nota": nota,
                    "Link": link,
                    "Ano": ano,
                    "Categoria": categoria
                    
                })
            else:
                print(f"{titulo} \nFilme incompleto ou erro na coleta de dados. ")
            # Aguardar um tempo aleatório entre os parâmetros escolhidos para não sobrecarregar o site e nem revelar que somos um BOT
            tempo = random.uniform(card_temp_min, card_temp_max)
            tempo_ajustado = math.ceil(tempo)
            time.sleep(tempo)
            print(f"Tempo de espera: {tempo_ajustado} segundos")
        except Exception as e:
            print(f"Erro ao processor o filme {titulo}. \nErro: {e}")
    # Esperar um tempo entre realizar uma operação em uma página e outra
    tempopg = random.uniform(pag_temp_min, pag_tempo_max)
    time.sleep(tempopg)
    print(f"Tempo de espera: {tempopg:.0f} segundos")

# Converter os dados coletados para um dataframe do pandas

df = pd.DataFrame(filmes)
print(df.head())

# Salva os dados em um arquivo csv
df.to_csv(saidaCSV, index=False, encoding="utf-8-sig", quotechar="'", quoting=1)

# Conecta um banco de dados SQLite (cria se não existir)
conn = sqlite3.connect(bancoDados)
cursor = conn.cursor()
cursor.execute('''
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Titulo TEXT,
            Direcao TEXT,
            Nota REAL,
            Link TEXT,
            Ano TEXT,
            Categoria TEXT
                ) 
''')

# Inserir cada filme coletado dentro da tabela no banco de dados

for filme in filmes:
    try:
        cursor.execute('''
                INSERT INTO filmes (titulo, Direcao, Nota, Link, Ano, Categoria) VALUES (?,?,?,?,?,?)
                       ''',(
                           filme['Titulo'],
                           filme['Direção'],
                           float(filme['Nota']) if filme['Nota'] != "N/A" else None,
                           filme['Link'],
                           filme['Ano'],
                           filme['Categoria']
                       ))
    except Exception as e:
        print(f"Erro ao inserir filme {filme['Titulo']} no banco de dados. \n Código de identificação do erro: {e}")
conn.commit()
conn.close()

print("------------------------------------")
print("Dados raspados e salvos com sucesso!")
print(f"\n Arquivo salvo em {saidaCSV}\n")
print(f"Obrigado por usar o Sistema de Bot do GMS")
print("------------------------------------")