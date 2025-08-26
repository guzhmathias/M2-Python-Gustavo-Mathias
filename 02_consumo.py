from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio
import random
import configuracoes_sql as config
import configuracoes_html as configpg

caminhoBanco = config.DB_PATH
queryVerVingadores = config.consulta01
queryGrafico1 = config.consulta02
queryApagar = config.consulta03
#configura o plotly para abrir os arquivos no navegador por padrão
pio.renderers.default = "browser"

#carregar o arquivo drinks.csv
dfDrinks = pd.read_csv(r"C:/Users/integral\Desktop/M2 Python Gustavo/drinks.csv")
dfAvengers = pd.read_csv(r"C:/Users/integral/Desktop/M2 Python Gustavo/avengers.csv", encoding='latin1')
#outros encodings de exemplo: uft-16 , cp1252, iso8859-1

#criar o banco de dados em sql e popular com os dados do csv
conn = sqlite3.connect(caminhoBanco)

#inserir as duas novas tabelas no banco de dados
dfDrinks.to_sql("bebidas", conn, if_exists="replace", index=False)
dfAvengers.to_sql("vingadores", conn, if_exists="replace", index=False)
conn.commit()
conn.close()

html_template = configpg.pInit

#iniciar o flask
app = Flask(__name__)


@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/grafico1')
def grafico1():
    with sqlite3.connect(caminhoBanco) as conn:
        df = pd.read_sql_query(queryGrafico1, conn)
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
    with sqlite3.connect(caminhoBanco) as conn:
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
    with sqlite3.connect(caminhoBanco) as conn:
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
    with sqlite3.connect(caminhoBanco) as conn:
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
        conn = sqlite3.connect(caminhoBanco)
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

@app.route('/ver_tabela')
def ver_vingadores():
    conn = sqlite3.connect(caminhoBanco)
    try:
        dfAvengers = pd.read_sql_query(queryVerVingadores, conn)
    except Exception as erro:
        conn.close()
        return f"<h3>Erro ao consultar a tabela {str(erro)}</h3><br><a href='/'> Voltar </a>"
    if dfAvengers.empty:
        conn.close()
        return f"<h3>A tabela de Vingadores não existe ou está vazia!</h3><br><a href='/'> Voltar </a>"
    return dfAvengers.to_html(index=False) + "<br><a href='/'> Voltar </a>"

@app.route('/apagar_avengers')
def apagar_avengers():
    conn = sqlite3.connect(caminhoBanco)
    cursor = conn.cursor()
    try:
        cursor.execute(queryApagar)
        conn.commit()
        mensagem = "<h3>A tabela de Vingadores foi apagada com sucesso!</h3>"
    except Exception as erro:
        mensagem = f"<h3>Erro ao deletar a tabela {str(erro)}</h3><br><a href='/'> Voltar </a>"

    return mensagem + "<br><a href='/'> Voltar </a>"
        

#iniciar o servidor 
if __name__ == '__main__':
    app.run(debug=True)