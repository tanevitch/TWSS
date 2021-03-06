import json
import re
import requests

from bs4 import BeautifulSoup
from cine import Cine
from actor import Actor
from funcion import Funcion
from genero import Genero

from pelicula import Pelicula

def cargarGeneros(generos) -> list[Genero]:
    generos= generos.split(",")
    return [Genero(g) for g in generos]

def cargarActores(actores) -> list[Actor]:
    actores= actores.split(",")
    return [Actor(a) for a in actores]
    
def cargarFuncionesCinemaLP(cineyhorarios) -> list[Funcion]:
    cine = cineyhorarios.find("a", attrs={"class": "cine"})
    formato= cine.parent.get_text().split("-")[1].strip()
    cine = cine.get_text()
    horarios = cineyhorarios.find_all("span", attrs={"id": re.compile(".*Horarios.*")})
    # cineurl= cine.find("a").get("href")
    # cine= requests.get("http://www.cinemalaplata.com/"+cineurl).text
    # cine = BeautifulSoup(cine, 'html.parser')
    l= []
    for horario in horarios: #va asi por si esta en español y subtitulada
        horario = horario.get_text().split(" - ")
        idioma= horario[0].split("     ")[0].split(":")[0]

        horario = horario + [horario[0].split("     ")[1]]
        horario.remove(horario[0])

        for h in horario: 
            l.append(Funcion(idioma, h, Cine(cine), formato))

    return l
    

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
    
    funciones= peli.find("div", attrs={"id": "ctl00_cph_pnFunciones"}).findChildren("div")
    listafunciones= []
    for f in funciones:
        listafunciones.extend(cargarFuncionesCinemaLP(f))

    return Pelicula(titulo, genero, duracion, actores, directores, listafunciones)

def buscarCinemaLP():
    cinemalp = requests.get("http://www.cinemalaplata.com/cartelera.aspx").text
    cinemalp = BeautifulSoup(cinemalp, 'html.parser')
    peliculas = cinemalp.find_all("div", attrs={"class": "page-container singlepost"})
    listapeliculas= []
    for pelicula in peliculas:
        listapeliculas.append(cargarPeliculaCinemaLP(pelicula))

    return listapeliculas
    
def persistir():
    data= {"peliculas": [pelicula.toJSON() for pelicula in buscarCinemaLP()]}
    with open('./data/cinemalp.json', 'w', encoding="utf8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4, sort_keys=True)
    
    return data