from flask import Flask, request
from files.busca import efetuarBusca
import json, nltk
from flask import make_response
from flask_cors import CORS
from files.conector import incluirNoBanco, retornarPesquisa

nltk.download('stopwords')

def print_json(arg):
    response = make_response(json.dumps(arg, sort_keys=True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response

app = Flask(__name__)
CORS(app) # MUDAR DEPOIS

@app.route("/")
def index():
    #return render_template("content/index.html")
    return 'página principal'


@app.route("/search", methods=['GET'])
def busca():
    termo_busca = request.args.get('busca')
    lista_bases = list()
    if request.args.get('springerlink'):
        lista_bases.append("springerlink")
    if request.args.get('sciencedirect'):
         lista_bases.append("sciencedirect")   
    if request.args.get('busca-rapida'):
        busca_rapida = True
    else:
        busca_rapida = False
    print(termo_busca)

    #resultado = print_json(efetuarBusca(termo_busca, busca_rapida, lista_bases))
    resultado = efetuarBusca(termo_busca, busca_rapida, lista_bases)
    resultado2 = json.dumps(resultado)
    
    token_retornado = incluirNoBanco(resultado2)

    resposta_formatada = f'''
    
    acho que foi

    se foi mesmo, salva esse token aí: {token_retornado}
    
    '''

    return resposta_formatada



@app.route("/result")
def resultado():
    return "resultado ?"


@app.route("/consulta")
def consulta():
    token = request.args.get('token')
    return retornarPesquisa(token)



if __name__ == "__main__":
    app.run(debug=True)