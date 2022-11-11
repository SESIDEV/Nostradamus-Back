from conector import buscarPesquisasPendentes, prepararParaPesquisa, incluirNoBanco
from busca import efetuarBusca
import json

def rodarPesquisasContinuas():
    token_encontrado = buscarPesquisasPendentes()

    dados_pesquisa = prepararParaPesquisa()

    termo_busca = dados_pesquisa[0]
    bool_busca_rapida = dados_pesquisa[1]
    lista_bases = json.loads(dados_pesquisa[2])['bases']

    resultadoJson = json.dumps(efetuarBusca(termo_busca, bool_busca_rapida, lista_bases))

    incluirNoBanco(token_encontrado, termo_busca, resultadoJson)