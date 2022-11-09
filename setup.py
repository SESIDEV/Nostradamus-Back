from flask import Flask, request
from files.busca import efetuarBusca
import json
from flask import make_response

def print_json(arg):
    response = make_response(json.dumps(arg, sort_keys=True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response

app = Flask(__name__)

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
    return print_json(efetuarBusca(termo_busca, lista_bases, busca_rapida))


@app.route("/result")
def resultado():
    return ""

if __name__ == "__main__":
    app.run(debug=True, port=5001)