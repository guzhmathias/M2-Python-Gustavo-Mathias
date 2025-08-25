from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio
import random

#configura o plotly para abrir os arquivos no navegador por padrão
pio.renderers.default = "browser"

#carregar o arquivo drinks.csv
dfDrinks = pd.read_csv(r"C:/Users/integral\Desktop/M2 Python Gustavo/drinks.csv")
dfAvengers = pd.read_csv(r"C:/Users/integral/Desktop/M2 Python Gustavo/avengers.csv", encoding='latin1')
#outros encodings de exemplo: uft-16 , cp1252, iso8859-1

#criar o banco de dados em sql e popular com os dados do csv
conn = sqlite3.connect(r"C:/Users/integral/Desktop/M2 Python Gustavo/bancodados.db")

#inserir as duas novas tabelas no banco de dados
dfDrinks.to_sql("bebidas", conn, if_exists="replace", index=False)
dfAvengers.to_sql("vingadores", conn, if_exists="replace", index=False)
conn.commit()
conn.close()

html_template = '''
            <style>
    body {
        font-family: "Poppins", sans-serif;
        background-image: linear-gradient(to right, #4facfe, #00f2fe);
        color: #333;
        margin: 0;
        padding: 20px;
    }
    .container {
        max-width: 900px;
        margin: 40px auto;
        background-color: rgba(255, 255, 255, 0.95);
        padding: 50px;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    }
    h1 {
        text-align: center;
        color: #0d47a1;
        font-size: 3em;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    h2 {
        color: #1a237e;
        border-bottom: 3px solid #00f2fe;
        padding-bottom: 5px;
        margin-top: 40px;
    }
    ul {
        list-style-type: none;
        padding: 0;
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center;
    }
    li a {
        display: block;
        padding: 20px 25px;
        background-color: #fff;
        border: 2px solid #00f2fe;
        color: #00897b;
        text-decoration: none;
        border-radius: 10px;
        transition: all 0.3s ease;
        font-weight: 600;
        text-align: center;
        min-width: 200px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    li a:hover {
        background-color: #00f2fe;
        color: #fff;
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
</style>

<div class="container">
    <h1>Dashboard - Consumo de Álcool</h1>
    <h2>Parte 01</h2>
    <ul>
        <li><a href="/grafico1">Top 10 países em consumo de álcool</a></li>
        <li><a href="/grafico2">Média de consumo por tipo de bebida</a></li>
        <li><a href="/grafico3">Consumo total por região</a></li>
        <li><a href="/grafico4">Comparativo entre tipos de bebidas</a></li>
        <li><a href="/pais?nome=Brazil">Insights por país (Brasil)</a></li>
    </ul>

    <h2>Parte 02</h2>
    <ul>
        <li><a href="/comparar">Comparar</a></li>
        <li><a href="/upload_avengers">Upload CSV</a></li>
        <li><a href="/apagar_avengers">Apagar Tabela Avengers</a></li>
        <li><a href="/atribuir_paises_avengers">Atribuir Países</a></li>
        <li><a href="/ver_tabela">Ver Tabela Avengers</a></li>
        <li><a href="/consultar_avengers">Consultar detalhes do Vingador</a></li>
        <li><a href="/avengers_vs_drinks">V.A.A (Vingadores Alcoólicos Anônimos)</a></li>
    </ul>
</div>

'''

#iniciar o flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/grafico1')
def grafico1():
    with sqlite3.connect(r"C:/Users/integral/Desktop/M2 Python Gustavo/bancodados.db") as conn:
        df = pd.read_sql_query("""
            SELECT country, total_litres_of_pure_alcohol
            FROM bebidas
            ORDER BY total_litres_of_pure_alcohol DESC
            LIMIT 10                            
                               """, conn)
    figuraGrafico01 = px.bar(
        df, 
        x = "country",
        y = "total_litres_of_pure_alcohol",
        title="Top 10 países com o maior consumo de alcool"
    )
    return figuraGrafico01.to_html() + "<br><a href='/'> Voltar </a>"

#Grafico 2 - Média por tipo global
@app.route('/grafico2')
def grafico2():
    with sqlite3.connect(r"C:/Users/integral/Desktop/M2 Python Gustavo/bancodados.db") as conn:
        df = pd.read_sql_query("""
            SELECT AVG(beer_servings) AS cerveja, AVG(spirit_servings) AS destilados, AVG(wine_servings) AS vinhos FROM bebidas   
                               """, conn)
        
        # Função Melt: transforma as colunas (cerbeja, destilados, vinhos) em linhas, criando colunas
        # Uma chamada Bebidas com os nomes originais das colunas
        # Outra chama Media de Porções com os valores correspondentes
        df_melted = df.melt(var_name="Bebidas", value_name='Media de Porções')
        
    figuraGrafico02 = px.bar(
       df_melted,
       x="Bebidas",
       y="Media de Porções",
       title="Média de consumo global por tipo"
    )
    return figuraGrafico02.to_html() + "<br><a href='/'> Voltar </a>"

@app.route('/grafico3')
def grafico3():
    regioes = {
        "Europa":['France','Germany','Italy','Spain','Portugal'],
        "Asia":['China','Japan','India','Thailand'],
        "Africa":['Angola','Nigeria','Egypt','Algeria'],
        "Americas":['Brazil','USA','Canada','Argentina','Mexico']
    }
    dados = []
    with sqlite3.connect(r"C:/Users/integral/Desktop/M2 Python Gustavo/bancodados.db") as conn:
        # Itera sobre o dicionario de regioes onde cada chave (região) tem uma lista de paises
        for regiao, paises in regioes.items():
            # Criando a linha de placeholders para os paises dessa região no formato "pais1", "pais2", ..., "paisN".
            # Isso vai ser utilizado na consulta SQL para filtrar os países da região
            placeholders = ','.join([f"'{p}'" for p in paises])
            query = f"""
                    SELECT SUM(total_litres_of_pure_alcohol) AS total
                    FROM bebidas
                    WHERE country IN ({placeholders})
            """
            # Como a consulta vai retornar um único valor (soma), pegamos o primeiro valor usando o [0] se o resultado for none (sem dados), retornamos  0 para evitar erros
            total = pd.read_sql_query(query, conn).iloc[0, 0]
            # Adicionar o resultado ao dicionário "dados", para cada região com o consumo total calculado
            dados.append({"Região": regiao, "Consumo Total": total})
    dfRegioes = pd.DataFrame(dados)
    figuraGrafico03 = px.pie(
        dfRegioes,
        names="Região",
        values="Consumo Total",
        title = "Consumo Total por Região"
        )
    return figuraGrafico03.to_html() + "<br><a href='/'> Voltar </a>"

# Gráfico 4: comparativo dos tipos de bebidas
@app.route('/grafico4')   
def grafico4():
    with sqlite3.connect(r"C:/Users/integral/Desktop/M2 Python Gustavo/bancodados.db") as conn:
        df = pd.read_sql_query("""
            SELECT beer_servings, spirit_servings, wine_servings FROM bebidas""", conn)
        medias = df.mean().reset_index()
        medias.columns = ["Tipo", "Media"]
        figuraGrafico04 = px.pie(
            medias,
            names="Tipo",
            values="Media",
            title="Proporção media entre os tipos de bebidas"
        )
        return  "<br><a href='/'> Voltar </a>" + figuraGrafico04.to_html() 
    
@app.route('/comparar', methods=['GET','POST'])
def comparar():
    opcoes = ['beer_servings','spirit_servings','wine_servings','total_litres_of_pure_alcohol']
    
    if request.method == 'POST':
        # Lógica para mostrar o gráfico quando tem POST ao acessar a página
        eixo_x = request.form.get('eixo_x')
        eixo_y = request.form.get('eixo_y')
        if eixo_x == eixo_y:
            return "<h3>Selecione campos diferentes!</h3>"
        
        conn = sqlite3.connect(r"C:/Users/integral/Desktop/M2 Python Gustavo/bancodados.db")
        df = pd.read_sql_query("SELECT country, {}, {} FROM bebidas".format(eixo_x,eixo_y), conn)
        conn.close()
        figuraComparar = px.scatter(
            df,
            x=eixo_x,
            y=eixo_y,
            title=f"Comparação entre {eixo_x} e {eixo_y}"
        )
        figuraComparar.update_traces(textposition='top center')
        return "<br><a href=/> Voltar </a>" + figuraComparar.to_html()
    # Aqui é a página sem post, ou seja, a primeira vez que o usuário entra na página
    return render_template_string('''
            <h2>Comparar Campos</h2> 
            <form method="POST">
                <label>Eixo X</label>
                <select name="eixo_x">
                    {% for opcao in opcoes %}
                        <option value="{{opcao}}">{{opcao}}</option>
                    {% endfor%}
                    
                </select>
                <br></br>
                <label>Eixo Y</label>
                <select name="eixo_y">
                    {% for opcao in opcoes %}
                        <option value="{{opcao}}">{{opcao}}</option>
                    {% endfor%}
                </select>
                <br></br>
                <input type="submit" value="-- Comparar --">
            </form>
        ''', opcoes = opcoes)
    
@app.route('/upload_avengers', methods=['GET','POST'])
def upload_avengers():   
    if request.method == 'POST':
        #Recebe um arquivo, então vamos cadastrara no banco
        recebido = request.files["arquivo"]
        if not recebido:
            return "<h3>Nenhum arquivo recebido</h3><br><a href='/upload_avengers'> Voltar </a> "
        dfAvengers = pd.read_csv(recebido, encoding='latin1')
        conn = sqlite3.connect(r"C:/Users/integral/Desktop/M2 Python Gustavo/bancodados.db")
        dfAvengers.to_sql("vingadores", conn, if_exists="replace", index=False)
        conn.commit()
        conn.close()
        return"<h3>Arquivo inserido com sucesso!</h3><br><a href='/'> Voltar </a>"
    #Acessar esta rota pela primeira vez (sem post) cai neste html
    return '''
        <h2>Upload da Tabela Avengers</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="arquivo" accept=".csv"><br>
            <input type="submit" value="-- Enviar --"><br>
        </form>
    '''
#iniciar o servidor 
if __name__ == '__main__':
    app.run(debug=True)