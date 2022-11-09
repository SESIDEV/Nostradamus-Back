from flask import Blueprint, render_template, request
from controllers.busca import efetuarBusca
import json
from flask import make_response

def nice_json(arg):
    response = make_response(json.dumps(arg, sort_keys=True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response

main = Blueprint('home', __name__, template_folder='templates')


@main.route("/", methods=['GET'])
def index():
    return nice_json({
        "uri": "/"
    })

@main.route("/search", methods=['GET'])
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
    return nice_json(efetuarBusca(termo_busca, lista_bases, busca_rapida))


@main.route("/result")
def resultado():
    return render_template("content/search.html")
