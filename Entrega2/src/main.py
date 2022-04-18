from merger import mergePeliculas as mergePeliculas
from recolector import recolectar_datos
from procesador import determinar_similares
import json

if __name__ == "__main__":
    # recolectar_datos()
    grupos= determinar_similares()
    mergeados= [mergePeliculas(grupo) for grupo in grupos]
        
    with open('data/mergeado.json', 'w', encoding="utf8") as openfile: 
        openfile.write(json.dumps(mergeados, indent=4, ensure_ascii=False))
        
     
