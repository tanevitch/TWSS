import json
import re
import requests

from bs4 import BeautifulSoup
from cine import MovieTheater
from funcion import ScreeningEvent
from pelicula import Movie

    
def cargarFuncionesCinemaLP(cineyhorarios) -> list[ScreeningEvent]:
    cine = cineyhorarios.find("a", attrs={"class": "cine"})
    formato= cine.parent.get_text().split("-")[1].strip()
    cine = cine.get_text()
    horarios = cineyhorarios.find_all("span", attrs={"id": re.compile(".*Horarios.*")})
    l= []
    for horario in horarios: 
        horario = horario.get_text().split(" - ")
        horario = horario + [horario[0].split(": ")[1]]

        horario.remove(horario[0])

        for h in horario: 
            l.append(ScreeningEvent(h, MovieTheater(cine), formato))

    return l
    

def cargarPeliculaCinemaLP(pelicula) -> Movie:
    url= pelicula.find("a").get("href")
    peli= requests.get("http://www.cinemalaplata.com/"+url).text
    peli = BeautifulSoup(peli, 'html.parser')
    titulo= peli.find("div", attrs={"class": "page-title"}).get_text()
    
    funciones= peli.find("div", attrs={"id": "ctl00_cph_pnFunciones"}).findChildren("div")
    listafunciones= []
    for f in funciones:
        listafunciones.extend(cargarFuncionesCinemaLP(f))

    return Movie(titulo, listafunciones)

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

