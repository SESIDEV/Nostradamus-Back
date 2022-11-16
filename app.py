from flask import Flask, request
import json, nltk
from flask import make_response
from flask_cors import CORS
from files.conector import retornarRequest, salvarRequest, retornarPesquisa
from time import time as tick
from files.looping import rodarPesquisasContinuas
import threading

nltk.download('stopwords')
nltk.download('punkt')
def print_json(arg):
    response = make_response(json.dumps(arg, sort_keys=True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response

app = Flask(__name__)
CORS(app) # MUDAR DEPOIS

@app.route("/")
def index():
    return 'página principal'


@app.route("/search") # definir parametros a serem recebdios pela rota
def busca():
    termo_busca = request.args.get('busca')
    lista_bases = list()
    dict_bases = dict()
    busca_rapida = 0
    if request.args.get('springerlink'):
        lista_bases.append("SL")
    if request.args.get('sciencedirect'):
         lista_bases.append("SD")   
    if request.args.get('busca-rapida'):
        busca_rapida = 1

    dict_bases['bases']=lista_bases
    bases = json.dumps(dict_bases)
    
    token = str(tick())[11:]
    
    salvarRequest(token, termo_busca, busca_rapida, bases)

    return json.dumps({'token': token})


@app.route("/result")
def resultado():
    return "resultado ?"


@app.route("/consulta")
def consulta():
    token = request.args.get('token')
    tupla = retornarRequest(token) # REQUEST DE PESQUISA
    print(f'Tupla retornada: {tupla}')
    if tupla[3] == 0: # SE A PESQUISA AINDA NÃO FOI FEITA
        return {"resposta":"not ready"}
    elif tupla[2] == 1: # SE A PESQUISA NÃO ESTÁ SENDO FEITA
        return {"resposta":"ongoing"}
    else:
        return retornarPesquisa(token)


if __name__ == "__main__":
    threading.Thread(target=rodarPesquisasContinuas).start()
    app.run(debug=True)
