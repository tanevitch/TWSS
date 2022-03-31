from ast import Try
import json
import re
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from bs4 import BeautifulSoup
from actor import Actor
from funcion import Funcion
from genero import Genero
    
from pelicula import Pelicula
# driver = webdriver.Chrome('./chromedriver')
driver=  webdriver.Firefox()

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
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "showtimes-filter-component-dates"))
    )
    botones_dias =  driver.find_element_by_class_name('showtimes-filter-component-dates').find_elements(By.TAG_NAME, "button")
    
    
    for boton in botones_dias:
        dia= boton.get_attribute("value")
        boton.click()
        cinesyhorarios= driver.find_elements_by_class_name("card")
        for cineyhorarios in cinesyhorarios:
            cine= cineyhorarios.text #nombrecine
            WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element_attribute((By.CLASS_NAME, "a"))
    )
            for tipo_funcion in driver.execute_script('return document.querySelectorAll(".movie-showtimes-component-combination a")'):
                print(tipo_funcion.text)

            
    actores= cargarActores(dd["Actores"])
    directores= cargarActores(dd["Director"])
    generos= cargarGeneros(dd["Género"])
    duracion= dd["Duración"]
    
    p= Pelicula(dd["Título Original"], generos, duracion, actores, directores, [])
    print(p)
    return p

def buscarCinepolis():
    driver.get("https://www.cinepolis.com.ar/")
    peliculas = [p.get_attribute("href") for p in driver.execute_script('return document.querySelectorAll(".movie-grid .movie-thumb")')]   
    
    listapeliculas= []
    for urlpeli in peliculas:
        try: 
            peli= cargarPeliculaCinepolis(urlpeli)
            listapeliculas.append(peli)
        except: 
            pass
    driver.close()
    return listapeliculas

def persistir():
    data= {"peliculas": [pelicula.toJSON() for pelicula in buscarCinepolis()]}
    with open('cinepolis.json', 'w', encoding="utf8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4, sort_keys=True)