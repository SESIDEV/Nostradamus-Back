from collections import Counter
from nltk import bigrams, word_tokenize
from nltk.corpus import stopwords
import json

stop = stopwords.words('english') + ["systematic", 
"review", "meta-analysis", "randomized", "literature",
"protocol", "trials", "controlled", "(", ")"]

class Artigo():
    def __init__(self, titulo, abstract, data = '', doi = '', link = '', assunto = ''):
        self.ngramas = []
        self.titulo = titulo if titulo is not None else ""
        self.abstract = abstract if abstract is not None else ""
        self.link = link
        self.ano = data[:4]
        self.mes = data[5:7]
        self.data = data
        self.assunto = assunto
        self.mapear_ngramas()

    def mapear_ngramas(self, n = 2):
        # Corpus é uma lista de artigos

        full = self.titulo + self.abstract
        full = full.lower().replace(",", " ").replace(".", " ").replace(":", " ") # PADRONIZAÇÃO DAS PALAVRAS
        full = word_tokenize(full)
        full = [w for w in full if w not in stop]
   
        self.ngramas = list(bigrams(full))

    def __str__(self) -> str:
        parameters = {
            'titulo': self.titulo,
            'abstract': self.abstract,
            'link': self.link,
            'ano': self.ano,
            'mes': self.mes,
            'data': self.data,
            'assunto': self.assunto,
        }
        return json.dumps(parameters)

def obter_n_gramas(artigos):
    pool_ngrams = []

    for artigo in artigos:
        ngramas_artigo = artigo.ngramas
        pool_ngrams.extend(list(ngramas_artigo))

    ngramas_mais_comuns = Counter(pool_ngrams).most_common(50)

    return ngramas_mais_comuns

def n_grams_json(dados):
    artigos = dados
    if type(artigos) is not list:
        n_grams = obter_n_gramas([artigos])
    else:
        n_grams = obter_n_gramas(artigos)

    resultado = [x for x in n_grams if len(' '.join(x[0])) > 3]
    return resultado