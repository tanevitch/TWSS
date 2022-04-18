
from difflib import SequenceMatcher
from itertools import chain

import json

def determinarSimilitudNombre(a, b):
    return SequenceMatcher(None, a, b).ratio()

def determinarSimilitudDirector(persona1, persona2):
    try:
        if type(persona1) == list:
            persona1 = persona1[0]
        if type(persona2) == list:
            persona2 = persona2[0]

        nombre1 = persona1.get("name").lower()
        nombre2 = persona2.get("name").lower()
    except:
        return 0

    return determinarSimilitudNombre(nombre1, nombre2)

def determinarSimilitudActores(pelicula1, pelicula2):
    try:
        actoresPelicula1= pelicula1.get("actor") if pelicula1.get("actor")!= None else pelicula1.get("actors")
        actoresPelicula2= pelicula2.get("actor") if pelicula2.get("actor")!= None else pelicula2.get("actors")

        actoresPelicula1= list(map(lambda a: a.get("name"), actoresPelicula1))
        actoresPelicula2= list(map(lambda a: a.get("name"), actoresPelicula2))

        suma = 0
        for a1 in actoresPelicula1:
            for a2 in actoresPelicula2:
                suma+= determinarSimilitudNombre(a1, a2)
        return suma/len(actoresPelicula1)
    except: 
        # filmaffinity no tiene declarados los actores
        return 0
    

def determinarSimilitudGeneros(generos1, generos2):
    try:
        suma = 0
        for a1 in generos1:
            for a2 in generos2:
                suma+= determinarSimilitudNombre(a1, a2)
        return suma/len(generos1)
    except: 
        return 0

def agregar(unapelicula, otrapelicula, lista: list):
    if determinarSimilitudNombre(unapelicula.get("name"), otrapelicula.get("name")) > 0.6:
        if determinarSimilitudDirector(unapelicula.get("director"), otrapelicula.get("director")) > 0.6 or determinarSimilitudActores(unapelicula, otrapelicula) > 0.6 or determinarSimilitudGeneros(unapelicula.get("genre"), otrapelicula.get("genre")) > 0.3:
            lista.append(otrapelicula)

    return lista

def determinar_similares():
    with open('data/rottentomatoes.json', 'r', encoding="utf8") as openfile:  
        rotten_tomatoes= json.load(openfile)
    
    with open('data/imdb.json', 'r', encoding="utf8") as openfile:  
        imdb= json.load(openfile)

    with open('data/ecartelera.json', 'r', encoding="utf8") as openfile:  
        ecartelera= json.load(openfile)
    
    with open('data/filmaffinity.json', 'r', encoding="utf8") as openfile:  
        filmaffinity= json.load(openfile)
    

    lista_iguales= []
    for una in imdb:
        iguales= []
        for otra in rotten_tomatoes+ecartelera+filmaffinity:
            agregar(una, otra, iguales)
            
        iguales.append(una)
        lista_iguales.append(iguales)

    for each in [each for each in rotten_tomatoes+ecartelera+filmaffinity if each not in list(chain(*lista_iguales))]:
        lista_iguales.append([each])
        
    return lista_iguales
