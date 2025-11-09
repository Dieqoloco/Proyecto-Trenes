from trenes import Tren
from rutas_predefinidas import ruta_sur, ruta_norte

# Tren 1: BMU Bimodal
tren_bmu = Tren(
    nombre="Tren BMU (Bimodal)",
    velocidad=160,
    cantidad_vagones=4,
    ruta=ruta_sur
)

# Tren 2: EMU – EFE SUR
tren_emu = Tren(
    nombre="Tren EMU – EFE SUR",
    velocidad=120,
    cantidad_vagones=3,
    ruta=ruta_norte
)

TRENES = [tren_bmu, tren_emu]
