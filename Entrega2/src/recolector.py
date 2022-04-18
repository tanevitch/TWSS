
import json
from bs4 import BeautifulSoup
import requests
import extruct 

def obtener_microdatos(urls):
    peliculas= []
    for url in urls:
        html = requests.get(url).text   
        contenido= extruct.extract(html, url, syntaxes=['microdata', 'json-ld'], uniform=True)
        peliculas.append(contenido['microdata'][0])
    return peliculas

def obtener_json_ld(urls):
    peliculas = []
    for url in urls:
        html = requests.get(url).text   
        soup = BeautifulSoup(html, "html.parser")
        contenido = soup.find("script", {"type":"application/ld+json"}).contents
        peliculas.append(json.loads("".join(contenido), strict=False))
    return peliculas

def recolectar_rottentomatoes():
    fuentes= ["https://www.rottentomatoes.com/m/the_batman",
        "https://www.rottentomatoes.com/m/coda_2021",
        "https://www.rottentomatoes.com/m/fantastic_beasts_the_secrets_of_dumbledore"]
    
    with open("data/rottentomatoes.json", "w",encoding='utf8') as outfile:
        outfile.write(json.dumps(obtener_json_ld(fuentes), indent=4, ensure_ascii=False))
    
def recolectar_imdb():
    fuentes= ["https://www.imdb.com/title/tt10366460/?ref_=nv_sr_srsg_0",
    "https://www.imdb.com/title/tt4123432/?ref_=nv_sr_srsg_0",
    "https://www.imdb.com/title/tt1877830/?ref_=fn_al_tt_1"]
    with open("data/imdb.json", "w",encoding='utf8') as outfile:
        outfile.write(json.dumps(obtener_json_ld(fuentes), indent=4, ensure_ascii=False))

def recolectar_ecartelera():
    fuentes= ["https://www.ecartelera.com/peliculas/animales-fantasticos-y-donde-encontrarlos-3/",
    "https://www.ecartelera.com/peliculas/coda-2021/",
    "https://www.ecartelera.com/peliculas/the-batman"]
    with open("data/ecartelera.json", "w",encoding='utf8') as outfile:
        outfile.write(json.dumps(obtener_json_ld(fuentes), indent=4, ensure_ascii=False))

def recolectar_filmaffinity():
    fuentes= ["https://www.filmaffinity.com/ar/film911057.html", "https://www.filmaffinity.com/ar/film867354.html","https://www.filmaffinity.com/ar/film660003.html"]
    with open("data/filmaffinity.json", "w",encoding='utf8') as outfile:
        outfile.write(json.dumps(obtener_microdatos(fuentes), indent=4, ensure_ascii=False))

def recolectar_datos():
    recolectar_rottentomatoes()
    recolectar_imdb()
    recolectar_filmaffinity()
    recolectar_ecartelera()