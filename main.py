
from bs4 import BeautifulSoup
import requests
from pelicula import Pelicula
from actor import Actor
from genero import Genero

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


import re 
import json 
import pprint

def cargarGeneros(generos) -> [Genero]:
    generos= generos.split(",")
    return [Genero(a) for a in generos]

def cargarActores(actores) -> [Actor]:
    actores= actores.split(",")
    return [Actor(a) for a in actores]

def cargarPeliculaCinemaLP(pelicula) -> Pelicula:
    url= pelicula.find("a").get("href")
    peli= requests.get("http://www.cinemalaplata.com/"+url).text
    peli = BeautifulSoup(peli, 'html.parser')
    titulo= peli.find("div", attrs={"class": "page-title"}).get_text()
    informacion= peli.find_all("div", attrs={"class": "dropcap6"})
    for i in informacion:
        if (i.find("span", attrs={"id": "ctl00_cph_lblGenero"})): 
            genero= cargarGeneros(i.find("span", attrs={"id": "ctl00_cph_lblGenero"}).get_text())
        elif (i.find("span", attrs={"id": "ctl00_cph_lblDuracion"})): 
            duracion= i.find("span", attrs={"id": "ctl00_cph_lblDuracion"}).get_text()
        elif (i.find("span", attrs={"id": "ctl00_cph_lblActores"})): 
            actores= cargarActores(i.find("span", attrs={"id": "ctl00_cph_lblActores"}).get_text())
        elif (i.find("span", attrs={"id": "ctl00_cph_lblDirector"})):
            directores= cargarActores(i.find("span", attrs={"id": "ctl00_cph_lblDirector"}).get_text())

    return Pelicula(titulo, genero, duracion, actores, directores)

def buscarCinemaLP():
    cinemalp = requests.get("http://www.cinemalaplata.com/cartelera.aspx").text
    cinemalp = BeautifulSoup(cinemalp, 'html.parser')
    peliculas = cinemalp.find_all("div", attrs={"class": "page-container singlepost"})
    listapeliculas= []
    for pelicula in peliculas:
        p= cargarPeliculaCinemaLP(pelicula)
        print(p)
        listapeliculas.append(p)

    return listapeliculas

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


    actores= cargarActores(dd["Actores"])
    directores= cargarActores(dd["Director"])
    generos= cargarGeneros(dd["Género"])
    duracion= dd["Duración"]
    
    p= Pelicula(dd["Título Original"], generos, duracion, actores, directores)
    print(p)
    return p

def buscarCinepolis():
    driver = webdriver.Chrome('./chromedriver') 
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

if __name__ == "__main__":
    # cinemalp= buscarCinemaLP()
    data= {
        "peliculas": [pelicula.jsonify() for pelicula in buscarCinepolis()]
    }
    with open('cinepolis.json', 'w', encoding="utf8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4, sort_keys=True)

    

    

    
