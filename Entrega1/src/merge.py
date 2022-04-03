

import itertools
import json
from actor import Actor
from cine import Cine
from genero import Genero
from pelicula import Pelicula 
from funcion import Funcion 
import re
import spacy
import itertools

from difflib import SequenceMatcher

nlp = spacy.load("es_dep_news_trf")

def deteminarSimilitud(a, b):
    return SequenceMatcher(None, a, b).ratio()

def estandarizarMinutos(listaDeMinutos: list[str]):
    return str(min(int(re.search(r'\d+', duracion).group()) for duracion in listaDeMinutos))+ " minutos"


def estandarizarGeneros(generos: list[str]):
    lista_generos = []
    for gen_str in generos:
        lista_generos.append(nlp(gen_str))

    lista_generos_lemmatizados = []
    for gen_doc in lista_generos:
        genero_lemmatizado= ""
        for token in gen_doc:
            genero_lemmatizado += token.lemma_  + " "
        lista_generos_lemmatizados.append(genero_lemmatizado)
        
    return set(lista_generos_lemmatizados)

def estandarizarIdioma(idioma: str):
    idioma = nlp(idioma.strip().lower())

    idioma_lemmatizado= ""
    for token in idioma:
        idioma_lemmatizado += token.lemma_  + " "
        
    if (str(idioma_lemmatizado.strip()) in ["español", "castellano"]):
        idioma_lemmatizado= "español latinoamérica"

    return idioma_lemmatizado

def mergeGeneros(generos: list[str]):
    generos_de_p = set([genero.get("nombre") for genero in generos] )
    return [Genero(x) for x in estandarizarGeneros(generos_de_p)]

def mergeActores(actores: list[str]):
    actores_de_p = set([actor.get("nombre") for actor in actores] )
    return [Actor(x) for x in actores_de_p]

def mergeFunciones(funciones):
    funciones_de_p= []
    for f in funciones:
        f["cine"]= Cine(**f["cine"])
        f["idioma"] = estandarizarIdioma(f["idioma"])
        funciones_de_p.append(Funcion(**f))
    return funciones_de_p

def mergeDirectores(directores: list[str]):
    directores_de_p = set([director.get("nombre") for director in directores] )
    return [Actor(x) for x in directores_de_p]

def procesarPeliculas(lista_titulos, fuentes:list):
    lista_peliculas= []
    for titulo in lista_titulos:
        info_peli=  [next(p for p in fuente.get("peliculas") if p.get("titulo")==titulo) for fuente in fuentes ]
        peli = Pelicula(
            titulo=titulo,
            generos=mergeGeneros(list(itertools.chain(*[info.get("generos") for info in info_peli]))),
            actores= mergeActores(list(itertools.chain(*[info.get("actores") for info in info_peli]))),
            funciones=mergeFunciones(list(itertools.chain(*[info.get("funciones") for info in info_peli]))),
            duracion=estandarizarMinutos(list(info.get("duracion") for info in info_peli)),
            directores=mergeDirectores(list(itertools.chain(*[info.get("directores") for info in info_peli])))    
        )
        lista_peliculas.append(peli)
    return lista_peliculas

def merge():
    
    json_cinemalp = open ('./data/cinemalp.json', "r", encoding="utf8")
    json_cinepolis = open ('./data/cinepolis.json', "r", encoding="utf8")

    fuentes= {
        "cinemalp": json.loads(json_cinemalp.read()),
        "cinepolis": json.loads(json_cinepolis.read())
    }

    titulos= {
        fuente: set(map(lambda p: p.get("titulo"), fuentes[fuente].get("peliculas"))) for fuente in fuentes

    }

    titulos_identicos = set.intersection(*[set(titulos[key]) for key in titulos]) # necesita una lista de sets

    for titulo in titulos_identicos:
        for fuente in fuentes:
            titulos[fuente].remove(titulo) 
   

    peliculas= []

    # proceso fuente multiple
    peliculas.extend(procesarPeliculas(
        lista_titulos=titulos_identicos,
        fuentes= fuentes.values()
    ))


    #proceso fuente simple
    for fuente in fuentes: 
        peliculas.extend(procesarPeliculas(
            lista_titulos=titulos[fuente],
            fuentes= [fuentes[fuente]]
        ))

    return peliculas


merge()

