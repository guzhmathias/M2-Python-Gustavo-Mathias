#   ___                   _       _        
#  / _ \ _   _  __ _ _ __| |_ ___| |_ ___  
# | | | | | | |/ _` | '__| __/ _ \ __/ _ \ 
# | |_| | |_| | (_| | |  | ||  __/ || (_) |
#  \__\_\\__,_|\__,_|_|   \__\___|\__\___/ 

'''

Linguagem : Quarteto
Autor : Gustavo Mathias
Versão : 0.0.1 Alpha
Data: 28/08/2025

'''

def interpretador(codigo, variaveis=None):
    # Quebra o código em linhas
    
    # Um dicionário para armazenar as variáveis
    if variaveis is None:
        variaveis = {}
             
    def eval_texto(expr):
        partes = [p.strip() for p in expr.split("+")] 
        out = ""
        for p in partes:
            if len(p) >= 2 and p[0] == '"':
                out += p[1:-1] # Trecho entre as aspas
            else:
                out += str(variaveis.get(p,p)) # Variável (literal se não existir)
        return out
        
    linhas = codigo.split('\n')
    for linha in linhas:
        linha = linha.strip() # Remove espaços desnecessários
        
        if not linha: # Ignora linhas vazias
            continue
    
        # Se for uma linha de definir -> Funções
        if linha.startswith("definir"): 
            resto = linha[7:].strip()
            if " como " not in resto:
                print(f"Erro de sintaxe no código inserido: {linha}")
                continue
            nome, valor = resto.split(" como ", 1)
            nome = nome.strip()
            valor = valor.strip()
            if len(valor) >= 2 and valor[0] == '"' and valor[1] == '"':
                valor = valor[1:-1]
            variaveis[nome] = valor
                
        
        # Se for uma linha de mostrar -> Print
        elif linha.startswith("mostrar"):
            conteudo = linha[7:].strip()
            print(eval_texto(conteudo))
        
            
        # Se for uma estrutura condicional (se) -> If
        elif linha.startswith("se"):
            resto = linha[3:].strip()
            if " então " not in resto:
                print(f"Erro de sintaxe no código inserido: {linha}")
                continue
            condicao, comando = resto.split(" então ", 1)
            
                        # Aqui podemos apenas checar se a condição é verdadeira ou falsa
            if condicao.strip() == "verdadeiro":
                interpretador(comando.strip(), variaveis) # Executa o comando dentro da condição
            
        # Se for um laço "enquanto" ->  While
        elif linha.startswith("enquanto"):
            condicao = linha[8:].split(" faça ")[0].strip()
            comando = linha.split(" faça ")[1].strip()
            
            # Verifica a condição do looping (por enquanto, consideramos verdadeiro ou falso)
            while condicao == "verdadeiro":
                interpretador(comando) # Executa o camndo dentro do loop
                break # Evita loops infinitos para esse exemplo
        
        else:
            print(f"Comando não foi reconhecido{linha}")
    


codigo_base = '''

    definir nome como "lalala"
    mostrar "O nome é " + nome
    se verdadeiro então mostrar "Isso é verdadeiro"
    enquanto verdadeiro faça mostrar "Dentro do laço"
    
    '''
decisao = input(f"O que você prefere? \n[1] Usar o código base  \n[2] Incluir sua própria versão? \nCódigo base:\n{codigo_base}")

if decisao == "1":
    interpretador(codigo_base)
    
elif decisao == "2":
    
    '''
    Correção do instrutor Caio:
    
    linha = []
    while True:
        linha = input(f"Insira a linha do código, ou pressiona Enter vazio para terminar \n")
        if not linha or linha.strip().upper() == "FIM":
            break
        linhas.append(linha)
        
    codigo_usuario = "\n".join(linhas)
    interpretador(codigo_usuario)
    '''
    
    # Minha versão:
    variaveis = {}
    i = int(input("Quantos códigos você deseja inserir? \n"))
    for cont in range (i):
        coman = input(f"Insira o {cont + 1}º comando \n")
        interpretador(coman, variaveis)
    
else:
    print("Insira um comando válido!")