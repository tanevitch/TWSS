
import json
from bs4 import BeautifulSoup
import requests

def obtener_json_ld(urls):
    peliculas = []
    for url in urls:
        html = requests.get(url).text   
        soup = BeautifulSoup(html, "html.parser")
        contenido = soup.find("script", {"type":"application/ld+json"}).contents
        peliculas.append(json.loads("".join(contenido), strict=False))
    return peliculas

    
def recolectar_imdb():
    fuentes= [
        "https://www.imdb.com/title/tt1840309/",
        "https://www.imdb.com/title/tt2908446/",
        "https://www.imdb.com/title/tt3410834/",
        "https://www.imdb.com/title/tt1392170/",
        "https://www.imdb.com/title/tt1951264/",
        "https://www.imdb.com/title/tt1951266/",
        "https://www.imdb.com/title/tt1951265/"

    ]
    with open("data/mergeado.json", "w",encoding='utf8') as outfile:
        outfile.write(json.dumps(obtener_json_ld(fuentes), indent=4, ensure_ascii=False))



