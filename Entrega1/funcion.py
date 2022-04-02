class Funcion:
    def __init__(self, idioma, horario, cine, formato, dia=None) -> None:
        self.idioma = idioma.strip().lower()
        self.horario = horario.strip()
        self.cine = cine 
        self.dia = dia
        self.formato = formato.strip().lower()


    def __repr__(self):
        return "\n\tCine: {0}\n\tHorario: {1}\n\tIdioma: {2}".format(self.cine.toJSON(), self.horario, self.idioma)

    def toJSON(self):
        return {
            'idioma': self.idioma,
            'horario': self.horario,
            'cine': self.cine.toJSON(),
            'formato': self.formato,
            'dia': self.dia
            }