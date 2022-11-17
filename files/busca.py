import files.obterArtigo as obterArtigo
from collections import Counter
from files.ngrama import n_grams_json

def efetuarBusca(termo_busca, busca_rapida, lista_bases):
    """
    Função para efetuar as buscas dos termos requisitados nas bases de dados selecionadas.

    Parâmetros:
    termo_busca (str): Termo utilizado pelo usuário para realizar a busca desejada.
    busca_rapida (bool): Variável utilizada para verificação se a busca deve ser rápida/simples ou não.
    lista_bases (list): Lista contendo as bases de dados desejadas pelo usuário.

    Retorno:
    resultado_ngramas list(tuple(tuple(str), int)): Lista contendo uma tupla em que o primeiro termo é uma tupla com cada termo dos bigramas e o segundo termo é a quantidade desses bigramas.
    artigos_em_string_json (list(dict)): # Lista de dicionários contendo título e resumo/abstract de cada artigo.
    total_assuntos (list(str)): Lista de strings dos assuntos mais relevantes de acordo com a busca realizada.
    total_anos (list(tuple)): Lista de tuplas em que o primeiro termo seria o ano e o segundo a quantidade de artigos criados/publicados naquele ano.
    """
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
        artigos_total_ngramas += classe_artigo.ngramas # A LISTA DE NGRAMAS ESTÁ VAZIA PORQUE OS NGRAMAS SÓ SÃO GERADOS NA LINHA 60


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

    print(f"\nBusca sobre '{termo_busca}' concluída.\n")

    return {"resultado_ngramas": resultado_ngramas, "artigos_em_string_json": artigos_em_string_json, "total_assuntos": total_assuntos, "total_anos": total_anos}