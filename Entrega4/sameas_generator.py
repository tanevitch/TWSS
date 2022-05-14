import json
from rdflib import Graph, Literal, RDF, RDFS, URIRef, OWL, Namespace
from rdflib.namespace import FOAF , XSD


G = Graph()
G.parse("dataset-original.ttl", format='ttl', encoding="utf-8")

BASE_URL = Namespace(G.value(predicate=RDF.type,object=OWL.Ontology)+"/")
BASE_SCHEMAORG_URL = Namespace("https://schema.org/")

def search_sameAs():
    g = Graph()
    dbr= Namespace("http://dbpedia.org/resource/")
    g.bind("dbr", dbr)
    g.bind("sw", BASE_URL)
    for s,o,p in G.triples((None, BASE_SCHEMAORG_URL["actor"], None)):
        nombre_actor = p.split("/")[3]
        g.add((p, OWL.sameAs, dbr[nombre_actor]))
    g.serialize("links.ttl", format="ttl", encoding="utf-8")

search_sameAs()
