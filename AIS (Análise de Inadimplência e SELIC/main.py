from flask import Flask, request, jsonify, render_template_string
import pandas as pd, sqlite3, os, plotly.graph_objs as go, dash, numpy as np, config, paginas
from dash import Dash, html, dcc
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
caminhoBd = config.DB_PATH
rot = config.ROTAS

def init_db():
    with sqlite3.connect(caminhoBd) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inadimplencia(
                mes TEXT PRIMARY KEY,
                inadimplencia REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selic (
                mes TEXT PRIMARY KEY,
                selic_diaria REAL
            )
        ''')
        conn.commit()
        
vazio = 0

@app.route(rot[0])
def index():
    return render_template_string(paginas.pgInicial)

@app.route(rot[1], methods=['POST','GET'])
def upload():
    inad_file = request.files.get('campo_inadimplencia')
    selic_file = request.files.get('campo_selic')
    
    if not inad_file or not selic_file:
        return jsonify({"Erro":"Ambos os arquivos devem ser enviados!"})
    
    inad_df = pd.read_csv(
        inad_file,
        sep = ';',
        names = ['data','inadimplencia'],
        header = 0
    )
    selic_df = pd.read_csv(
        selic_file,
        sep = ';',
        names = ['data','selic_diaria'],
        header = 0
    )
    
    inad_df['data'] = pd.to_datetime(
        inad_df['data'], format="%d/%m/%Y"
        )
    selic_df['data'] = pd.to_datetime(
        selic_df['data'], format="%d/%m/%Y"
        )
    
    inad_df['mes'] = inad_df['data'].dt.to_period('M').astype(str)
    selic_df['mes'] = selic_df['data'].dt.to_period('M').astype(str)
    
    inad_mensal = inad_df[['mes','inadimplencia']].drop_duplicates()
    selic_mensal = selic_df.groupby('mes')['selic_diaria'].mean().reset_index()
    
    with sqlite3.connect(caminhoBd) as conn:
        inad_df.to_sql(
            'inadimplencia',
            conn,
            if_exists='replace',
            index=False
        )
        selic_df.to_sql(
            'selic',
            conn,
            if_exists='replace',
            index=False
        )
    return jsonify({"Mensagem":"Dados Cadastrados com Sucesso!"})
    
    
@app.route(rot[2], methods=['POST','GET'])
def consultar():
    if request.method == "POST":
        tabela = request.form.get('campo_tabela')
        if tabela not in ['inadimplencia','selic']:
            return jsonify({"Erro":"Tabela Invalida"}),400
        with sqlite3.connect(caminhoBd) as conn:
            df_temp = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
        return df_temp.to_html(index=False)
            
    
    return render_template_string(paginas.pgConsulta)

@app.route(rot[3])
def graficos():
    with sqlite3.connect(caminhoBd) as conn:
        inad_df = pd.read_sql_query('SELECT * FROM inadimplencia', conn)
        selic_df = pd.read_sql_query('SELECT * FROM selic', conn)
    
    # Criação de um gráfico para Inadimplência utilizando o plotly.graph_objs
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x = inad_df['mes'],
        y = inad_df['inadimplencia'],
        mode = 'lines+markers',
        name = 'Inadimplência'
        ) 
    )
    fig1.update_layout(
        title = "Evolução da Inadimplência",
        xaxis_title = 'Mês',
        yaxis_title = '%',
        template = 'plotly_dark'
        # Lista de templates do plotly: ver documentação da biblioteca
    )
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x = selic_df['mes'],
        y = selic_df['selic_diaria'],
        mode = 'lines+markers',
        name = 'Selic'
        ) 
    )
    fig2.update_layout(
        title = "Evolução da Taxa Selic",
        xaxis_title = 'Mês',
        yaxis_title = '%',
        template = 'plotly_dark'
    )

    graph_html_1 = fig1.to_html(
        full_html = False,
        include_plotlyjs = "cdn"    
        )
    graph_html_2 = fig2.to_html(
        full_html = False,
        include_plotlyjs = False    
        )
    
    return render_template_string(paginas.pgGraficos, reserva01 = graph_html_1, reserva02 = graph_html_2)


@app.route(rot[4], methods=['POST','GET'])
def editar_inad():
    #Escolher data e valor para analisar  a inadimplencia e retorna para o gráfico
    if request.method =="POST":
        mes = request.form.get('campo_mes')
        novo_valor = request.form.get('campo_valor')
        try:
            novo_valor = float(novo_valor)
        except:
            return jsonify({"Erro":"Valor invalido"})
        with sqlite3.connect(caminhoBd) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE inadimplencia 
                SET inadimplencia = ? 
                WHERE mes = ?
            ''', (novo_valor, mes))
            conn.commit()
        return jsonify({"Mensagem":f"Valor atualizado para o mes {mes} com sucesso!"})
    return render_template_string(paginas.pgEditarInad)

@app.route(rot[5], methods=['POST','GET'])
def editar_selic():
    # Escolher data e valor para analisar  a selic e retorna para o gráfico
    if request.method =="POST":
        mes = request.form.get('campo_mes')
        novo_valor = request.form.get('campo_valor')
        if not mes or not novo_valor:
            return jsonify({"Erro":"Informe a data e o valor"}), 400
        try:
            novo_valor = float(novo_valor.replace(',','.'))
        except ValueError:
            return jsonify({"Erro":"Valor invalido"})
        with sqlite3.connect(caminhoBd) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE selic
                SET selic_diaria = ? 
                WHERE mes = ?
            ''', (novo_valor, mes))
            conn.commit()
        return jsonify({"Mensagem":f"Valor atualizado para o mes {mes} com sucesso!"})
    return render_template_string(paginas.pgEditarSelic)
    
    
@app.route(rot[6])
def correlacao():
    with sqlite3.connect(caminhoBd) as conn:
        inad_df = pd.read_sql_query(" SELECT * FROM inadimplencia", conn)
        selic_df = pd.read_sql_query(" SELECT * FROM selic", conn)
        
    # Juntar os dataframes de inadimplencia e selic usando a coluna de mês como chave de junção
    merged = pd.merge(inad_df, selic_df, on='mes') 
    
    # Correlação de Pearson: corr(Pandas) ou correl(Numpy)
    # Calcula o coeficiente da correlação de Pearson entre duas variáveis (Inadimplência e Selic)
    correl = merged['inadimplencia'].corr(merged['selic_diaria'])
    
    # Registro das variáveis para futuramente fazer a regressão linear, onde x é a variável independente (no caso a Selic)
    x = merged['selic_diaria']
    # y é a variável dependente
    y = merged['inadimplencia']
    
    # Cálculo do coeficiente da reta de regressão linear onde 'm' é a inclinação e 'b' é a interseção
    m, b = np.polyfit(x, y, 1)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x = x,
        y = y,
        mode = 'markers',
        name = 'Inadimplencia vs Selic',
        marker = dict(
            color = 'rgba(0, 123, 255, 0.8)',
            size = 12,
            line = dict(width = 2, color = 'white'), 
            symbol = 'circle'),
        hovertemplate = 'SELIC: %{x:.2f}%<br>Inadimplencia: %{y:.2f}%<extra></extra>'
            )
        )

    # Criar outro add_trace para adicionar a linha de tendência da regressão linear
    fig.add_trace(go.Scatter(
        x = x, # Usa o mesmo eixo dos dados
        y = m * x + b, # A equação da linha de tendência 
        mode = 'lines',
        name = 'Linha de tendência',
        line = dict(
            color = 'rgba(255, 53, 69, 1)',
            width = 4,
            dash = 'dot'
            )
        )
    )
    
    fig.update_layout(
        title = {
            'text':f'<b>Correlação entre Selic e Inadimplência</b><br><span style="font-size: 16px"> Coeficiente de Correlação {correl:.2f}</span>',
            'y':0.95, # Posição Vertical do Título (95% da Altura do Gráfico)
            'x':0.5, # Posição Horizontal do título (50% da Altura do Gráfico)
            'xanchor':'center', # Centraliza horizontalmente o título
            'yanchor':'top' # Alinha o título verticalmente o título ao topo
            },
        xaxis_title = dict(
            text = 'SELIC Média Mensal (%)',
            font = dict(
                size = 18,
                family = 'Arial',
                color = 'gray'
                )
            ),
        yaxis_title = dict(
            text = 'Inadimplência (%)',
            font = dict(
                size = 18,
                family = 'Arial',
                color = 'gray'
                )
            ),
        xaxis = dict(
            tickfont = dict(
                size = 14 ,
                family = 'Arial',
                color = 'black',
            ),
            gridcolor = 'lightgray'
            ),
        yaxis = dict(
            tickfont = dict(
                size = 14 ,
                family = 'Arial',
                color = 'black',
            ),
            gridcolor = 'lightgray'
            ),
        font = dict(
            family = 'Arial',
            size = 14,
            color = 'black'
            ),
        legend = dict(
            orientation ='h', # Legenda Horizontal
            yanchor = 'bottom', # Alinhamento vertical da legenda
            y = 1.05, # Posição da legenda um pouco acima do gráfico
            xanchor = 'center', # Alinhamento horizontal da legenda
            x = 0.5, # Posição horizontal da legenda
            bgcolor = 'rgba(0,0,0,0)', # Cor de fundo da legenda
            borderwidth = 0, # Largura da borda da legenda
            ),
        margin = dict(
            l =  60,
            r = 60,
            t = 120,
            b = 60
            ), 
        plot_bgcolor = '#f8f9fa', # Cor de fundo do Gráfico
        paper_bgcolor = 'white' # Cor de fundo da Área do Gráfico
        
    )
    
    # Gera o HTML do gráfico sem o código javascript necessário para o gráfico funcionar (inclusão externa)
    graph_html = fig.to_html(full_html=False, include_plotlyjs = 'cdn')
       
    return render_template_string(paginas.pgCorrel, grafico = graph_html)


@app.route(rot[7])

def graf3D():
    
    with sqlite3.connect(caminhoBd) as conn:
        inad_df = pd.read_sql_query(" SELECT * FROM inadimplencia", conn)
        selic_df = pd.read_sql_query(" SELECT * FROM selic", conn)
        
    # Mescla os dois Dataframes com base na coluna de mês ordenando do mais antigo para o mais novo
    merged = pd.merge(inad_df, selic_df, on='mes').sort_values('mes')
    
    
    merged['mes_idx'] = range(len(merged))
    
    # Cálculo da diferença de inadimplência em relação ao mês anterior (Primeira derivada discreta)
    # Função fillna -> Substitui/Preenche valores NaN em uma séire ou coluna por 0
    merged['tend_inad'] = merged['inadimplencia'].diff().fillna(0)
    
    # Classificar a tendência como subiu ou caiu ou estabilizou com base na variação calculada
    trend_color = ['subiu' if x > 0 else 'caiu' if x < 0 else 'estavel' for x in merged['tend_inad']]
    
    # Cálculo das variações mensais (derivadas discretas) da inadimplência e da selic
    merged['var_inad'] = merged['inadimplencia'].diff().fillna(0)
    merged['var_selic'] = merged['selic_diaria'].diff().fillna(0)
    
    # Seleciona as colunas numéricas que serão usadas para agrupar os meses por similaridade
    features = merged[['selic_diaria','inadimplencia']].copy()
    scaler = StandardScaler() # Normaliza para padronizar as variáveis (média = 0; Desvio Padrão = 1)
    
    scaler_features = scaler.fit_transform(features) # Aplica a normalização
    
    # Executa o algoritmo do KMeans com 3 clusters (grupos) distimtos. Isso vai rotular cada mês com um número de cluster, agrupando meses similares
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    merged['cluster'] = kmeans.fit_predict(scaler_features) # Adiciona as colunas com os clusters selecionados
    
    # Prepara os dados de entrada para o cálculo de uma regressão linear múltipla, a ideia é encontrar um plno que melhor se ajusta aos pontos 3D do gráfico
    
    x = merged[['mes_idx','selic_diaria']].values # Matriz de entrada: Tempo e selic
    
    y = merged['inadimplencia'].values # Vetor de saída
    
    # Concatena uma coluna para permitir o cálculo independente
    a = np.c_[x, np.ones(x.shape[0])] # c_ -> Cálculo específco para os termos independentes
    # A função toda aplica o método dos mínimos quadrados para resolver a * coef = y
    # Resultado da função: coef[0] = a; coef[1] = b; coef[2] = c
    coeffs, _, _, _ = np.linalg.lstsq(a, y, rcond=None)
    
    # Criação de uma malha de pontos 2d parar desenhar a superfície do plano de regressão
    
    # 30 pontos entre a menor e o maior mês
    xi = np.linspace(
        merged['mes_idx'].min(),merged['mes_idx'].max(), 30)
    # 30 pontos entre a menor e a maior Taxa Selic
    yi = np.linspace(merged['selic_diaria'].min(),merged['selic_diaria'].max(), 30)
    
    # Gera todas as combinações possíveis entre os valores de xi e yi
    xi, yi = np.meshgrid(xi,yi)
    
    # Aplica à equação do plano para gerar os valo x (Inadimplencia)
    zi = coeffs[0] * xi + coeffs[1] * yi + coeffs[2]
    
    # Criando o gráfico 3D com informações extras ao passar o mouse sobre os pontos
    
    # Caso queira mudar o tema da paleta de cores: https://plotly.com/python/builtin-colorscales/
    disp = go.Scatter3d(
        x = merged['mes_idx'],
        y = merged['selic_diaria'],
        z = merged['inadimplencia'],
        mode = 'markers', # Apenas marcadores de bolinhas
        marker = dict(
            size = 8,
            color = merged['cluster'],
            colorscale = 'Blues',# Tema da paleta de cores padrão
            opacity = 0.9  # Transparencia
        ),
        text = [ # Conteúdo que aparece ao passar o mouse sobre os pontos de dados
           f'''
            Mês: {m}
            Inadimplência: {z:.2f}%
            SELIC: {y:.2f}%
            Variação da Inadimplência: {vi:.2f}%
            Variação SELIC: {vs:.2f}%
            Tendência: {t}
           ''' 
           for m, z, y, vi, vs, t in zip(
               merged['mes'], 
               merged['inadimplencia'],
               merged['selic_diaria'],
               merged['var_inad'],
               merged['var_selic'],
               trend_color
            )
        ],
        hovertemplate='%{text}<extra><extra>'
    )
    
    # Criando a superfície 3D do plano de regressão
    surface =go.Surface(
        # Coordenadas da grade
        x = xi,
        y = yi,
        z = zi,
        showscale = False, # Barra de cores
        colorscale = 'dense', # Paleta de cores para o plano 
        opacity = 0.5,
        name = 'Plano de Regressão'
    )
    
    # Juntando os dois gráficos (pontos de dados e plano de regressão) em uma única visualização 3D
    fig = go.Figure( data = [disp, surface])
    
    # Formatando o Layout da cena completa em 3D
    fig.update_layout(
        scene = dict(
            xaxis = dict(
                title = 'Tempo (Meses)',
                tickvals = merged['mes_idx'],
                ticktext = merged['mes']
            ),
            yaxis = dict(title='SELIC (%)'),
            zaxis = dict(title='Inadimplência (%)')
        ),
        title = 'Insights Econômicos 3D com tendências, derivadas e clusters',
        margin = dict(l=0, r=0, t=50, b=0) ,
        height = 800
   )
    
    graph3d_html = fig.to_html(full_html = False, include_plotlyjs='cdn')
   
    
    return render_template_string(paginas.pgGraf3D, grafico3d = graph3d_html) 

    
if __name__ == '__main__':
    init_db()
    app.run(
        debug= config.FLASK_DEBUG,
        host= config.FLASK_HOST,
        port= config.FLASK_PORT  
            )
    
