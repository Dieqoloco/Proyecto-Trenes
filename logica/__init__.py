from .guardar import crear_carpeta
from .cargar import carpetas_en

__all__ = [
    "crear_carpeta",
    "carpetas_en"
]


"""Esto de la clases lo deje un poco avanzado"""
class Estacion:
    def __init__(self, id, nombre, poblacion, vias):
        self.id = id #número identificador, número de la estación
        self.nombre = nombre #nombre de la estación
        self.poblacion = poblacion # Cantidad total de habitantes en la ciudad que se encuentra
        self.vias = vias #vias disponibles 
        self.flujo = 0 # Cantidad acumuladad de personas que pasan por la estación


class Ruta:
    def __init__(self, origen, destino, distancia):
        self.origen = origen 
        self.destino = destino
        self.distancia = distancia

class Tren:
    def __init__(self, id, nombre, velocidad, capacidad_total):
        self.id = id
        self.nombre = nombre 
        self.velocidad = velocidad #velocidad del tren
        self.capacidad_total = capacidad_total
        self.posicion = None  # estación donde inicia
