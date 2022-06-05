from rdflib import Graph, URIRef, OWL, Namespace
from dpedia_service import DbpediaService
from wikidata_service import WikidataService

GRAFO = Graph() 
SCHEMA= Namespace("http://schema.org/")

def load_movies():
    GRAFO.parse("dataset-original.ttl", format='ttl', encoding="utf-8")

def get_resource_from_graph(graph, nombre_actor):
    return graph.query("""
                    select ?subject  where {
                        ?subject rdfs:label ?label .
                        filter(?label="%s"@en)
                    }
                    """%(nombre_actor))

def enrich_actor(actor: URIRef, grafo: Graph, triples, nombre_actor: str):
    for row in get_resource_from_graph(triples, nombre_actor):
        grafo.add((actor, OWL.sameAs, row.subject))
    grafo+=triples

def enrich_dbpedia(actor: URIRef, nombre_actor: str, grafo: Graph):
    dbpediaservice = DbpediaService()
    triples = dbpediaservice.get_actor_by_name(nombre_actor)
    if triples:
        enrich_actor(actor, grafo, triples, nombre_actor)
    triples = dbpediaservice.get_directed_by_oscar_winner(nombre_actor) 

    if triples:
        for s,p,o in triples:
            grafo.add((actor, p, o))
    
def enrich_wikidata(actor: URIRef, nombre_actor: str, grafo: Graph):
    wikidataservice = WikidataService()
    triples = wikidataservice.get_actor_by_name(nombre_actor)
    if triples:
        enrich_actor(actor, grafo, triples, nombre_actor)
    triples = wikidataservice.get_directed_by_oscar_winner(nombre_actor) 
    if triples:
        for s,p,o in triples:
            grafo.add((actor, p, o))

if __name__ == "__main__":
    load_movies()
    for s,o,p in GRAFO.triples((None, SCHEMA["actor"], None)):
        nombre_actor = p.split("/")[3].replace("_", " ")
        enrich_dbpedia(p, nombre_actor, GRAFO)
        enrich_wikidata(p, nombre_actor, GRAFO)
    GRAFO.serialize("grafo-enriquecido.ttl", format="ttl", encoding="utf-8")

