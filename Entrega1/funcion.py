class Funcion:
    def __init__(self, idioma, horario, cine, dia=None) -> None:
        self.idioma = idioma.strip()
        self.horario = horario.strip()
        self.cine = cine 
        self.dia = dia

    def __repr__(self):
        return "\n\tCine: {0}\n\tHorario: {1}\n\tIdioma: {2}".format(self.cine, self.horario, self.idioma)

    def toJSON(self):
        return {
            'idioma': self.idioma,
            'horario': self.horario,
            'cine': self.cine.toJSON(),
            'dia': self.dia
            }