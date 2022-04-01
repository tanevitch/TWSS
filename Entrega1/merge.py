

import json
from actor import Actor
from genero import Genero
from pelicula import Pelicula 
from funcion import Funcion 
import re
import spacy

nlp = spacy.load("es_dep_news_trf")


def estandarizarMinutos(listaDeMinutos):
    return str(min(int(re.search(r'\d+', duracion).group()) for duracion in listaDeMinutos))+ " minutos"


def estandarizarGeneros(generos):
    lista_generos = []
    for gen_str in generos:
        lista_generos.append(nlp(gen_str))

    lista_generos_lemmatizados = []
    for gen_doc in lista_generos:
        genero_lemmatizado= ""
        for token in gen_doc:
            genero_lemmatizado += token.lemma_  + " "
        lista_generos_lemmatizados.append(genero_lemmatizado.strip())
        
    return set(lista_generos_lemmatizados)

def merge():
    with open('cinepolis.json', 'r', encoding="utf8") as fp:
        cinepolis = json.load(fp)
    
     
    with open('cinemalp.json', 'r', encoding="utf8") as fp:
        cinemalp =json.load(fp)

    titulos_consolidados = []
    titulos_cinemalp= [p.get("titulo") for p in cinemalp.get("peliculas")]
    titulos_cinepolis= [p.get("titulo") for p in cinepolis.get("peliculas")]

    for t in titulos_cinemalp:
        if t in titulos_cinepolis:
            titulos_consolidados.append(t)

    peliculas= []
    for t in titulos_consolidados:
        info_cinemalp =next(p for p in cinemalp.get("peliculas") if p.get("titulo")==t) 
        info_cinepolis= next(p for p in cinepolis.get("peliculas") if p.get("titulo")==t) 

        generos_de_p = set([x.get("nombre") for x in info_cinemalp.get("generos") + info_cinepolis.get("generos")] )
        generos_de_p = [Genero(x) for x in estandarizarGeneros(generos_de_p)]

        actores_de_p = set([x.get("nombre") for x in info_cinemalp.get("actores") + info_cinepolis.get("actores")] )
        actores_de_p = [Actor(x) for x in actores_de_p]

        funciones_de_p = [x for x in info_cinemalp.get("funciones") + info_cinepolis.get("funciones")]
        duracion_de_p = estandarizarMinutos([info_cinepolis["duracion"], info_cinemalp["duracion"]])

        
        peli = Pelicula(t, generos_de_p, duracion_de_p, actores_de_p, [], [])
        peliculas.append(peli)


    for t in [t for t in titulos_cinemalp if t not in titulos_consolidados]:
        info_cinemalp =next(p for p in cinemalp.get("peliculas") if p.get("titulo")==t) 

        generos_de_p = [x.get("nombre") for x in info_cinemalp.get("generos")]
        generos_de_p = [Genero(x) for x in estandarizarGeneros(generos_de_p)]

        actores_de_p = [x.get("nombre") for x in info_cinemalp.get("actores")]
        actores_de_p = [Actor(x) for x in actores_de_p]

        funciones_de_p = [x for x in info_cinemalp.get("funciones")]
        duracion_de_p = estandarizarMinutos(info_cinemalp["duracion"])

        
        peli = Pelicula(t, generos_de_p, duracion_de_p, actores_de_p, [], [])
        peliculas.append(peli)


    return peliculas


data= {"peliculas": [pelicula.toJSON() for pelicula in merge()]}
with open('mergeadas.json', 'w', encoding="utf8") as fp:
    json.dump(data, fp, ensure_ascii=False, indent=4, sort_keys=True)