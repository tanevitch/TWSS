import json

class Pelicula:
    def __init__(self, titulo, generos, duracion, actores, directores):
        self.titulo= titulo.strip()
        self.duracion= duracion.strip()
        self.generos= generos
        self.actores= actores
        self.directores = directores

    def __repr__(self):
        return "\nTitulo: {0}\n Generos: {1}\n Duracion: {2}\n Actores: {3}\n Directores: {4}".format(self.titulo,self.generos,self.duracion, self.actores, self.directores)

    def duraMenosDe(self, unaDuracion):
        return self.duracion <= unaDuracion 

    def jsonify(self):
        return json.dumps(self, default=lambda o: o.__dict__)