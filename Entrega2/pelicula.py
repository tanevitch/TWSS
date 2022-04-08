class Pelicula:
    def __init__(self, titulo, generos, duracion, actores, directores, funciones):
        self.titulo= titulo.strip().lower().title()
        self.duracion= duracion.strip().lower()
        self.generos= generos
        self.actores= actores
        self.directores = directores
        self.funciones= funciones

    def __repr__(self):
        return "\nTitulo: {0}\n Generos: {1}\n Duracion: {2}\n Actores: {3}\n Directores: {4}\n Funciones: {5}".format(self.titulo,self.generos,self.duracion, self.actores, self.directores, [x for x in self.funciones])

    def duraMenosDe(self, unaDuracion):
        return self.duracion <= unaDuracion 

    def toJSON(self):
        return {
            "titulo": self.titulo,
            "duracion": self.duracion,
            "actores": [ a.toJSON() for a in self.actores],
            "directores": [ d.toJSON() for d in self.directores],
            "generos": [ g.toJSON() for g in self.generos],
            "funciones": [ f.toJSON() for f in self.funciones]
        }