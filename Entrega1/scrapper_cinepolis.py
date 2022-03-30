import json
import re
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from bs4 import BeautifulSoup
from actor import Actor
from funcion import Funcion
from genero import Genero

from pelicula import Pelicula
driver = webdriver.Chrome('./chromedriver')
# driver=  webdriver.Firefox()

def cargarGeneros(generos) -> [Genero]:
    generos= generos.split(",")
    return [Genero(a) for a in generos]

def cargarActores(actores) -> [Actor]:
    actores= actores.split(",")
    return [Actor(a) for a in actores]


def cargarPeliculaCinepolis(url) -> Pelicula:
    
    pelicula= requests.get(url).text
    
    pelicula = BeautifulSoup(pelicula, "html.parser")
    informacion = pelicula.find("div", attrs={"id": "tecnicos"})

    infostr= []
    for i in informacion:
        x =  i.get_text().split("\n")
        for f in x:
            infostr.append(f)
    infostr= list(filter(lambda x: x.strip(), infostr))
    dd = {}
    for info in infostr:
        i = info.split(': ')
        dd[i[0]] = i[1]

    driver.get(url)
    funciones =  driver.execute_script('return document.querySelectorAll(".card.panel.panel-primary")') 
    for f in funciones:
        print(f.text())
    

    actores= cargarActores(dd["Actores"])
    directores= cargarActores(dd["Director"])
    generos= cargarGeneros(dd["Género"])
    duracion= dd["Duración"]
    
    p= Pelicula(dd["Título Original"], generos, duracion, actores, directores)
    print(p)
    return p

def buscarCinepolis():
    driver.get("https://www.cinepolis.com.ar/")
    peliculas = driver.execute_script('return document.querySelectorAll(".movie-grid .movie-thumb")')   
    listapeliculas= []
    for p in peliculas:
        try: 
            peli= cargarPeliculaCinepolis(p.get_attribute("href"))
            listapeliculas.append(peli)
        except: 
            pass
    driver.close()
    return listapeliculas

def persistir():
    data= {"peliculas": [pelicula.toJSON() for pelicula in buscarCinepolis()]}
    with open('cinepolis.json', 'w', encoding="utf8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4, sort_keys=True)