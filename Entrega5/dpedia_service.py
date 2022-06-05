from query_service import QueryService


class DbpediaService(QueryService):
    def __init__(self) -> None:
        self.url = "http://dbpedia.org/sparql"

    def query_actor_by_name(self, actor_name: str):
        return """
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
            """%(actor_name)

    def query_directed_by_oscar_winner(self, actor_name):
        return """
            PREFIX sw: <http://www.semanticweb.org#>      
            CONSTRUCT{
                ?actor1 sw:was-DirectedByOscarWinner ?actor2
            } 
             WHERE {
                SELECT DISTINCT ?actor1 ?actor2 {
                    ?movie rdf:type schema:Movie .
                    ?movie dbo:starring ?actor1.
                    ?actor1 rdfs:label ?labelActor1.
                    ?movie dbo:director ?actor2 .
                    ?actor2 dbo:award dbr:Academy_Awards .
                    filter(?labelActor1="%s"@en)    
               }
            }
        """%(actor_name)