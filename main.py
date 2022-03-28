
from bs4 import BeautifulSoup
import requests

def buscarCinemaLP():
    cinemalp = requests.get("http://www.cinemalaplata.com/default.aspx").text
    cinemalp = BeautifulSoup(cinemalp, 'html.parser')
    peliculas = cinemalp.find_all("div", attrs={"class": "item1"})
    return peliculas

def buscarCinepolis():
    cinepolis = requests.get("https://www.cinepolis.com.ar/").text
    cinepolis = BeautifulSoup(cinepolis, 'html.parser')
    peliculas = cinepolis.find("div", attrs={"class": "slider slider-horizontal"}).findChildren("movie-thumb")
    return peliculas

if __name__ == "__main__":
    cinemalp= buscarCinemaLP()
    cinepolis = buscarCinepolis()

    

    

    
