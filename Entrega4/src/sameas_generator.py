import json
from rdflib import Graph, Literal, RDF, RDFS, URIRef, OWL, Namespace
from rdflib.namespace import FOAF , XSD


def search_sameAs(input_file):
    same_as_graph = Graph()
    
    input_graph = Graph()
    input_graph.parse(input_file, format='ttl', encoding="utf-8")

    base_url = Namespace(input_graph.value(predicate=RDF.type,object=OWL.Ontology)+"/")
    base_schemaorg_url = Namespace("https://schema.org/")
    dbr= Namespace("http://dbpedia.org/resource/")
    same_as_graph.bind("dbr", dbr)
    same_as_graph.bind("sw", base_url)
    for s,o,p in input_graph.triples((None, base_schemaorg_url["actor"], None)):
        nombre_actor = p.split("/")[3]
        same_as_graph.add((p, OWL.sameAs, dbr[nombre_actor]))
    same_as_graph.serialize("../data/links.ttl", format="ttl", encoding="utf-8")
