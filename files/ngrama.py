import nltk
nltk.download('stopwords')
from collections import Counter
from nltk import bigrams, word_tokenize
from nltk.corpus import stopwords
import json

stop = stopwords.words('english') + ["systematic", 
"review", "meta-analysis", "randomized", "literature",
"protocol", "trials", "controlled", "(", ")"]

class Artigo():
    """
    Classe artigo a ser utilizada para que sejam atribuídos: 
    Os dados necessários para cada artigo de cada base de dado.
    Métodos para o mapeamento de ngramas.
    """
    def __init__(self, titulo, abstract, data = '', doi = '', link = '', assunto = ''):
        """
        Inicializa os atributos da Classe artigo, sendo obrigatórios o título e abstract.
        """
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
        """
        Mapea os ngramas e atribui a lista de ngramas os bigramas, de acordo com os conteúdos do título e do resumo de cada artigo.
        """

        full = self.titulo + self.abstract
        full = full.lower().replace(",", " ").replace(".", " ").replace(":", " ") # PADRONIZAÇÃO DAS PALAVRAS
        full = word_tokenize(full)
        full = [w for w in full if w not in stop]
   
        self.ngramas = list(bigrams(full))

    def __str__(self) -> str:
        """ 
        Override do str que retorna os atributos de cada artigo instanciado.

        Retorno:
        json.dumps(parameters) (str): Uma string com encoding JSON contendo as informações do objeto Artigo.
        """
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
    """
    Retorna os 50 ngramas mais comuns à partir de uma lista de artigos.
    
    Parâmetros:
    artigos (list): Lista de artigos a ser processada para que se obtenha os ngramas.
    Retorno:
    ngramas_mais_comuns (Counter): Retorna um objeto Counter() contendo os 50 ngramas mais comuns.
    """
    pool_ngrams = []

    for artigo in artigos:
        ngramas_artigo = artigo.ngramas
        pool_ngrams.extend(list(ngramas_artigo))

    ngramas_mais_comuns = Counter(pool_ngrams).most_common(50)

    return ngramas_mais_comuns

def n_grams_json(dados):
    """ 
    Retorna os ngramas em forma de uma lista contendo uma tupla em que: 
    O primeiro termo é uma tupla com cada termo dos bigramas
    O segundo termo é a quantidade desses bigramas.
    Parâmetros:
    dados (Counter()): Lista de artigos como objeto Counter() # TODO: Verificar
    Retorno:
    resultado (list(tuple(tuple(str)), int)): Lista contendo uma tupla com uma tupla dos bigramas e a quantidade dos bigramas.
    """

    artigos = dados
    if type(artigos) is not list:
        n_grams = obter_n_gramas([artigos])
    else:
        n_grams = obter_n_gramas(artigos)

    resultado = [x for x in n_grams if len(' '.join(x[0])) > 3]
    return resultado