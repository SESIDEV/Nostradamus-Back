import os, mysql.connector as mydb

#STRINGS SQL:
pw = os.environ.get('nostradamus_pass')
host1 = os.environ.get('nostradamus_host1')
port1 = os.environ.get('nostradamus_port1')
scheme = os.environ.get('nostradamus_scheme')
set_in_process = "UPDATE requests SET inProcess = 1 WHERE id = %s"
set_done = "UPDATE requests SET inProcess = 0, done = 1 WHERE id = %s"
add_request = "INSERT INTO requests (id, input, inProcess, done, fastSearch, selectedBases) VALUES (%s, %s, %s, %s, %s, %s)"
add_research = "INSERT INTO pesquisas (id, json) VALUES (%s, %s)"
lookup_reserach = "SELECT json FROM pesquisas WHERE id = %s"
lookup_request_status = "SELECT inProcess, done FROM requests WHERE id = %s"
get_pending = "SELECT id FROM requests WHERE done = 0 AND inProcess = 0"
get_full_request = "SELECT input, fastSearch, selectedBases FROM requests WHERE id = %s"

def retornarDB():
    """
    Função para conectar no banco de dados.
    Pode ser (e será) chamada várias vezes ao longo do código,
    pois a conexão sempre se encerra ao fim de cada consulta.

    Retorno:
    Retorna um objeto MySQLConnection.
    """
    print("\nConectando ao banco...")
    if os.environ.get('nostradamus_db_valid1') == os.environ.get('nostradamus_db_valid2'):
        db = mydb.connect(host="localhost",user="root",password="admin",database=scheme)
    else:
        db = mydb.connect(host=host1, port=port1, user="root",password=pw,database=scheme)
    print("Conectado.\n")
    return db

def salvarRequisicao(token, termo_busca, busca_rapida, bases):
    """
    Função para salvar uma requisição de busca.
    Considerando que mais de uma busca podem ser feitas ao mesmo tempo (por usuários diferentes),
    esta função armazena o termo buscado e devolve um token para identificar este mesmo termo futuramente,
    quando a pesquisa completa for feita.
    
    Parâmetros:
    token - número de identificação do request e também da pesquisa posteriormente
    termo_busca - termo buscado pelo usuário
    busca_rapida - boolean para saber se a pesquisa será limitada ou não
    bases - lista com as bases de dados escolhidas pelo usuário
    """
    print('Usuário adicionou busca de Pesquisa')
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token, termo_busca, 0, 0, busca_rapida, bases)
    cursor.execute(add_request, parametros)
    db.commit()

def buscarPesquisasPendentes(): # EXECUTAR A CADA 60 SEGUNDOS
    """
    Função para procurar requisições pendentes. Ao ser adicionada, a requisição possui 2 status:
    "Em processo" e "Feita".
    Esta função busca qualquer requisição que esteja com estes dois valores marcados como 'Falso'.

    Retorno:
    Retorna apenas o id da requisição. Caso não haja nenhuma pendente, esta função retorna uma string vazia.
    """
    db = retornarDB()
    cursor = db.cursor()
    id = ''
    cursor.execute(get_pending)

    for retorno in cursor:
        id = retorno[0]
        break

    return id

def prepararParaPesquisa(token):
    """
    Função para alterar o status 'em Processo' de falso para verdadeiro e retornar os dados da requisição.
    
    Parâmetros:
    token - Número de identificação do request e também da pesquisa posteriormente.
    
    Retorno:
    input - Termo buscado.
    fastSearch - Boolean para saber se a pesquisa será limitada ou não.
    selectedBases - Lista com as bases de dados escolhidas.
    """
    print('Buscando dados do Request para realizar a Pesquisa...')
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token,)
    cursor.execute(set_in_process, parametros)
    db.commit()
    cursor.execute(get_full_request, parametros)
    
    for x in cursor:
        valor = x

    return valor

def incluirNoBanco(token, json):
    """
    Função para adicionar o resultado da busca no banco de dados.
    
    Parâmetros:
    token - Número de identificação da pesquisa e também do request anteriormente.
    json - Resultado completo da pesquisa feita nos bancos selecionados.
    """
    print('Pesquisa sendo adicionada ao banco...')
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token, json)
    cursor.execute(add_research, parametros) # ADICIONA A BUSCA COMPLETA NA TABELA DE PESQUISAS
    print('\nPesquisa adicionada com sucesso.')
    parametros2 = (token,)
    cursor.execute(set_done, parametros2) # ALTERA O STATUS DO REQUEST PARA CONCLUÍDO
    db.commit()
    print('Status alterado para concluído.\n')



def retornarStatusRequisicao(token):
    """
    Função para retornar o status de uma requisição feita ao sistema, a partir do número de identificação.
    
    Parâmetros:
    token - Número de identificação do request e da pesquisa.

    Retorno:
    inProcess - Boolean indicando se o request está sendo atendido.
    done - Boolean indicando se o request já foi atendido.
    """
    print('Usuário iniciou busca de Requisição')
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token,)
    valor = ''
    cursor.execute(lookup_request_status, parametros)

    for x in cursor:
        valor = x

    return valor

def retornarPesquisa(token):
    """
    Função para retornar uma pesquisa pronta, a partir do número de identificação.
    
    Parâmetros:
    token - Número de identificação do request e da pesquisa.

    Retorno:
    json - Resultado completo da pesquisa feita nos bancos selecionados.
    """
    print('Usuário iniciou busca de Pesquisa')
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token,)
    valor = ''
    cursor.execute(lookup_reserach, parametros)

    for x in cursor:
        valor = x[0]

    return valor