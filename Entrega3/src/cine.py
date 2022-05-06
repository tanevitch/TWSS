class MovieTheater:
    def __init__(self, nombre) -> None:
        self.nombre= nombre.strip().title()


    def toJSON(self):
        return {
            '@type': 'MovieTheater',
            'name': self.nombre,
        }