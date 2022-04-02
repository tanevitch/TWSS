

import json
from actor import Actor
from cine import Cine
from genero import Genero
from pelicula import Pelicula 
from funcion import Funcion 
import re
import spacy
nlp = spacy.load("es_dep_news_trf")


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

def procesarPeliculas(lista_titulos, cine):
    lista_peliculas= []
    for titulo in lista_titulos:
        info_peli =next(p for p in cine.get("peliculas") if p.get("titulo")==titulo) 

        peli = Pelicula(
            titulo=titulo,
            generos=mergeGeneros(info_peli.get("generos")),
            actores= mergeActores(info_peli.get("actores")),
            funciones=mergeFunciones(info_peli.get("funciones")),
            duracion=estandarizarMinutos([info_peli["duracion"]]),
            directores=mergeDirectores(info_peli.get("directores"))    
        )
        lista_peliculas.append(peli)
    return lista_peliculas

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
        
        peli = Pelicula(
            titulo=t,
            generos=mergeGeneros(info_cinemalp.get("generos") + info_cinepolis.get("generos")),
            actores= mergeActores(info_cinemalp.get("actores") + info_cinepolis.get("actores")),
            funciones=mergeFunciones(info_cinemalp.get("funciones")+info_cinepolis.get("funciones")),
            duracion=estandarizarMinutos([info_cinepolis["duracion"], info_cinemalp["duracion"]]),
            directores=mergeDirectores(info_cinemalp.get("directores")+info_cinepolis.get("directores"))    
        )
        peliculas.append(peli)
    
    

    peliculas.extend(procesarPeliculas(
        lista_titulos=[t for t in titulos_cinemalp if t not in titulos_consolidados],
        cine= cinemalp
    ))

    peliculas.extend(procesarPeliculas(
        lista_titulos=[t for t in titulos_cinepolis if t not in titulos_consolidados],
        cine= cinepolis
    ))


    return peliculas


data= {"peliculas": [pelicula.toJSON() for pelicula in merge()]}
print(data)
with open('mergeadas.json', 'w', encoding="utf8") as fp:
    json.dump(data, fp, ensure_ascii=False, indent=4, sort_keys=True)