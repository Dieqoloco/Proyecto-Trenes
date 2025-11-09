from trenes_predefinidos import TRENES
from rutas_predefinidas import ESTACIONES

# Mostrar todas las estaciones
print("=== ESTACIONES ===")
for e in ESTACIONES:
    print(f"- {e.nombre} (Población: {e.poblacion_total})")

# Mostrar trenes y rutas
print("\n=== TRENES ===")
for t in TRENES:
    print(f"{t.nombre} | Velocidad: {t.velocidad} km/h | Ruta: {t.ruta.id_ruta}")

# Simulación simple
print("\nSimulación de prueba:")
tren = TRENES[0]
tren.mover()
