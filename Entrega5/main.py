from typing import final
from rdflib import Graph, Literal, RDF, RDFS, URIRef, OWL, Namespace
from rdflib.namespace import FOAF , XSD
from SPARQLWrapper import JSON, TURTLE, SPARQLWrapper, RDFXML
import re

dbr= Namespace("http://dbpedia.org/resource/")
schema= Namespace("http://schema.org/")

GRAFO = Graph() 
GRAFO.bind("dbr", dbr)
GRAFO.bind("dbo", "http://dbpedia.org/ontology/")
GRAFO.bind("dbp", "http://dbpedia.org/property/")
GRAFO.bind("schema", schema)


def load_movies():
    GRAFO.parse("dataset-original.ttl", format='ttl', encoding="utf-8")

def get_resource_from_graph(graph):
    return graph.query("""
                    select ?subject  where {
                        ?subject rdfs:label ?label .
                        filter(?label="%s"@en)
                    }
                    """%(nombre_actor))


def execute_query(query_service: str, query: str, grafo: Graph, actor: URIRef):
    sparql = SPARQLWrapper(query_service)

    sparql.setQuery(query)
    try : 
        triples = sparql.queryAndConvert()
        for row in get_resource_from_graph(triples):
            grafo.add((actor, OWL.sameAs, row.subject))
        grafo+=triples
    except Exception as e: 
        print("Error: "+str(e))

def enrich_dbpedia(actor, nombre_actor: str, grafo):
    query_service= "http://dbpedia.org/sparql"
    # ver si agregar ?subject rdf:type dbo:Person .
    
    query = """
    CONSTRUCT{
            ?subject ?property ?object
        } WHERE {
            ?subject ?property ?object . 
            
            { ?subject dbo:occupation dbr:Actor . }
            UNION {
                ?subject dbp:occupation ?occupation
                FILTER (contains(str(?occupation), "Actor") ||
                contains(str(?occupation), "Actress")) 
            }
            ?subject rdfs:label ?label .
            filter(?label="%s"@en)    
         }
    """%(nombre_actor)
    
    execute_query(query_service, 
                    query,
                    grafo, 
                    actor)
    

def enrich_wikidata(actor, nombre_actor: str, grafo):
    query_service= "http://query.wikidata.org/sparql"

    query = """
        CONSTRUCT{
            ?subject ?property ?object
        } WHERE {
            ?subject ?property ?object .
            ?subject wdt:P31 wd:Q5 .
            {  ?subject wdt:P106 wd:Q10800557 . }
            UNION {
                ?subject wdt:P106 ?occupation
                        FILTER (contains(str(?occupation), "Actor") ||
                                contains(str(?occupation), "Actress")) 
            }
            ?subject ?label "%s"@en.
            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
    """%(nombre_actor)
    execute_query(query_service, 
                    query,
                    grafo, 
                    actor) 



if __name__ == "__main__":
    load_movies()
    for s,o,p in GRAFO.triples((None, schema["actor"], None)):
        nombre_actor = p.split("/")[3].replace("_", " ")
        enrich_dbpedia(p, nombre_actor, GRAFO)
        enrich_wikidata(p, nombre_actor, GRAFO)

    GRAFO.serialize("grafo-enriquecido.ttl", format="ttl", encoding="utf-8")

