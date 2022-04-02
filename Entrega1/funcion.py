class Funcion:
    def __init__(self, idioma, horario, cine, dia=None, tipo_sala=None) -> None:
        self.idioma = idioma.strip().lower()
        self.horario = horario.strip()
        self.cine = cine 
        self.dia = dia
        tipo_sala = tipo_sala


    def __repr__(self):
        return "\n\tCine: {0}\n\tHorario: {1}\n\tIdioma: {2}".format(self.cine.toJSON(), self.horario, self.idioma)

    def toJSON(self):
        return {
            'idioma': self.idioma,
            'horario': self.horario,
            'cine': self.cine.toJSON(),
            'sala': self.tipo_sala,
            'dia': self.dia
            }