import itertools
import json
from actor import Actor
from genero import Genero
from pelicula import Pelicula 
import re
# import spacy
import itertools
from difflib import SequenceMatcher

# nlp = spacy.load("es_dep_news_trf")

def estandarizarMinutos(listaDeMinutos: list[str]):
    return str(min(int(re.search(r'\d+', duracion).group()) for duracion in listaDeMinutos))+ " minutos"


def determinarSimilitudNombre(a, b):
    return SequenceMatcher(None, a, b).ratio()

def determinarSimilitudDirectores(listaDir1, listaDir2):
    puntajes= []
    for dir1 in listaDir1:
        for dir2 in listaDir2:        
            puntajes.append(SequenceMatcher(None, dir1.get("name"), dir2.get("name")).ratio())

    return sum(puntajes)/len(puntajes)

def merge():

    peliculas_jsonld =  json.loads(open('peliculas_jsonld.json', "r", encoding="utf8").read())

    mergeadas = []
    for p1 in peliculas_jsonld:
        for p2 in peliculas_jsonld:
            if p1 != p2 and p1 not in mergeadas and p2 not in mergeadas:
                if determinarSimilitudNombre(p1.get("name"), p2.get("name")) > 0.7 and determinarSimilitudDirectores(p1.get("director"), p2.get("director")) > 0.7:
                    mergeadas.append(p1)
                else:
                    mergeadas.append(p2)

    mergeadas
    mergeadas
merge()