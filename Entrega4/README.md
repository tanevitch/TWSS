# Moviepedia
Enriquecedor de ontología de películas, cargada con individuals obtenidos a partir de scrappear a cinemalp e IMDB.

## Estructura
- dataset-original.ttl es el grafo obtenido con scrapping
- links.ttl son las tripletas de owl:sameAs, generadas a partir de consultar a dbpedia por los actores del dataset original
- dataset-enriquecido.ttl es el grafo obtenido luego de enriquecer el original con ciertas propiedades de dbpedia

## Instalación
```sh
git clone https://github.com/tanevitch/TWSS.git && cd TWSS/Entrega4
python -m venv .env
.env\Scripts\activate
pip install -r requirements.txt
python main.py -i dataset-original.ttl -o dataset-enriquecido.ttl
```
