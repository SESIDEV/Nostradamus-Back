import mysql.connector as mydb

def retornarDB():
    print("Conectando ao banco...")
    db = mydb.connect(host="containers-us-west-110.railway.app", port="7717", user="root",password="LyTaKtOjN58WLwYREa5Z",database="railway")
    #db = mydb.connect(host="localhost",user="root",password="admin",database="railway")
    print("Conectado.")
    return db

def incluirNoBanco(json, token):
    db = retornarDB()
    cursor = db.cursor()
    string_sql = "INSERT INTO pesquisas (id, json) VALUES (%s, %s)"
    valores = (token, json)
    cursor.execute(string_sql, valores)
    db.commit()
    print(cursor.rowcount, "record inserted.")


def retornarPesquisa(token):
    db = retornarDB()
    cursor = db.cursor()
    string_sql = f"SELECT json FROM pesquisas WHERE id = {token}"
    valor = ''
    cursor.execute(string_sql)

    for x in cursor:
        print(x[0])
        valor = x[0]

    return valor