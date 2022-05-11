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
BASE_DBPEDIA_URL = Namespace("https://dbpedia.org/ontology/")
G.bind("dbo", BASE_DBPEDIA_URL)

def search_required_properties(actor_triples):
    actor_graph= Graph()
    actor_graph.parse(data=actor_triples)
    attributes_to_add= {}
    for s,o,p in actor_graph.triples((None, BASE_DBPEDIA_URL["birthDate"] ,None)):
        attributes_to_add["birthDate"] = p
    
    for s,o,p in actor_graph.triples((None,  BASE_DBPEDIA_URL["occupation"] ,None)):
        attributes_to_add["occupation"] = p
    
    return attributes_to_add

def get_resource_url(obj):
    return SAMEAS_G.value(subject=obj, predicate=OWL.sameAs)

def get_ttl_url(obj):
    
    formats = requests.get(get_resource_url(obj)).headers["Link"].split(",")
    for f in formats:
        if "ttl" in f:
            return re.compile(r"http([\s\S]+).ttl").search(f).group().replace("<","").replace(">", "")

def search_actors():
    for s,o,p in G.triples((None, BASE_SCHEMAORG_URL["actor"], None)):
  
        actor_triples=  requests.get(get_ttl_url(p)).text
        
        G.add((p, OWL.sameAs, URIRef(get_resource_url(p))))

        attributes = search_required_properties(actor_triples)
        for attribute_name in attributes.keys():
            G.add((p, BASE_DBPEDIA_URL[attribute_name], attributes[attribute_name]))




def dbpedia_search():
    search_actors()

def load_movies():
    # parser = argparse.ArgumentParser()                                               
    # parser.add_argument("--input", "-i", type=str, required=True)
    # args = parser.parse_args()
    # G.parse(args.input, format='ttl', encoding="utf-8")
    G.parse("dataset-original.ttl", format='ttl', encoding="utf-8")
    SAMEAS_G.parse("links.ttl", format='ttl', encoding="utf-8")

if __name__ == "__main__":
    load_movies()
    
    dbpedia_search()
    G.serialize("dataset-enriquecido.ttl", format="ttl", encoding="utf-8")