class Cine:
    def __init__(self, nombre, direccion, telefono) -> None:
        self.nombre= nombre
        self.direccion= direccion
        self.telefono=telefono

    def toJSON(self):
        return {
            'nombre': self.nombre,
        }