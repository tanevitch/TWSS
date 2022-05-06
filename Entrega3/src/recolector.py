
import json
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def obtener_json_ld(urls):
    peliculas = []
    for url in urls:
        html = requests.get(url).text   
        soup = BeautifulSoup(html, "html.parser")
        contenido = soup.find("script", {"type":"application/ld+json"}).contents
        peliculas.append(json.loads("".join(contenido), strict=False))
    return peliculas

    
def recolectar_imdb():
    with open('data/cinemalp.json', encoding='utf-8') as fh:
        json_peliculas = json.load(fh)

    peliculas= []
    for pelicula in json_peliculas["peliculas"]:
        peliculas.append(pelicula)

    driver=  webdriver.Firefox()
    driver.get("https://www.imdb.com/?ref_=nv_home")
    fuentes= []
    for pelicula in peliculas:
        driver.find_element_by_id("suggestion-search").send_keys(pelicula.get("name"))
        primer_resultado= driver.find_element(By.CLASS_NAME, "imdb-header__search-menu")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sc-bqyKva"))
        )
        fuentes.append(primer_resultado.find_element(By.CLASS_NAME, "sc-bqyKva").get_attribute("href"))
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sc-hBEYos"))
        )
        pelicula["name"]= primer_resultado.find_element(By.CLASS_NAME, "sc-hBEYos").get_attribute("textContent")
        driver.find_element_by_id("suggestion-search").clear()
    driver.close()
    

    with open("data/imdb.json", "w",encoding='utf8') as outfile:
        outfile.write(json.dumps(obtener_json_ld(fuentes), indent=4, ensure_ascii=False))

    with open('data/cinemalp.json', 'w', encoding="utf8") as fp:
        json.dump(peliculas, fp, ensure_ascii=False, indent=4, sort_keys=True)


