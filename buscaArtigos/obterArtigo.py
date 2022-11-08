import json
import requests
import progressbar
import time
from buscaArtigos.ngrama import Artigo

# CONVERTE O RESULTADO DA BUSCA INDIVIDUAL DE ARTIGOS DE XML PARA JSON
xml_to_json = {'Accept': 'application/json'}

# Chaves das APIs
api_key_sciencedirect = 'e53f507ae669632b072347e2f2010545'  # Key para API do ScienceDirect
api_key_busca_sciencedirect = '7f59af901d2d86f78a1fd60c1bf9426a'  # Key para busca na API do ScienceDirect?
api_key_springerlink = '0c43e1aa36f88f6d3215f4223f6e2306' # Key para API do SpringerLink

def ScienceDirect(termo, busca_rapida):
    indice_busca = 1
    idx = 1
    links_artigos = list()
    lista_artigos = list()

    if busca_rapida:
        limite = 2
    else:
        limite = 100

    while (idx <= 5):  # LOOP PARA PEGAR MAIS DE 100 LINKS
        # BUSCA TODOS OS LINKS DOS ARTIGOS QUE CONTÉM O TERMO BUSCADO
        url = f"https://api.elsevier.com/content/search/sciencedirect?query={termo}&count={limite}&start={indice_busca}&apikey={api_key_busca_sciencedirect}"
        time.sleep(1)  # Sleep para evitar Erro 429 (excesso de requests)
        # RETORNA UM OBJETO 'RESPONSE' COM O METODO GET
        resultado = requests.get(url)

        while resultado.status_code != 200:
            print(
                f"Erro de requisição: [{resultado.status_code}] {resultado.reason}")
            print("Tentando nova conexão...")
            time.sleep(200)
            resultado = requests.get(url)

        # Transforma a resposta JSON em um objeto Python
        artigos = json.loads(resultado.text)

        try:
            artg_todos = artigos['search-results']['entry']
            # USA O LOOPING DO RANGE COMO INDEX PARA CADA ARTIGO
            for artigo in range(len(artg_todos)):
                links_artigos.append(
                    artigos['search-results']['entry'][artigo]['link'][0]['@href'])
            indice_busca += 100
            idx += 1
        except KeyError:
            break

    # Útil?
    del resultado

    print("Carregando artigos...")

    # Barra de Progresso
    for link in progressbar.progressbar(links_artigos):
        url = link + "?apikey=" + api_key_sciencedirect  # RETORNA UM OBJETO 'RESPONSE' COM O METODO GET
        resultado = requests.get(url, headers=xml_to_json)

        while resultado.status_code != 200:
            print(
                f"Erro de requisição: [{resultado.status_code}] {resultado.reason}")
            print("Tentando nova conexão...")
            # Esperar 200 segundos para tentar outro request
            time.sleep(200)
            resultado = requests.get(url, headers=xml_to_json)

        # CARREGA O TEXTO DO RESPONSE COMO JSON EM UM OBJETO PYTHON
        artigo = json.loads(resultado.text)

        # FORMATOS DE RESPOSTA:
        titulo = artigo["full-text-retrieval-response"]['coredata']['dc:title']
        resumo = artigo["full-text-retrieval-response"]['coredata']['dc:description']
        if resumo is not None:
            resumo = resumo.strip()
        data = artigo["full-text-retrieval-response"]['coredata']['prism:coverDate']
        doi = artigo["full-text-retrieval-response"]['coredata']['dc:identifier']
        link = artigo["full-text-retrieval-response"]['coredata']['link'][-1]['@href']
        try:
            subject_list = artigo["full-text-retrieval-response"]['coredata']['dcterms:subject']
            subject = [x['$'] for x in subject_list]
        except KeyError as e:
            subject = "No subject"

        lista_artigos.append(Artigo(  # SALVA OS DADOS NA LISTA NOVA USANDO A CLASSE ARTIGO
            titulo,
            resumo,
            data,
            doi,
            link,
            subject
        ))

    return lista_artigos


def SpringerLink(termo, busca_rapida):
    indice_busca = 1
    quantidade = 10
    artigos_brutos = list()
    lista_artigos = list()

    if busca_rapida:
        qtd_loops = 1
    else:
        qtd_loops = 200

    # LOOPING PARA PEGAR MAIS DE 10 ARTIGOS
    for x in progressbar.progressbar(range(qtd_loops)):
        # BUSCA DE TODOS OS ARTIGOS QUE CONTÉM O TERMO BUSCADO
        url = f"http://api.springernature.com/meta/v2/json?q={termo}&s={indice_busca}&count={quantidade}&api_key={api_key_springerlink}"
        # RETORNA UM OBJETO 'RESPONSE' COM O METODO GET
        resultado = requests.get(url)

        while resultado.status_code != 200:
            print(
                f"Erro de requisição: [{resultado.status_code}] {resultado.reason}")
            print("Tentando nova conexão...")
            time.sleep(200)
            resultado = requests.get(url)

        # CARREGA O TEXTO DO RESPONSE COMO JSON EM UM OBJETO PYTHON
        artigos = json.loads(resultado.text)
        artigos_brutos.extend(artigos['records'])
        indice_busca += quantidade

    print("Separando artigos...")

    # TODO: Refatorar
    # Iterando pela quantidade de artigos
    for index in range(len(artigos_brutos)):
        # FORMATOS DE RESPOSTA:
        titulo = artigos_brutos[index]['title']
        resumo = artigos_brutos[index]['abstract']
        if resumo is not None:
            resumo = resumo.strip()

        # TODO: Melhorar lógica
        try:
            data = artigos_brutos[index]['onlineDate']
        except KeyError as e:
            print(f"Não foi possível puxar o {e}, será obtido o publishedDate\n")
            try:
                data = artigos_brutos[index]['publishedDate']
            except KeyError as e2:
                print(f"Não foi possível puxar o {e2}, será obtido então o publicationDate\n")
                data = artigos_brutos[index]['publicationDate']

        doi = artigos_brutos[index]['doi']
        link = artigos_brutos[index]['url'][0]['value']
        try:
            subject = artigos_brutos[index]['keyword']
        except KeyError as e:
            subject = "No subject"

        lista_artigos.append(Artigo(  # SALVA OS DADOS NA LISTA NOVA USANDO A CLASSE ARTIGO
            titulo,
            resumo,
            data,
            doi,
            link,
            subject
        ))

    # SALVA APENAS TÍTULO E RESUMO DOS ARTIGOS EM CLASSES NA LISTA FINAL

    return lista_artigos
