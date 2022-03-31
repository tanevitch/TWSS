class Cine:
    def __init__(self, nombre, direccion=None, telefono=None) -> None:
        self.nombre= nombre.strip()
        self.direccion= direccion
        self.telefono=telefono

    def __repr__(self):
        return "\nNombre: {0}", self.nombre


    def toJSON(self):
        return {
            'nombre': self.nombre,
        }