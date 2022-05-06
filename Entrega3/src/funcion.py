import datetime


class ScreeningEvent:
    def __init__(self, horario, cine, formato) -> None:
        self.horario = horario.strip()
        self.cine = cine 
        self.dia = datetime.date.today() + datetime.timedelta(days=1)
        self.formato = formato.strip().lower()

    def toJSON(self):
        return {
            '@type': 'ScreeningEvent',
            'location': self.cine.toJSON(),
            'doorTime': f"{self.dia} {self.horario}",
            'videoFormat': self.formato,
        }