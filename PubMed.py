import json
import requests
import progressbar
import time
import xmltodict
from ngrama import Artigo, n_grams_json
'''
===================================================================================================================================================


==================================================================================================================================================='''


def obterArtigos_PubMed(termo, busca_rapida):

    apikey = ''  # minha key
    lista_artigos = []
    database = 'pubmed'

    if busca_rapida:
        limite = 10
    else:
        limite = 200

    # BUSCA TODOS OS LINKS DOS ARTIGOS QUE CONTÉM O TERMO BUSCADO
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={database}&term={termo}&retmax={limite}&retmode=json"
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

    lst_ids = artigos['esearchresult']['idlist']  # SALVA A LISTA DE IDs

    print("Carregando artigos...")

    # LOOP DOS 2000 LINKS JUNTANDO DE 10 EM 10
    for loop10 in progressbar.progressbar(range(0, limite, 10)):

        url2 = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db={database}&id={lst_ids[loop10+0]},{lst_ids[loop10+1]},{lst_ids[loop10+2]},{lst_ids[loop10+3]},{lst_ids[loop10+4]},{lst_ids[loop10+5]},{lst_ids[loop10+6]},{lst_ids[loop10+7]},{lst_ids[loop10+8]},{lst_ids[loop10+9]}&retmode=xml&sort=relevance'
        resultado2 = requests.get(url2)

        while resultado2.status_code != 200:
            print(
                f"Erro de requisição: [{resultado.status_code}] {resultado.reason}")
            print("Tentando nova conexão...")
            time.sleep(200)
            resultado2 = requests.get(url)

        resultado_xml = resultado2.text
        # CONVERTE O XML EM DICIONÁRIO ORDENADO
        xml_convertido = xmltodict.parse(resultado_xml)
        # CONVERTE O DICIONÁRIO ORDENADO EM OBJETO JSON
        resultado_json = json.loads(json.dumps(xml_convertido))

        for indice_artigo in range(10):
            # FORMATOS DE RESPOSTA:
            titulo = resultado_json['PubmedArticleSet']['PubmedArticle'][
                indice_artigo]['MedlineCitation']['Article']['ArticleTitle']
            if type(titulo) != str:
                titulo = resultado_json['PubmedArticleSet']['PubmedArticle'][
                    indice_artigo]['MedlineCitation']['Article']['ArticleTitle']['#text']
            

            resumo = resultado_json['PubmedArticleSet']['PubmedArticle'][
                indice_artigo]['MedlineCitation']['Article']['Abstract']['AbstractText']
            if type(resumo) != str:
                try:
                    resumo = resultado_json['PubmedArticleSet']['PubmedArticle'][
                        indice_artigo]['MedlineCitation']['Article']['Abstract']['AbstractText']['#text']
                except TypeError as e:
                    print("Exception: {}".format(e))
                    resumo = ""
            
            date_f = resultado_json['PubmedArticleSet']['PubmedArticle'][
                indice_artigo]['MedlineCitation']['Article']['ArticleDate']
            dia = date_f['Day']
            mes = date_f['Month']
            ano = date_f['Year']
            date = f'{dia}/{mes}/{ano}'
            doi = resultado_json['PubmedArticleSet']['PubmedArticle'][indice_artigo][
                'PubmedData']['ArticleIdList']['ArticleId'][1]['#text']

            lista_artigos.append({  # SALVA OS DADOS NA LISTA NOVA USANDO A CLASSE ARTIGO
                "titulo": titulo,
                "resumo": resumo,
                "date": date,
                "doi": doi,
                "link": "https://doi.org/" + doi
            })

    # SALVA APENAS TÍTULO E RESUMO DOS ARTIGOS EM CLASSES NA LISTA FINAL
    lista_ngramas = [Artigo(x['titulo'], x['resumo']) for x in lista_artigos]

    return lista_ngramas, lista_artigos


def obterNgramas_ScienceDirect(termo):

    lista_final = obterArtigos_PubMed(termo)

    resultados = n_grams_json(lista_final)

    return resultados
