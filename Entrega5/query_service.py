from abc import ABCMeta, abstractmethod

from SPARQLWrapper import SPARQLWrapper


class QueryService(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        self.url = None

    @abstractmethod
    def query_actor_by_name(self, actor_name: str):
        pass

    @abstractmethod
    def query_directed_by_oscar_winner(self, actor_name: str):
        pass

    def get_directed_by_oscar_winner(self, actor_name: str):
        return self.execute_query(
            self.query_directed_by_oscar_winner(actor_name)
        )

    def get_actor_by_name(self, actor_name: str):
        return self.execute_query(
            self.query_actor_by_name(actor_name)
        )

    def execute_query(self, query: str):
        sparql = SPARQLWrapper(self.url)
        sparql.setQuery(query)
        try : 
            return sparql.queryAndConvert()
        except Exception as e: 
            print("Error: "+str(e))