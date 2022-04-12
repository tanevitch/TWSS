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

def estandarizarMinutos(listaDeMinutos: [str]):
    return str(min(int(re.search(r'\d+', duracion).group()) for duracion in listaDeMinutos))+ " minutos"

def cargarPelicula(itemJSONLD):
    titulo= ""
    genre= []
    duration = ""
    actors = []
    director = []
    try:
        titulo= itemJSONLD.get("name")
        genre = itemJSONLD.get("genre")
        duration = itemJSONLD.get("duration") 
        actors= itemJSONLD.get("actors") or itemJSONLD.get("actor")
        director = itemJSONLD.get("director")
    except: 
        pass 

    return Pelicula(
                titulo,
                set(genre),
                duration,
                mergeActores(actors),
                mergeActores(director)
            )


def mergeActores(actores):
    actores_de_p = set([actor.get("name") for actor in actores] )
    return [Actor(x) for x in actores_de_p]
    
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
    for index1 in range(len(peliculas_jsonld)):
        estructura_merge = {
            "name": None,
            "genre": [],
            "duration": "",
            "actors": [],
            "director": []
        }
        for index2 in range(len(peliculas_jsonld)):
            if index1 != index2 and peliculas_jsonld[index1] != None and peliculas_jsonld[index2] != None and determinarSimilitudNombre(peliculas_jsonld[index1].get("name"), peliculas_jsonld[index2].get("name")) > 0.7 and determinarSimilitudDirectores(peliculas_jsonld[index1].get("director"), peliculas_jsonld[index2].get("director")) > 0.7:
                estructura_merge["name"]= peliculas_jsonld[index1].get("name") if estructura_merge["name"]==None else None
                estructura_merge["director"].extend([*peliculas_jsonld[index1].get("director"), *peliculas_jsonld[index2].get("director")])
                estructura_merge["duration"]= peliculas_jsonld[index1].get("duration") or peliculas_jsonld[index2].get("duration")

                estructura_merge["genre"].extend([*peliculas_jsonld[index1].get("genre"), *peliculas_jsonld[index2].get("genre")])
                estructura_merge["actors"].extend([*peliculas_jsonld[index1].get("actor"), *peliculas_jsonld[index2].get("actor")])

                peliculas_jsonld[index2]= None
        if estructura_merge["name"] == None and peliculas_jsonld[index1] != None:
            mergeadas.append(cargarPelicula(peliculas_jsonld[index1]))

        elif peliculas_jsonld[index1] != None:
            nueva_pelicula= cargarPelicula(estructura_merge)
            mergeadas.append(nueva_pelicula)
        peliculas_jsonld[index1]= None
            
    mergeadas
merge()