from scrapper_cinemalp import persistir as persistir_cinemalp
from scrapper_cinepolis import persistir as persistir_cinepolis
from merge import merge
import json

if __name__ == "__main__":
    # persistir_cinemalp()
    # persistir_cinepolis()
    
    data= {"peliculas": [pelicula.toJSON() for pelicula in merge()]}
    print(data)
    with open('./data/mergeadas.json', 'w', encoding="utf8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4, sort_keys=True)