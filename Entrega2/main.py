from bs4 import BeautifulSoup
import requests
import json

# https://www.metacritic.com/movie/the-batman ver por qué no se puede

# batmanURLs= ["https://www.rottentomatoes.com/m/the_batman",
#             "https://www.ecartelera.com/peliculas/the-batman",
#             "https://www.imdb.com/title/tt1877830/?ref_=fn_al_tt_1"]

# batmanJSONs = []
# for url in batmanURLs:
#     html = requests.get(url).text   
#     soup = BeautifulSoup(html, "html.parser")
#     contenido = soup.find("script", {"type":"application/ld+json"}).contents
#     batmanJSONs.append(json.loads("".join(contenido), strict=False))

# with open('peliculas_jsonld.json', 'w', encoding="utf8") as fp:
#     json.dump(batmanJSONs, fp, ensure_ascii=False, indent=4, sort_keys=True)

batman_jsonld= json.loads(open('peliculas_jsonld.json', "r", encoding="utf8").read())

