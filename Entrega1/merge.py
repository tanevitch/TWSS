

import json


def merge():
    with open('Entrega1/cinepolis.json', 'r', encoding="utf8") as fp:
        cinepolis = json.load(fp)
    
     
    with open('Entrega1/cinemalp.json', 'r', encoding="utf8") as fp:
        cinemalp =json.load(fp)

    titulos_consolidados = []
    titulos_cinemalp= [p.get("titulo") for p in cinemalp.get("peliculas")]
    titulos_cinepolis= [p.get("titulo") for p in cinepolis.get("peliculas")]

    for t in titulos_cinemalp:
        if t in titulos_cinepolis:
            titulos_consolidados.append(t)

    for t in titulos_consolidados:
        info_cinemalp =next(p for p in cinemalp.get("peliculas") if p.get("titulo")==t) 
        info_cinepolis= next(p for p in cinepolis.get("peliculas") if p.get("titulo")==t) 
        actores_de_p = set([x.get("nombre") for x in info_cinemalp.get("actores") + info_cinepolis.get("actores")] )

merge()