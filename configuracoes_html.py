pInit = '''
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