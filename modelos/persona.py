import datetime as dt

class Persona:

    def __init__(self, id_persona: int, origen, destino):
        self.id_persona = id_persona
        self.origen = origen
        self.destino = destino

        self.estado = "esperando"  # esperando, viajando, llegado
        self.hora_creacion = dt.datetime.now()
        self.hora_partida = None
        self.hora_llegada = None
        self.tiempo_espera = 0
        self.tiempo_viaje = 0

    def subir_tren(self, tren):
        self.estado = "viajando"
        self.hora_partida = dt.datetime.now()
        self.tiempo_espera = (self.hora_partida - self.hora_creacion).total_seconds()
        print(f"Persona {self.id_persona} sube al tren {tren.nombre} desde {self.origen.nombre}.")

    def bajar_tren(self, estacion):
        self.estado = "llegado"
        self.hora_llegada = dt.datetime.now()
        self.tiempo_viaje = (self.hora_llegada - self.hora_partida).total_seconds() if self.hora_partida else 0
        print(f"Persona {self.id_persona} bajó en {estacion.nombre}. Tiempo de viaje: {self.tiempo_viaje:.1f}s.")

    def resumen(self):
        return {
            "id": self.id_persona,
            "origen": self.origen.nombre,
            "destino": self.destino.nombre,
            "estado": self.estado,
            "espera_segundos": self.tiempo_espera,
            "viaje_segundos": self.tiempo_viaje
        }

    def __repr__(self):
        return f"<Persona {self.id_persona}: {self.origen.nombre} → {self.destino.nombre} | {self.estado}>"