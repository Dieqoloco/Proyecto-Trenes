from estacion import Estacion
from entidades.via import Via
from entidades.ruta import Ruta

# === Estaciones ===
est_central = Estacion("Estación Central (Santiago)", 8242459)
rancagua = Estacion("Rancagua", 274407)
talca = Estacion("Talca", 242344)
chillan = Estacion("Chillán", 204091)

# === Vías (tramos entre estaciones) ===
via1 = Via("V1", est_central, rancagua, 87, "Sur")
via2 = Via("V2", rancagua, talca, 200, "Sur")
via3 = Via("V3", talca, chillan, 180, "Sur")

# Para conexiones de vuelta (si tu simulación lo permite)
via4 = Via("V4", chillan, est_central, 467, "Norte")

# === Rutas predefinidas ===
# Ruta 1: Santiago → Rancagua → Talca → Chillán
ruta_sur = Ruta(
    "RutaSur",
    [via1, via2, via3],
    [est_central, rancagua, talca, chillan]
)

# Ruta 2: Chillán → Santiago (trayecto inverso)
ruta_norte = Ruta(
    "RutaNorte",
    [via4],
    [chillan, est_central]
)

# Lista general para importar fácilmente
RUTAS = [ruta_sur, ruta_norte]
ESTACIONES = [est_central, rancagua, talca, chillan]
VIAS = [via1, via2, via3, via4]