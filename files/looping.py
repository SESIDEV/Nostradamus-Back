from conector import buscarPesquisasPendentes, prepararParaPesquisa, incluirNoBanco
from busca import efetuarBusca
import json, time

def rodarPesquisasContinuas():
    while True:
        time.sleep(5)
        print('\n##################################################\nBuscando requisição...')
        token_encontrado = buscarPesquisasPendentes() # BUSCA POR REQUESTS COM STATUS PENDENTES

        if token_encontrado != '':
            print('\nRequisição encontrada.')
            dados_pesquisa = prepararParaPesquisa(token_encontrado) # RETORNA OS DADOS DO REQUEST E ALTERA SEU STATUS PARA 'EM PROGRESSO'

            termo_busca = dados_pesquisa[0]
            bool_busca_rapida = dados_pesquisa[1]
            lista_bases = json.loads(dados_pesquisa[2])['bases']

            resultadoJson = json.dumps(efetuarBusca(termo_busca, bool_busca_rapida, lista_bases)) # REALIZA A BUSCA NAS BASES SELECIONADAS E RETORNA UM RESULTADO EM JSON
            
            print('\nRequisição concluída.')
            incluirNoBanco(token_encontrado, resultadoJson) # ADICIONA A BUSCA COMPLETA NA TABELA DE PESQUISAS E ALTERA O STATUS DO REQUEST PARA CONCLUÍDO
        else:
            print('Nenhuma requisição pendente.')