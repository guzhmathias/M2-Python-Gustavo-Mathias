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

def interpretador(codigo):
    # Quebra o código em linhas
    linhas = codigo.split('\n')
    
    # Um dicionário para armazenar as variáveis
    variaveis = {}
    
    for linha in linhas:
        linha = linha.strip() # Remove espaços desnecessários
        
        # Se for uma linha de definir -> Funções
        if linha.startswith("definir"): 
            partes = linha[7:].strip().split(" como ") # Pega o nome da variável e o valor
            nome = partes[0].strip()
            valor = partes[1].strip().strip('"') # Remove as aspas duplas
            variaveis[nome] = valor # Armazenando a variável
        
        # Se for uma linha de mostrar -> Print
        elif linha.startswith("mostrar"):
            conteudo = linha[7:].strip().strip('"')
            print(conteudo)
        
            
        # Se for uma estrutura condicional (se) -> If
        elif linha.startswith("se"):
            condicao = linha[3:].split(" então ")[0].strip()
            comando = linha.split(" então ")[1].strip()
            
            # Aqui podemos apenas checar se a condição é verdadeira ou falsa
            if condicao == "verdadeiro":
                interpretador(comando) #executa o comando dentro da condição
            
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
    

codigo = """
    definir nome como "lalala"
    mostrar "O nome é" + nome
    se verdadeiro então mostrar "Isso é verdadeiro"
    enquanto verdadeiro faça mostrar "Dentro do laço"
    """

interpretador(codigo)