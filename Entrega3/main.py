import json
from rdflib import Graph, Literal, RDF, RDFS, URIRef, OWL, Namespace
from rdflib.namespace import FOAF , XSD

BASE_URL = Namespace("http://www.semanticweb.org/")
BASE_SCHEMAORG_URL = Namespace("https://schema.org/")

g = Graph()
g.bind("schema", BASE_SCHEMAORG_URL)
g.bind("sw", BASE_URL)

def count_individuals_of(node_type: str, url= BASE_URL):
    return len(list(g.triples((None, RDF.type, url[node_type]))))

def add_individual(node_type, label):
    
    for s, p, o in g.triples((None, RDFS.label, Literal(label,  lang= "es"))):
        return s

    individual= BASE_URL[node_type.lower()+str(count_individuals_of(node_type))]
    g.add((individual, RDF.type, BASE_URL[node_type]))
    g.add((individual, RDFS.label, Literal(label, lang= "es")))
    return individual 

def add_actor(movie, actor):
    actor= add_individual(
            "Actor",
            actor.get("name")
        )
    g.add((movie, BASE_SCHEMAORG_URL["actor"], actor))
    g.add((actor, BASE_URL["playsIn"], movie))

def add_genre(movie, genre):
    g.add((movie, BASE_URL["hasGenre"], add_individual(
            "Genre",
            genre
        )))
    
def add_director(movie, director):
    g.add((movie, BASE_SCHEMAORG_URL["director"], add_individual(
            "Director",
            director.get("name")
        )))

def add_rating(movie, rating):
    rating_individual= BASE_URL["aggregateRating"+str(count_individuals_of("AggregateRating", url=BASE_SCHEMAORG_URL))]

    g.add((rating_individual, RDF.type, BASE_SCHEMAORG_URL["AggregateRating"]))
    g.add((rating_individual, BASE_URL["ratingValue"], Literal(rating.get("ratingValue"))))
    g.add((movie, BASE_SCHEMAORG_URL["aggregateRating"], rating_individual))

def add_movie(movie):
    movie_individual= add_individual(
        movie.get("@type"),
        movie.get("name")
    )
    
    g.add((movie_individual, BASE_URL["duration"], Literal(movie.get("duration")))) if movie.get("duration") else None
    g.add((movie_individual, BASE_SCHEMAORG_URL["dateCreated"], Literal(movie.get("datePublished"), datatype=BASE_SCHEMAORG_URL["Date"]))) if movie.get("datePublished") else None

    for actor in movie.get("actor") or []:
        add_actor(movie_individual, actor)
    

    for genre in movie.get("genre") or []:
        add_genre(movie_individual, genre)
        
    for director in movie.get("director") or []:
        add_director(movie_individual, director)

    add_rating(movie_individual, movie.get("aggregateRating"))

with open('mergeado.json', encoding='utf-8') as fh:
    json_peliculas = json.load(fh)


g.parse("movies.ttl", format='ttl', encoding="utf-8")

for movie in json_peliculas:
    add_movie(movie)
    

g.serialize("output.ttl", format="ttl", encoding="utf-8")
    