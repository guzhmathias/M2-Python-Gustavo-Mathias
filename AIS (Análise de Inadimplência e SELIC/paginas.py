
pgInicial = ('''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Upload de Dados Econômicos</title>
    <style>
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e9f7ef, #f5f9ff);
            color: #2c3e50;
            margin: 0;
            padding: 0;
        }

        h1 {
            text-align: center;
            color: #145a32; /* verde escuro (finanças) */
            margin-top: 30px;
        }

        form {
            max-width: 600px;
            margin: 30px auto;
            padding: 25px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        label {
            display: block;
            font-weight: bold;
            margin: 15px 0 8px;
            color: #1c2833;
        }

        input[type="file"] {
            width: 100%;
            padding: 10px;
            border: 2px dashed #27ae60;
            border-radius: 8px;
            cursor: pointer;
            background-color: #f9f9f9;
        }

        input[type="submit"] {
            display: block;
            width: 100%;
            margin-top: 20px;
            padding: 12px;
            background: #27ae60;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }

        input[type="submit"]:hover {
            background: #219150;
        }

        hr {
            margin: 40px auto;
            width: 80%;
            border: none;
            border-top: 2px solid #d5dbdb;
        }

        .links {
            text-align: center;
            margin: 20px 0;
        }

        .links a {
            display: inline-block;
            margin: 10px 15px;
            padding: 12px 18px;
            background: #2980b9;
            color: white;
            text-decoration: none;
            font-weight: 500;
            border-radius: 8px;
            transition: 0.3s;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }

        .links a:hover {
            background: #1f618d;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>

    <h1>Upload de Dados Econômicos</h1>  

    <form action="/upload" method="POST" enctype="multipart/form-data">
        <label for="campo_inadimplencia">Arquivo de Inadimplência (CSV)</label>
        <input id="campo_inadimplencia" name="campo_inadimplencia" type="file" required>

        <label for="campo_selic">Arquivo de Taxa Selic (CSV)</label>
        <input id="campo_selic" name="campo_selic" type="file" required>

        <input type="submit" value="Fazer Upload">
    </form>   

    <hr>

    <div class="links">
        <a href="/consultar">Consultar Dados Armazenados</a>
        <a href="/graficos">Visualizar Gráficos</a>  
        <a href="/editar_inadimplencia">Editar Inadimplência</a>
        <a href="/editar_selic">Editar Taxa Selic</a>  
        <a href="/correlacao">Analisar Correlação</a> 
        <a href="/grafico_3d">Visualização 3D</a>
    </div>

</body>
</html>
       
''')

pgConsulta = ('''
              <html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Consulta de Tabela</title>
    <style>
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e9f7ef, #f5f9ff);
            color: #2c3e50;
            margin: 0;
            padding: 0;
        }

        h1 {
            text-align: center;
            color: #145a32;
            margin-top: 30px;
        }

        form {
            max-width: 500px;
            margin: 30px auto;
            padding: 25px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
        }

        label {
            display: block;
            font-weight: bold;
            margin-bottom: 10px;
            color: #1c2833;
        }

        select {
            width: 80%;
            padding: 10px;
            border: 2px solid #27ae60;
            border-radius: 8px;
            background-color: #f9f9f9;
            font-size: 15px;
            margin-bottom: 20px;
            cursor: pointer;
        }

        select:focus {
            outline: none;
            border-color: #219150;
            background: #ecfdf5;
        }

        input[type="submit"] {
            display: block;
            width: 80%;
            margin: 0 auto;
            padding: 12px;
            background: #27ae60;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }

        input[type="submit"]:hover {
            background: #219150;
        }

        .links {
            text-align: center;
            margin-top: 25px;
        }

        .links a {
            display: inline-block;
            padding: 10px 16px;
            background: #2980b9;
            color: white;
            text-decoration: none;
            font-weight: 500;
            border-radius: 8px;
            transition: 0.3s;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }

        .links a:hover {
            background: #1f618d;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>

    <h1>Consulta de Tabela</h1>

    <form method="POST">
        <label for="campo_tabela">Escolha uma Tabela</label>
        <select id="campo_tabela" name="campo_tabela" required>
            <option value="inadimplencia">Inadimplência</option>
            <option value="selic">Taxa Selic</option>
        </select>
        <input type="submit" value="Consultar">
    </form>

    <div class="links">
        <a href="/">Voltar</a>
    </div>

</body>
</html>
              ''')

pgGraficos = ('''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Gráficos Econômicos</title>
    <style>
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e9f7ef, #f5f9ff);
            color: #2c3e50;
            margin: 0;
            padding: 0;
        }

        h1 {
            text-align: center;
            color: #145a32;
            margin: 25px 0;
            font-size: 2.2rem;
            position: relative;
        }

        /* Simulação de marquee com animação */
        .marquee {
            display: inline-block;
            white-space: nowrap;
            overflow: hidden;
            animation: scroll 12s linear infinite;
        }

        @keyframes scroll {
            from { transform: translateX(100%); }
            to { transform: translateX(-100%); }
        }

        .container {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
            padding: 20px;
        }

        .graph {
            flex: 1;
            min-width: 400px;
            max-width: 48%;
            background: white;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .links {
            text-align: center;
            margin: 20px 0;
        }

        .links a {
            display: inline-block;
            padding: 10px 16px;
            background: #2980b9;
            color: white;
            text-decoration: none;
            font-weight: 500;
            border-radius: 8px;
            transition: 0.3s;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }

        .links a:hover {
            background: #1f618d;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <h1>
        <span class="marquee">📈 Gráficos Econômicos 📊</span>
    </h1>

    <div class="container">
        <div class="graph">{{ reserva01|safe }}</div>
        <div class="graph">{{ reserva02|safe }}</div>
    </div>

    <div class="links">
        <a href="/">Voltar</a>
    </div>
</body>
</html>

              ''')

pgEditarInad = ('''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Editar Inadimplência</title>
    <style>
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e9f7ef, #f5f9ff);
            color: #2c3e50;
            margin: 0;
            padding: 0;
        }

        h1 {
            text-align: center;
            color: #145a32;
            margin-top: 30px;
        }

        form {
            max-width: 500px;
            margin: 30px auto;
            padding: 25px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        label {
            display: block;
            font-weight: bold;
            margin: 15px 0 8px;
            color: #1c2833;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #27ae60;
            border-radius: 8px;
            background-color: #f9f9f9;
            font-size: 15px;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #219150;
            background: #ecfdf5;
        }

        input[type="submit"] {
            display: block;
            width: 100%;
            margin-top: 20px;
            padding: 12px;
            background: #27ae60;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }

        input[type="submit"]:hover {
            background: #219150;
        }

        .links {
            text-align: center;
            margin-top: 25px;
        }

        .links a {
            display: inline-block;
            padding: 10px 16px;
            background: #2980b9;
            color: white;
            text-decoration: none;
            font-weight: 500;
            border-radius: 8px;
            transition: 0.3s;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }

        .links a:hover {
            background: #1f618d;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>

    <h1>Editar Inadimplência</h1>

    <form method="POST" action="/editar_inadimplencia">
        <label for="campo_mes">Mês (AAAA-MM)</label>
        <input type="text" id="campo_mes" name="campo_mes" placeholder="2025-01" required>

        <label for="campo_valor">Novo valor de Inadimplência</label>
        <input type="text" id="campo_valor" name="campo_valor" required>

        <input type="submit" value="Atualizar Dados">
    </form>

    <div class="links">
        <a href="/">Voltar</a>
    </div>

</body>
</html>

              ''')

pgEditarSelic = ('''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Editar Taxa Selic</title>
    <style>
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e9f7ef, #f5f9ff);
            color: #2c3e50;
            margin: 0;
            padding: 0;
        }

        h1 {
            text-align: center;
            color: #145a32;
            margin-top: 30px;
        }

        form {
            max-width: 500px;
            margin: 30px auto;
            padding: 25px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        label {
            display: block;
            font-weight: bold;
            margin: 15px 0 8px;
            color: #1c2833;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #27ae60;
            border-radius: 8px;
            background-color: #f9f9f9;
            font-size: 15px;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #219150;
            background: #ecfdf5;
        }

        input[type="submit"] {
            display: block;
            width: 100%;
            margin-top: 20px;
            padding: 12px;
            background: #27ae60;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.3s;
        }

        input[type="submit"]:hover {
            background: #219150;
        }

        .links {
            text-align: center;
            margin-top: 25px;
        }

        .links a {
            display: inline-block;
            padding: 10px 16px;
            background: #2980b9;
            color: white;
            text-decoration: none;
            font-weight: 500;
            border-radius: 8px;
            transition: 0.3s;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }

        .links a:hover {
            background: #1f618d;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>

    <h1>Editar Taxa Selic</h1>

    <form method="POST" action="/editar_selic">
        <label for="campo_mes">Mês (AAAA-MM)</label>
        <input type="text" id="campo_mes" name="campo_mes" placeholder="2025-01" required>

        <label for="campo_valor">Novo valor da Taxa Selic</label>
        <input type="text" id="campo_valor" name="campo_valor" required>

        <input type="submit" value="Atualizar Dados">
    </form>

    <div class="links">
        <a href="/">Voltar</a>
    </div>

</body>
</html>
              ''')

pgCorrel = ('''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Correlação Selic vs Inadimplência</title>
    <style>
        body {
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e9f7ef, #f5f9ff);
            color: #2c3e50;
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 900px;
            margin: 40px auto;
            padding: 25px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
        }

        h1 {
            color: #145a32;
            margin-bottom: 25px;
        }

        .graph {
            padding: 15px;
            border-radius: 10px;
            background: #f9f9f9;
            box-shadow: inset 0 2px 6px rgba(0,0,0,0.05);
        }

        .links {
            margin-top: 30px;
        }

        .links a {
            display: inline-block;
            padding: 10px 16px;
            background: #2980b9;
            color: white;
            text-decoration: none;
            font-weight: 500;
            border-radius: 8px;
            transition: 0.3s;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }

        .links a:hover {
            background: #1f618d;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Correlação entre Selic e Inadimplência</h1>
        <div class="graph">{{ grafico|safe }}</div>
        
        <div class="links">
            <a href="/">Voltar</a>
        </div>
    </div>
</body>
</html>
              ''')

pgGraf3D = ('''
            
            ''')