class Actor:
    def __init__(self, nombre):
       self.nombre= nombre.strip()

    def __repr__(self):
        return self.nombre