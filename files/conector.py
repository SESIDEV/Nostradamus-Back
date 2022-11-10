import mysql.connector as mydb
from time import time as tick

def retornarCursor():
    db = mydb.connect(host="containers-us-west-110.railway.app",user="root",password="LyTaKtOjN58WLwYREa5Z",database="railway")
    return db

def incluirNoBanco(json):
    token = str(tick())[11:]

    db = retornarCursor()
    string_sql = "INSERT INTO pesquisas (id, json) VALUES (%s, %s)"
    valores = (token, json)
    db.execute(string_sql, valores)
    db.commit()
    print(db.rowcount, "record inserted.")