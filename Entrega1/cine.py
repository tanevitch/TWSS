class Cine:
    def __init__(self, nombre=None, direccion=None, telefono=None) -> None:
        self.nombre= nombre.strip()
        self.direccion= direccion.strip()
        self.telefono=telefono.strip()

    def toJSON(self):
        return {
            'nombre': self.nombre,
        }