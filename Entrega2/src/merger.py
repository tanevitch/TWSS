from itertools import chain
import datetime
from googletrans import Translator, constants
translator = Translator()


def mergearTitulo(titulos: list[str]):
    return titulos[0]

def obtenerActores(peliculas):
    # una fuente usa actors, que fue luego reemplazada por actor
    try:
        actores= []
        for pelicula in peliculas:
            actores.extend(pelicula.get("actor") if pelicula.get("actor")!= None else pelicula.get("actors"))
        return actores
    except: 
        # filmaffinity no tiene declarados los actores
        return None

def mergearPersonas(personas: list):
    nombres= set(filter(None, map(lambda p: p.get("name").lower(), personas)))
    nombres = list(filter(lambda n: n!="na", nombres)) #rottentomatoes los tiene como NA a veces
    personas = [{
        "@type": "Person",
        "name": nombre.title()
    } for nombre in nombres]


    return personas

def mergearGeneros(generos: list[str]): 
    generos= list(set(map(lambda g:translator.translate(g.lower(), dest="en").text, generos)))
    generos= list(set(map(lambda g:translator.translate(g.title(), dest="es").text, generos)))
    return generos

def mergearDuracion(duracion: list[str]):
    duracion = set(duracion)
    for d in duracion: 
        if "T" in d: #esta en el formato iso
            return d 
    return None

def mergearFechaPublicacion(fp: list[str]): 
    fp = set(fp)
    for f in fp:
        try:
            datetime.datetime.strptime(f, '%Y-%m-%d')
            return f
        except ValueError:
            pass

    return None

def normalizarRating(ratings: list):
    for rating in ratings:
        rating["ratingValue"]= float(str(rating.get("ratingValue")).replace(",", ".")) if rating.get("ratingValue") != None else 0
        if rating.get("bestRating") == "100" or rating.get("bestRating") == 100:
            rating["ratingValue"]= rating.get("ratingValue")/10


def mergearRating(ratings: list):
    normalizarRating(ratings)
    return {
        "bestRating": 10,
        "worstRating": 0,
        "ratingValue": sum(map(lambda r: r.get("ratingValue"), ratings))/ len(ratings)
    }

def agregarAtributo(obj, nombreAtributo, fun, *params):
    try: 
        if fun == None:
            valor= params
        else:
            valor = fun(*params)
        if (valor is not None and len(valor)!=0):
            obj[nombreAtributo]= valor
    except:
        return None #que no agregue el atributo

def mergePeliculas(peliculas: list):
    nuevo_objeto= {
        "@context": "http://schema.org",
        "@type": "Movie"
    }
    agregarAtributo(nuevo_objeto, "name", mergearTitulo, list(
             filter(
                    None, list(map(lambda p: p.get("name") ,peliculas))
                )
            ))
    agregarAtributo(nuevo_objeto, "datePublished", mergearFechaPublicacion, list(
            filter(
                None, list(map(lambda p: p.get("datePublished"), peliculas)))
                ))

    agregarAtributo(nuevo_objeto, "genre", mergearGeneros, list(chain(
            *list(map(lambda p: p.get("genre"), peliculas))
            )))

    agregarAtributo(nuevo_objeto, "duration", mergearDuracion, list(
                filter(
                    None, list(map(lambda p: p.get("duration"), peliculas))
                )
            ))

    agregarAtributo(nuevo_objeto, "director", mergearPersonas, list(chain(
                *list(map(lambda p: p.get("director"), peliculas))
            )))

    agregarAtributo(nuevo_objeto, "actor", mergearPersonas, obtenerActores(peliculas))

    agregarAtributo(nuevo_objeto, "image", None, list( 
               filter(
                    None, list(map(lambda p: p.get("image"), peliculas))
                )
            ))
    
    agregarAtributo(nuevo_objeto, "aggregateRating", mergearRating, list(
                filter(
                    None, list(map(lambda p: p.get("aggregateRating"), peliculas))
                )
            ))


    return nuevo_objeto

    







