
from difflib import SequenceMatcher
import json

def determinarSimilitudNombre(a, b):
    return SequenceMatcher(None, a, b).ratio()

def determinarSimilitudDirector(persona1, persona2):
    try:
        nombre1 = persona1.get("name").lower()
        nombre2 = persona2.get("name").lower()
    except:
        return 0

    return determinarSimilitudNombre(nombre1, nombre2)

def agregar(unapelicula, otrapelicula, lista: list):
    if determinarSimilitudNombre(unapelicula.get("name"), otrapelicula.get("name")) > 0.6:
        lista.append(otrapelicula)

    return lista

def determinar_similares():
    with open('data/rottentomatoes.json', 'r', encoding="utf8") as openfile:  
        rotten_tomatoes= json.load(openfile)
    
    with open('data/imdb.json', 'r', encoding="utf8") as openfile:  
        imdb= json.load(openfile)

    with open('data/ecartelera.json', 'r', encoding="utf8") as openfile:  
        ecartelera= json.load(openfile)
    

    lista_iguales= []
    for una in rotten_tomatoes:
        iguales= []
        for otra in imdb+ecartelera:
            agregar(una, otra, iguales)
            
        iguales.append(una)
        lista_iguales.append(iguales)

    return lista_iguales
