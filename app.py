from flask import Flask, request
import json, nltk
from flask import make_response
from flask_cors import CORS
from files.conector import retornarStatusRequisicao, salvarRequisicao, retornarPesquisa
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
# 127.0.0.1 se refere ao uso e teste local
CORS(app, origins=['http://127.0.0.1:5001','https://nostradamus.up.railway.app/'])

@app.route("/")
def index():
    return 'página principal'


@app.route("/search")
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
    
    salvarRequisicao(token, termo_busca, busca_rapida, bases)

    return json.dumps({'token': token})


@app.route("/result")
def resultado():
    return "resultado ?"

@app.route("/consulta")
def consulta():
    verdadeiro = 1
    falso = 0
    token = request.args.get('token')
    tupla = retornarStatusRequisicao(token) # RETORNA BOOLEANS (inProcess, done)
    
    if len(tupla) != 2:
        return {"resposta": 404} # NÃO FOI FEITA NENHUMA BUSCA COM ESTE TOKEN
    elif tupla[1] == falso: 
        return {"resposta": 422} # A PESQUISA AINDA NÃO FOI FEITA
    elif tupla[0] == verdadeiro: 
        return {"resposta": 102} # A PESQUISA ESTÁ SENDO FEITA
    else:
        return retornarPesquisa(token)

threading.Thread(target=rodarPesquisasContinuas).start()

if __name__ == "__main__":
    app.run(debug=False)
