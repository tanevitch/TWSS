from itertools import chain
from googletrans import Translator, constants
translator = Translator()

# https://www.metacritic.com/movie/the-batman ver por qué no se puede



def mergearTitulo(titulos: list[str]):
    return titulos[0]

def obtenerActores(peliculas):
    # una fuente usa actors, que fue luego reemplazada por actor
    actores= []
    for pelicula in peliculas:
        actores.extend(pelicula.get("actor") if pelicula.get("actor")!= None else pelicula.get("actors"))
    return actores


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
    # ver si poner el mainEntityOfPage
    return next(iter(set(duracion)))

def mergearFechaPublicacion(fp: list[str]): 
    return next(iter(set(fp)))

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

    

def mergePeliculas(peliculas: list):
    return {
        "@context": "http://schema.org",
        "@type": "Movie",
        "name": mergearTitulo(list(
             filter(
                    None, list(map(lambda p: p.get("name") ,peliculas))
                )
            )),
        "genre": mergearGeneros(list(chain(
            *list(map(lambda p: p.get("genre"), peliculas))
            ))),
        "datePublished": mergearFechaPublicacion(list(
            filter(
                None, list(map(lambda p: p.get("datePublished"), peliculas)))
                )
            ),
        "duration": mergearDuracion(
            list(
                filter(
                    None, list(map(lambda p: p.get("duration"), peliculas))
                )
            )
        ),
        "director": mergearPersonas(list(chain(
                *list(map(lambda p: p.get("director"), peliculas))
            ))),
        "actor": mergearPersonas(obtenerActores(peliculas)),
        "image": 
           list( 
               filter(
                    None, list(map(lambda p: p.get("image"), peliculas))
                )
            )
        ,
        "aggregateRating": mergearRating(list(
                filter(
                    None, list(map(lambda p: p.get("aggregateRating"), peliculas))
                )
            ))
    }

    







