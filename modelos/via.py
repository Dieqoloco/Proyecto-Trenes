class Via:
    def __init__(self, id_via: str, origen, destino, longitud: float, orientacion: str = "N/A"):
        self.id_via = id_via
        self.origen = origen
        self.destino = destino
        self.longitud = longitud
        self.orientacion = orientacion
        self.ocupada = False

    def ocupar(self):
        self.ocupada = True
        print(f"La vía {self.id_via} está ocupada (de {self.origen.nombre} a {self.destino.nombre}).")

    def liberar(self):
        self.ocupada = False
        print(f"La vía {self.id_via} ha sido liberada.")
