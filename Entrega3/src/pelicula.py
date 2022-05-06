class Movie:
    def __init__(self, titulo, funciones):
        self.titulo= titulo.strip().lower().title()
        self.funciones= funciones

    def toJSON(self):
        return {
            "@type": 'Movie',
            "name": self.titulo,
            "events": [ f.toJSON() for f in self.funciones]
        }