class Genero:
    def __init__(self, nombre):
        self.nombre = nombre.strip().title()
        

    def __repr__(self):
        return self.nombre

    def toJSON(self):
        return {'nombre': self.nombre}