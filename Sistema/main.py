# Mapa interativo de custos (NY x RJ) com pontos e mapa de calor

# Bibliotecas utilizadas
import pandas as pd, numpy as np, plotly.graph_objs as go

# Utilidades de padronização

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:

    # Função para padronizar as colunas ao tentar detectar automaticamente as colunas latitude e longitude, custos e nome
    # Aceita vários nomes comuns como lat/latitude custo, valor e etc.
    # Preenche custos ausentes com a mediana (ou se tudo tiver ausente)
    
    df = df.copy()
    
    lat_candidates = ['lat', 'latitude', 'Latitude', 'LAT', 'Lat', 'LATITUDE']
    lon_candidates = ['lon','longitude', 'Longitude', 'LON', 'Lon', 'LONGITUDE','Lng']
    cost_candidates = ['custo','valor','cost','preço','preco','valor_total','price']
    name_candidates = ['nome','name','descricao','titulo','title','local','place']
    
    def pick(colnames, candidates):
        # Colnames -> Nomes das colunas da tabela
        # Candidates -> Possíveis nomes a serem encontrados
        for c in candidates:
            # Percorre cada candidato (c) dentro da lista de candidatos
            if c in colnames:
                # Se o candidato for exatamente igual a um dos nomes em colnames ...
                return c
                # Retorna esse candidato imediatamente
        for c in candidates:
            # Se não encontro a correspondência exata
            # Percorre novamente cada candidato
            for col in colnames:
                # Aqui percorre cada nome de coluna
                if c.lower() in col.lower():
                    # Faz igual o de cima, mas trabalhando em minúsculos apenas
                    return col
        return None 
        # Se não encontrou nada nem exato nem parcialmente, retorna None (nenhum match encontrado)
        
    lat_col = pick(df.columns, lat_candidates)
    lon_col = pick(df.columns, lon_candidates)
    cost_col = pick(df.columns, cost_candidates)
    name_col = pick(df.columns, name_candidates)
    
    if lat_col is None or lon_col is None:
        raise ValueError (f"Não foram encontradas colunas de latitude e longitude {list(df.columns)}")
    
    out = pd.DataFrame()
    out['lat'] = pd.to_numeric(df[lat_col], errors='coerce')
    out['lon'] = pd.to_numeric(df[lon_col], errors='coerce')
    out['custo'] = pd.to_numeric(df[cost_col], errors='coerce') if cost_col is not None else np.nan
    out['nome'] = df[name_col].astype(str) if name_col is not None else [f"Ponto {i} " for i in range(len(df))]
    
    # Removendo linhas sem coordenadas (inúteis para o exercício pois sem coordenas simplesmente não aparecem)
    
    out = out.dropna(subset = ['lat','lon']).reset_index(drop=True)
    
    # Preenche o custo ausente
    if out['custo'].notna().any():
        med = float(out['custo'].median()) # Calcula a mediana dos custos
        if not np.isfinite(med):
            med = 1.0
        out['custo'] = out['custo'].fillna(med)
    else:
        out['custo'] = 1.0
    return out

def city_center(df: pd.DataFrame) -> dict:

    # Define a função city_center
    # - Recebe como parâmetro um dataframe pandas (Df)
    # - Deve retornar um dicionário (-> Dict)]
    
    return dict(
        # Calcula a média da coluna 
        lat = float(df['lat'].mean()),
        lon = float(df['lon'].mean())
    )
    
# ------------------------ Traces ------------------------

def make_point_trace(df:pd.DataFrame, name:str) -> go.Scattermapbox:
    hover = ("<b>%{customdata[0]}</b><br>"
             "Custo: %{customdata[1]}<br>"
             "Lat: %{lat:.5f}<br>Lon: %{lon:.5f}")
    # Definir o tamanho dos marcadores (normalizar pelo custo)
    c = df["custo"].astype(float).values
    c_min, c_max = float(np.min(c)), float(np.max(c))
    if not np.isfinite(c_min) or not np.isfinite(c_max) or abs(c_max - c_min) < 1e-9:
        size = np.full_like(c, 10.0, dtype=float)
    else:
    # Caso Normal: Normaliza os custos para o intervalo [0,1] e escala para variar entre 6 e 26 (20 de amplitude mais deslocamento de 6)
    # Pontos de custo baixo ~6, Pontos de custo alto ~26
        size = (c - c_min) / (c_max - c) * 20 + 6
    # Mesmo que os dados estejam fora da faixa de 6 a 26 ele evita sua apresentação, forçando a ficar entre o intervalo
    sizes = np.clip(size, 6, 26)
    
    # Stack: gera uma array com duas dimensões
    # Axis=1 -> Empilha as colunas lado a lado
    custom = np.stack([df['nome'].values, df['custo'].values], axis=1)
    
    return go.scattermapbox(
        lat = df['lat'],
        lon = df['lon'],
        mode = 'markers',
        marker = dict(
            size = sizes,
            color = df['custo'],
            colorscale = "Blues",
            colorbar = dict(title ='Custo'), 
            ),
        name = f"{name} • Pontos",
        hovertemplate = hover,
        customdata = custom
    )
        
        
# Definir a densidade dos traços
def make_density_trace(df: pd.DataFrame, name:str) -> go.Densitymapbox:
    return go.Densitymapbox(
        lat = df['lat'],
        lon = df['lon'],
        z = df['Custo'],
        radius = 20, 
        colorscale = "PuBu",
        name = f"{name} • Pontos",
        showscale= True,
        colorbar = dict(title='Custo'),
    )

# --------------------------------- MAIN ---------------------------------
def main():
    # Carregar e padronizar os dados!
    folder = "C:/Users/integral/Desktop/M2 Python Gustavo/Sistema/"
    ny = standardize_columns(pd.read_csv(f'{folder}listingsNY.csv'))
    rj = standardize_columns(pd.read_csv(f'{folder}listingsRJ.csv'))
    
    # cria os quatro traces(NY pontos / NY calor/ RJ pontos / RJ calor)
    ny_point = make_point_trace(ny, "Nova York")
    ny_heat = make_density_trace(ny, "Nova York")
    rj_point = make_point_trace(rj, "Rio de Janeiro")
    rj_heat = make_density_trace(rj, "Rio de Janeiro")
    
    fig = go.Figure([ny_point, ny_heat, rj_point, rj_heat])
    
    def center_zoom(df, zoom):
        return dict(center=city_center(df), zoom=zoom)
    
    # Dropdown simples com quatro opções (cidade • visualização)
    buttons = [
        dict(
            label = "Nova York • Pontos",
            method = "update",
            args = [
                {"visible":[True, False, False, False]},
                {"mapbox": center_zoom(ny, 9)}
            ]
        ),
        dict(
            label = "Nova York • Calor",
            method = "update",
            args = [
                {"visible":[False, True, False, False]},
                {"mapbox": center_zoom(ny, 9)}
            ]
        ),
        dict(
            label = "Rio de Janeiro • Pontos",
            method = "update",
            args = [
                {"visible":[False, False, True, False]},
                {"mapbox": center_zoom(rj, 10)}
            ]
        ),
        dict(
            label = "Rio de Janeiro • Calor",
            method = "update",
            args = [
                {"visible":[False, False, False, True]},
                {"mapbox": center_zoom(rj, 10)}
            ]
        )
    ]
    
    fig.update_layout(
        title = "🌐 Mapa Interativo de Custos 💵 • Pontos e Mapa de Calor",
        mapboxstyle = 'open-street-map',
        mapbox = dict(center=city_center(rj), zoom=10),
        margin = dict(l=10, r=10, t=50, b=10),
        updatemenus = [dict(
            buttons = buttons,
            direction = "down",
            x = 0.01,
            y = 0.99,
            xanchor = "left",
            yanchor = "top",
            bg_color = "white",
            bordercolor = "lightgray"
        )],
        legend = dict(
               orientation = "h",
               yanchor = "bottom",
               xanchor = "right",
               y = 0.01,
               x = 0.99
        )
        
    )

    # Salva HTML de apresentação
    fig.write_html(f"{folder}mapa_custos_interativos.html", include_plotlyjs = "cdn", full_html = True)

    print(f"Arquivo gerado com sucesso em: {folder}mapa_custos_interativos.html")
if __name__ == '__main__':
    main()