import json
from rdflib import Graph, Literal, RDF, RDFS, URIRef, OWL, Namespace
from rdflib.namespace import FOAF , XSD
import argparse
import requests
import re 

G = Graph()
SAMEAS_G= Graph()
BASE_URL = Namespace("http://www.semanticweb.org/")
BASE_SCHEMAORG_URL = Namespace("https://schema.org/")
BASE_DBPEDIA_URL = Namespace("http://dbpedia.org/property/") 
G.bind("dbp", BASE_DBPEDIA_URL)

def search_required_properties(actor_triples, actor_uri):
    actor_graph= Graph()
    actor_graph.parse(data=actor_triples)
        
    triples_to_add= []

    for s,o,p in actor_graph.triples((actor_uri, BASE_DBPEDIA_URL["birthDate"] ,None)):
        triples_to_add.append([s,o,p])

    
    for s,o,p in actor_graph.triples((actor_uri,  BASE_DBPEDIA_URL["occupation"] ,None)):
        triples_to_add.append([s,o,p])
    
    return triples_to_add

def get_resource_url(obj):
    return SAMEAS_G.value(subject=obj, predicate=OWL.sameAs)

def get_ttl_url(obj):
    
    formats = requests.get(get_resource_url(obj)).headers["Link"].split(",")
    for f in formats:
        if "ttl" in f:
            return re.compile(r"http([\s\S]+).ttl").search(f).group().replace("<","").replace(">", "")

def search_actors():
    for s,o,p in G.triples((None, BASE_SCHEMAORG_URL["actor"], None)):
        
        actor_uri= URIRef(get_resource_url(p))
        G.add((p, OWL.sameAs, actor_uri))

        actor_triples=  requests.get(get_ttl_url(p)).text
        attributes = search_required_properties(actor_triples, actor_uri)

        for attribute in attributes:
            s, p, o = attribute
            G.add((s,p,o))




def dbpedia_search():
    search_actors()

def load_movies(input_file):
    G.parse(input_file, format='ttl', encoding="utf-8")
    SAMEAS_G.parse("links.ttl", format='ttl', encoding="utf-8")

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()                                               
    # parser.add_argument("--input", "-i", type=str, required=True)
    # parser.add_argument("--output", "-o", type=str, required=True)
    # args = parser.parse_args()

    # load_movies(args.input)
    # dbpedia_search()

    # G.serialize(args.output, format="ttl", encoding="utf-8")
    load_movies("dataset-original.ttl")
    dbpedia_search()
    G.serialize("dataset-enriquecido.ttl", format="ttl", encoding="utf-8")