from query_service import QueryService


class WikidataService(QueryService):
    def __init__(self) -> None:
        self.url= "http://query.wikidata.org/sparql"
        
    def query_actor_by_name(self, actor_name: str):
        return """
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
        """%(actor_name)

    def query_directed_by_oscar_winner(self, actor_name):
        return """
            PREFIX sw: <http://www.semanticweb.org#>      
            CONSTRUCT{
                ?actor1 sw:wasDirectedByOscarWinner ?actor2
            } 
            WHERE {
                SELECT DISTINCT ?actor1 ?actor2 
                WHERE {
                    ?movie wdt:P31 wd:Q11424.
                    ?movie wdt:P161 ?actor1.
                    ?actor1 ?label ?labelActor1.
                    ?movie wdt:P57 ?actor2 .
                    ?actor2 wdt:P166 wd:Q19020 .
                    filter(?labelActor1="%s"@en)    
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } 
                }
            }
        """%(actor_name)

        