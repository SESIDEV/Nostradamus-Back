import mysql.connector as mydb

#STRINGS SQL:
set_in_process = "UPDATE requests SET inProcess = 1 WHERE id = %s"
set_done = "UPDATE requests SET inProcess = 0, done = 1 WHERE id = %s"
add_request = "INSERT INTO requests (id, input, inProcess, done, fastSearch, selectedBases) VALUES (%s, %s, %s, %s, %s, %s)"
add_research = "INSERT INTO pesquisas (id, json) VALUES (%s, %s)"
lookup_reserach = "SELECT json FROM pesquisas WHERE id = %s"
lookup_request = "SELECT * FROM requests WHERE id = %s"
get_pending = "SELECT id FROM requests WHERE done = 0 AND inProcess = 0"
get_full_request = "SELECT input, fastSearch, selectedBases FROM requests WHERE id = %s"

def retornarDB():
    print("\nConectando ao banco...")
    db = mydb.connect(host="containers-us-west-110.railway.app", port="7717", user="root",password="LyTaKtOjN58WLwYREa5Z",database="railway")
    #db = mydb.connect(host="localhost",user="root",password="admin",database="railway")
    print("Conectado.\n")
    return db

def prepararParaPesquisa(token): #   ESTÁGIO 2 (RETORNA DADOS NECESSÁRIOS PARA EFETUAR A BUSCA COMPLETA)
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token,)
    cursor.execute(set_in_process, parametros) # ALTERA O STATUS DO REQUEST PARA 'EM PROCESSO'
    db.commit()
    cursor.execute(get_full_request, parametros) # BUSCA OS DADOS DO REQUEST
    
    for x in cursor:
        valor = x

    return valor

def incluirNoBanco(token, json): #   ESTÁGIO 3
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token, json)
    cursor.execute(add_research, parametros) # ADICIONA A BUSCA COMPLETA NA TABELA DE PESQUISAS
    print('\nPesquisa adicionada com sucesso.')
    parametros2 = (token,)
    cursor.execute(set_done, parametros2) # ALTERA O STATUS DO REQUEST PARA CONCLUÍDO
    db.commit()
    print('Status alterado para concluído.\n')

def salvarRequisicao(token, termo_busca, busca_rapida, bases): #   ESTÁGIO 0
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token, termo_busca, 0, 0, busca_rapida, bases)
    cursor.execute(add_request, parametros) # REGISTRA O REQUEST NA TABELA DE REQUESTS PENDENTES
    db.commit()

def retornarRequisicao(token):
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token,)
    valor = ''
    cursor.execute(lookup_request, parametros) # RETORNA UM REQUEST ESPECÍFICO

    for x in cursor:
        valor = x

    return valor

def retornarPesquisa(token):
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token,)
    valor = ''
    cursor.execute(lookup_reserach, parametros) # RETORNA UMA PESQUISA PRONTA NA TABELA DE PESQUISAS

    for x in cursor:
        valor = x[0]

    return valor

def buscarPesquisasPendentes(): #   ESTÁGIO 1 (EXECUTAR SEMPRE)
    db = retornarDB()
    cursor = db.cursor()
    valor = ''
    cursor.execute(get_pending) # BUSCA POR REQUESTS PENDENTES

    for x in cursor:
        valor = x[0]
        break

    return valor