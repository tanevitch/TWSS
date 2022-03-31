import json
 re
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from bs4 import BeautifulSoup
from cine import Cine
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
    
    funciones= []
    
    for boton in botones_dias:
        dia= boton.get_attribute("value")
        boton.click()
        card_cine_todas= driver.find_elements(By.CLASS_NAME,("card"))
        for card_cine in card_cine_todas:
            tipo_funcion_todas = card_cine.find_elements(By.CLASS_NAME,("movie-showtimes-component-combination"))
            for tipo_funcion in tipo_funcion_todas:
                idioma = tipo_funcion.find_element(By.TAG_NAME, "small").get_attribute("textContent")
                for horario in tipo_funcion.find_elements(By.CLASS_NAME, "btn-detail-showtime"):
                    print(idioma.split("•")[2])
                    funciones.append(
                        Funcion(
                            idioma, 
                            horario.get_attribute("textContent"), 
                            Cine(card_cine.text)
                        )
                    )

    actores= cargarActores(dd["Actores"])
    directores= cargarActores(dd["Director"])
    generos= cargarGeneros(dd["Género"])
    duracion= dd["Duración"]
    p= Pelicula(dd["Título Original"], generos, duracion, actores, directores, funciones)
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