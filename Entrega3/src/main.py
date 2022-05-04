import json
from rdflib import Graph, Literal, RDF, RDFS, URIRef, OWL, Namespace
from rdflib.namespace import FOAF , XSD
from datetime import datetime
from recolector import recolectar_imdb



BASE_URL = Namespace("http://www.semanticweb.org/")
BASE_SCHEMAORG_URL = Namespace("https://schema.org/")

g = Graph()
g.bind("schema", BASE_SCHEMAORG_URL)
g.bind("sw", BASE_URL)

def count_individuals_of(node_type: str, url= BASE_URL):
    return len(list(g.triples((None, RDF.type, url[node_type]))))

def add_individual(node_type, label, url=BASE_URL):
    
    for s, p, o in g.triples((None, RDFS.label, Literal(label,  lang= "en"))):
        return s

    individual= url[node_type.lower()+str(count_individuals_of(node_type, url))]
    g.add((individual, RDF.type, url[node_type]))
    g.add((individual, RDFS.label, Literal(label, lang="en")))
    g.add((individual, BASE_SCHEMAORG_URL["name"], Literal(label)))
    return individual 

def add_actor(movie, actor):
    actor= add_individual(
            actor.get("@type"),
            actor.get("name"),
            url= BASE_SCHEMAORG_URL
        )
    g.add((movie, BASE_SCHEMAORG_URL["actor"], actor))

def add_genre(movie, genre):
    g.add((movie, BASE_SCHEMAORG_URL["genre"], Literal(genre)))
    
def add_director(movie, director):
    g.add((movie, BASE_SCHEMAORG_URL["director"], add_individual(
            director.get("@type"),
            director.get("name"),
            url= BASE_SCHEMAORG_URL
        )))

def add_rating(movie, rating):
    rating_individual= BASE_URL["aggregateRating"+str(count_individuals_of("AggregateRating", url=BASE_SCHEMAORG_URL))]

    g.add((rating_individual, RDF.type, BASE_SCHEMAORG_URL["AggregateRating"]))
    g.add((rating_individual, BASE_SCHEMAORG_URL["ratingValue"], Literal(rating.get("ratingValue"))))
    g.add((movie, BASE_SCHEMAORG_URL["aggregateRating"], rating_individual))


def add_image(movie, image):
    image_individual= BASE_URL["image"+str(count_individuals_of("ImageObject", url=BASE_SCHEMAORG_URL))]
    g.add((image_individual, RDF.type, BASE_SCHEMAORG_URL["ImageObject"]))
    g.add((image_individual, BASE_SCHEMAORG_URL["contentUrl"], Literal(image)))
    return image_individual

def add_movie(movie):
    movie_individual= add_individual(
        movie.get("@type"),
        movie.get("name"),
        url= BASE_SCHEMAORG_URL
    )
    
    g.add((movie_individual, BASE_SCHEMAORG_URL["duration"], Literal(movie.get("duration"), datatype= XSD.duration))) if movie.get("duration") else None
    g.add((movie_individual, BASE_SCHEMAORG_URL["image"], add_image(movie_individual, movie.get("image")))) if movie.get("image") else None

    g.add((movie_individual, BASE_SCHEMAORG_URL["datePublished"], Literal(datetime.strptime(movie.get("datePublished"), '%Y-%m-%d').isoformat(), datatype=XSD.date))) if movie.get("datePublished") else None

    for actor in movie.get("actor") or []:
        add_actor(movie_individual, actor)

    for genre in movie.get("genre") or []:
        add_genre(movie_individual, genre)
        
    add_director(movie_individual, movie.get("director"))

    add_rating(movie_individual, movie.get("aggregateRating"))


    
if __name__ == "__main__":
    recolectar_imdb()
    with open('../data/mergeado.json', encoding='utf-8') as fh:
        json_peliculas = json.load(fh)


    g.parse("movies.ttl", format='ttl', encoding="utf-8")

    for movie in json_peliculas:
        add_movie(movie)
        

    g.serialize("output.ttl", format="ttl", encoding="utf-8")