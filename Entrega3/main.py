import json
from rdflib import Graph, Literal, RDF, URIRef, OWL
from rdflib.namespace import FOAF , XSD

json_peliculas = open('mergeado.json')

g = Graph()
g.parse("movies.owl", format="owl", encoding="utf-8")
uri = URIRef("http://www.semanticweb.org/movies")

for movie in json.load(json_peliculas):
    g.add((uri, RDF.type, uri))

    
