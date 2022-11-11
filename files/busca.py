import os, files.obterArtigo as obterArtigo
from collections import Counter
from files.ngrama import n_grams_json

os.system('cls')

def buscaMultipla(palavras):
    buscas = palavras.split(";")
    for termo_busca in buscas:
        efetuarBusca(termo_busca)


def efetuarBusca(termo_busca, busca_rapida, lista_bases):
    termo_formatado = termo_busca.replace(" ", "%20")

    artigos_retornados = list()
    total_anos = list()
    total_assuntos = list()
    artigos_total_ngramas = list()
    artigos_em_string_json = list()

    if "SD" in lista_bases:
        print(f"[ScienceDirect]: Pesquisando informações sobre: {termo_busca}")
        artigos_retornados.extend(
            obterArtigo.ScienceDirect(termo_formatado, busca_rapida))

    if "SL" in lista_bases:
        print(f"[SpringerLink]: Pesquisando informações sobre: {termo_busca}")
        artigos_retornados.extend(
            obterArtigo.SpringerLink(termo_formatado, busca_rapida))
    
    #PARA NGRAMAS
    for classe_artigo in artigos_retornados:
        artigos_total_ngramas += classe_artigo.ngramas


    #PARA ARTIGOS
    for classe_artigo in artigos_retornados:
        artigos_em_string_json.append(classe_artigo.__str__())

    #PARA ASSUNTOS
    for assunto in artigos_retornados:
        if assunto.assunto == 'No subject':
            pass
        elif type(assunto.assunto) != list:
            total_assuntos.append(assunto.assunto)
        else:
            total_assuntos.extend(assunto.assunto)

    #PARA ANOS
    for ano in artigos_retornados:
        total_anos.append(ano.ano)

    resultado_ngramas = n_grams_json(artigos_retornados)
    total_anos = list(Counter(total_anos).most_common())
    total_assuntos = list(Counter(total_assuntos).most_common())

    print(f"Busca sobre '{termo_busca}' concluída.\n")

    #retornarResultado(resultado_ngramas, termo_busca)

    return {"resultado_ngramas": resultado_ngramas, "artigos_em_string_json": artigos_em_string_json, "total_assuntos": total_assuntos, "total_anos": total_anos}