import json
from rdflib import Graph, Literal, RDF, RDFS, URIRef, OWL, Namespace
from rdflib.namespace import FOAF , XSD

BASE_URL = Namespace("http://www.semanticweb.org/movies#")
g = Graph()

def count_individuals_of(node_type: str):
    return len(list(g.triples((None, RDF.type, BASE_URL[node_type]))))

def add_individual(node_type, label):
    individual= BASE_URL[node_type.lower()+str(count_individuals_of(node_type))]
    g.add((individual, RDF.type, BASE_URL[node_type]))
    g.add((individual, RDFS.label, Literal(label)))

json_peliculas = open('mergeado.json')

g.parse("movies.ttl", format='ttl', encoding="utf-8")

for movie in json.load(json_peliculas):
    add_individual(
        movie.get("@type"),
        movie.get("name")
    )
    for actor in movie.get("actor") or []:
        add_individual(
            "Actor",
            actor.get("name")
        )
    
    

g.serialize("output.ttl", format="ttl", encoding="utf-8")
    