import mysql.connector as mydb

#STRINGS SQL:
set_in_progress = "UPDATE requests SET inProgress = 1 WHERE id = %s"
set_done = "UPDATE requests SET inProgress = 0 AND done = 1 WHERE input = %s"
add_request = "INSERT INTO requests (id, input, inProcess, done, fastSearch, selectedBases) VALUES (%s, %s, %s, %s, %s, %s)"
add_research = "INSERT INTO pesquisas (id, json) VALUES (%s, %s)"
lookup_reserach = "SELECT json FROM pesquisas WHERE id = %s"
get_pending = "SELECT id FROM requests WHERE done = 0 AND inProcess = 0"
get_full_request = "SELECT input, fastSearch, selectedBases FROM requests WHERE id = %s"

def retornarDB():
    print("Conectando ao banco...")
    db = mydb.connect(host="containers-us-west-110.railway.app", port="7717", user="root",password="LyTaKtOjN58WLwYREa5Z",database="railway")
    #db = mydb.connect(host="localhost",user="root",password="admin",database="railway")
    print("Conectado.")
    return db

def prepararParaPesquisa(token): #   ESTÁGIO 2 (RETORNA DADOS NECESSÁRIOS PARA EFETUAR A BUSCA COMPLETA)
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token,)
    cursor.execute(set_in_progress, parametros)
    db.commit()
    cursor.execute(get_full_request, parametros)

def incluirNoBanco(token, json): #   ESTÁGIO 3
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token, json)
    cursor.execute(add_research, parametros)
    parametros2 = (token,)
    cursor.execute(set_done, parametros2)
    db.commit()

def salvarRequest(token, termo_busca, busca_rapida, bases): #   ESTÁGIO 0
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token, termo_busca, busca_rapida, bases)
    cursor.execute(add_request, parametros)
    db.commit()

def retornarPesquisa(token):
    db = retornarDB()
    cursor = db.cursor()
    parametros = (token,)
    valor = ''
    cursor.execute(lookup_reserach, parametros)

    for x in cursor:
        print(x[0])
        valor = x[0]

    return valor

def buscarPesquisasPendentes(): #   ESTÁGIO 1 (EXECUTAR SEMPRE)
    db = retornarDB()
    cursor = db.cursor()
    valor = ''
    cursor.execute(get_pending)

    for x in cursor:
        valor = x[0]


    return valor