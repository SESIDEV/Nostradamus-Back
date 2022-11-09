from flask import Flask, request
from files.busca import efetuarBusca

app = Flask(__name__)

@app.route("/")
def index():
    #return render_template("content/index.html")
    return 'página principal'


@app.route("/search")
def busca():
    bases = ["springerlink", "sciencedirect"]
    bases_selecionadas = list()
    termo = request.args.get("search")
    busca_rapida = request.args.get("busca-rapida")

    for base in bases:
        if request.args.get(base):
            bases_selecionadas.append(base)

    if termo != None and termo != "":
        resultados = efetuarBusca(termo, busca_rapida, bases_selecionadas) # RETORNA UMA TUPLA (resultado_ngramas, artigos_em_string_json)
        return resultados
        #render_template("content/result.html", termo=termo, resultados_ngramas=resultados[0], dados_das_buscas=resultados[1], total_assuntos=resultados[2], total_anos=resultados[3])
    else:
        resultados = ""
        return resultados
        #render_template("content/search.html")


@app.route("/result")
def resultado():
    return 'resultado' #render_template("content/search.html")


if __name__ == "__main__":
    app.run(debug=True)