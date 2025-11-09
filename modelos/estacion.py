class Estacion:
    def __init__(self, nombre: str, poblacion_total: int):
        self.nombre = nombre
        self.poblacion_total = poblacion_total
        self.vias_conectadas = []
        self.personas_esperando = []
        self.flujo_personas = 0

    def agregar_via(self, via):
        self.vias_conectadas.append(via)

    def llegada_tren(self, tren):
        print(f"El tren {tren.nombre} ha llegado a {self.nombre}.")

    def salida_tren(self, tren):
        print(f"El tren {tren.nombre} ha salido de {self.nombre}.")

    def agregar_persona(self, persona):
        self.personas_esperando.append(persona)
        print(f"La persona {persona.id_persona} espera en {self.nombre}.")
