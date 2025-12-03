# sim_trenes_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import time

# -------------------------
# Datos base (posiciones en canvas y poblaciones)
# -------------------------
STATIONS = [
    ("Santiago", 100, 250, 8242459),
    ("Rancagua", 300, 250, 274407),
    ("Talca",   500, 250, 242344),
    ("Chillán", 700, 250, 204091),
]

# conexiones con distancia (km) - orientativo
CONNECTIONS = {
    ("Santiago", "Rancagua"): 87,
    ("Rancagua", "Talca"): 200,
    ("Talca", "Chillán"): 180,
    ("Chillán", "Santiago"): 360,  # vuelta larga
}

# Trenes preset
TRAINS_PRESET = {
    "BMU (Bimodal) – 160 km/h": {"vel": 160, "cap": 236, "energia": "Eléctrico/Diésel", "color": "red"},
    "EMU EFE Sur – 120 km/h":    {"vel": 120, "cap": 200, "energia": "Eléctrico", "color": "green"},
}

# Rutas seleccionables (nombre, start_index, end_index)
ROUTES = [
    ("Santiago → Rancagua", 0, 1),
    ("Rancagua → Talca", 1, 2),
    ("Talca → Chillán", 2, 3),
    ("Santiago → Chillán", 0, 3),
]


# -------------------------
# Clase TrainVisual: representa un tren en el canvas
# -------------------------
class TrainVisual:
    def __init__(self, canvas, name, preset, start_pos, end_pos):
        self.canvas = canvas
        self.name = name
        self.vel_kmh = preset["vel"]
        self.capacity = preset["cap"]
        self.energia = preset["energia"]
        self.color = preset.get("color", "blue")
        self.occupancy = random.randint(10, int(self.capacity * 0.5))
        self.flow = 0  # pasajeros acumulados embarcados

        # posiciones (float para movimiento suave)
        self.x, self.y = float(start_pos[0]), float(start_pos[1])
        self.start_pos = start_pos
        self.end_pos = end_pos

        # dibujar
        self.size = 14
        self.shape = self.canvas.create_rectangle(self.x-self.size, self.y-self.size,
                                                  self.x+self.size, self.y+self.size,
                                                  fill=self.color)
        self.label = self.canvas.create_text(self.x, self.y - 20, text=self.name, font=("Arial", 10))
        self.at_station = True

        # cálculo de movimiento: velocidad en px/seg según distancia px <-> km
        # definimos escala: px_per_km ≈ (canvas distance in px) / (real km)
        self.px_per_km = self.compute_px_per_km()
        self.speed_px_per_sec = (self.vel_kmh * self.px_per_km) / 3600.0  # km/h -> px/s

        # tiempo restante para llegar (s)
        self.total_distance_px = math.hypot(self.end_pos[0]-self.x, self.end_pos[1]-self.y)
        self.move_dx = 0
        self.move_dy = 0
        if self.total_distance_px > 0:
            self.move_dx = (self.end_pos[0]-self.x) / (self.total_distance_px)
            self.move_dy = (self.end_pos[1]-self.y) / (self.total_distance_px)

    def compute_px_per_km(self):
        # Elegimos una aproximación: promedio de distancias y km entre estaciones "vecinas"
        # Si las estaciones están en línea horizontal, tomamos la conexión más cercana
        # Aquí simplificamos: buscamos una conexión conocida entre start and end (por nombre)
        # Fallback: usar 3 px/km como mínimo para no tener velocidades cero.
        return 3.0

    def step(self, dt, others):
        """
        dt: segundos transcurridos desde el último paso
        others: lista de otros TrainVisual para evitar colisiones (simple)
        """
        # Evitar colisión simple: si hay otro tren muy cerca en la dirección al que vamos, frenar (no mover)
        for o in others:
            if o is not self:
                dist = math.hypot((o.x - self.x), (o.y - self.y))
                if dist < 30:
                    # detenerse para evitar choque
                    return

        # mover según velocidad
        move_amount = self.speed_px_per_sec * dt
        # si ya estamos casi en el destino
        remaining = math.hypot(self.end_pos[0]-self.x, self.end_pos[1]-self.y)
        if remaining <= move_amount:
            # llegar al destino: fijar coordenadas finales y marcar arrived
            self.x, self.y = float(self.end_pos[0]), float(self.end_pos[1])
            self.canvas.coords(self.shape, self.x-self.size, self.y-self.size, self.x+self.size, self.y+self.size)
            self.canvas.coords(self.label, self.x, self.y-20)
            self.arrive_at_station()
            return

        # movimiento normal
        self.x += self.move_dx * move_amount
        self.y += self.move_dy * move_amount
        self.canvas.coords(self.shape, self.x-self.size, self.y-self.size, self.x+self.size, self.y+self.size)
        self.canvas.coords(self.label, self.x, self.y-20)

    def arrive_at_station(self):
        # Simular subida/bajada y flujo
        boarding = random.randint(0, 30)
        leaving = random.randint(0, 20)
        self.occupancy = max(0, min(self.capacity, self.occupancy + boarding - leaving))
        self.flow += boarding
        # marcar que llegó (se podría invertir dirección o decidir siguiente tramo)
        self.at_station = True


# -------------------------
# Clase principal: GUI y lógica
# -------------------------
class TrainSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación EFE - Selección y Animación")
        self.root.geometry("980x520")
        self.root.resizable(False, False)

        self.selected_train_key = tk.StringVar()
        self.selected_route_key = tk.StringVar()

        # Selección frame
        self.create_selection_frame()

        # Variables para simulación
        self.canvas = None
        self.trains_visual = []
        self.running = False
        self.last_time = None

    def create_selection_frame(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.place(x=10, y=10, width=300, height=200)

        ttk.Label(frame, text="Selecciona un tren:").pack(anchor="w")
        train_combo = ttk.Combobox(frame, values=list(TRAINS_PRESET.keys()), textvariable=self.selected_train_key, state="readonly")
        train_combo.pack(fill="x", pady=6)

        ttk.Label(frame, text="Selecciona una ruta:").pack(anchor="w", pady=(6, 0))
        route_combo = ttk.Combobox(frame, values=[r[0] for r in ROUTES], textvariable=self.selected_route_key, state="readonly")
        route_combo.pack(fill="x", pady=6)

        # Botones
        start_btn = ttk.Button(frame, text="Iniciar simulación", command=self.on_start)
        start_btn.pack(pady=(10, 2), fill="x")

        stop_btn = ttk.Button(frame, text="Detener / Reset", command=self.on_stop)
        stop_btn.pack(pady=2, fill="x")

        # Log area (mini)
        self.log_box = tk.Text(self.root, width=34, height=18)
        self.log_box.place(x=10, y=220)

    def log(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    def on_start(self):
        train_key = self.selected_train_key.get()
        route_key = self.selected_route_key.get()
        if not train_key or not route_key:
            messagebox.showwarning("Falta selección", "Selecciona un tren y una ruta antes de iniciar.")
            return

        # preparar canvas si no existe
        if self.canvas is None:
            self.create_canvas()

        # limpiar cualquier tren previo
        for tv in self.trains_visual:
            self.canvas.delete(tv.shape)
            self.canvas.delete(tv.label)
        self.trains_visual = []

        # obtener indices de ruta
        route = next(r for r in ROUTES if r[0] == route_key)
        _, start_idx, end_idx = route

        start_station = STATIONS[start_idx]
        end_station = STATIONS[end_idx]

        start_pos = (start_station[1], start_station[2])
        end_pos = (end_station[1], end_station[2])

        preset = TRAINS_PRESET[train_key]
        tv = TrainVisual(self.canvas, train_key, preset, start_pos, end_pos)
        self.trains_visual.append(tv)

        # mostrar info y log
        info_text = f"Tren: {train_key} | Capacidad: {preset['cap']} | Energía: {preset['energia']}"
        self.log(info_text)
        self.log(f"Iniciando ruta: {route_key}  ({start_station[0]} -> {end_station[0]})")

        # iniciar loop de animación
        self.running = True
        self.last_time = time.time()
        self.root.after(20, self.animation_step)

    def on_stop(self):
        # detener y limpiar
        self.running = False
        if self.canvas:
            # opcional: limpiar trenes
            for tv in self.trains_visual:
                self.canvas.delete(tv.shape)
                self.canvas.delete(tv.label)
            self.trains_visual = []
        self.log("Simulación detenida / reseteada.")

    def create_canvas(self):
        # Crear área de mapa (si ya existe, no crear)
        if self.canvas is not None:
            return
        self.canvas = tk.Canvas(self.root, width=640, height=480, bg="white")
        self.canvas.place(x=330, y=10)
        # dibujar vías y estaciones
        self.draw_map()

    def draw_map(self):
        # dibuja conexiones directas (líneas) - usamos la secuencia STATIONS ordenada
        for i in range(len(STATIONS)-1):
            x1, y1 = STATIONS[i][1], STATIONS[i][2]
            x2, y2 = STATIONS[i+1][1], STATIONS[i+1][2]
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=5)

        # dibuja estaciones con texto
        for name, x, y, pop in STATIONS:
            self.canvas.create_oval(x-12, y-12, x+12, y+12, fill="lightblue", outline="black")
            self.canvas.create_text(x, y-25, text=name, font=("Arial", 10, "bold"))
            self.canvas.create_text(x, y+25, text=f"Pob: {pop}", font=("Arial", 8))

    def animation_step(self):
        if not self.running:
            return
        now = time.time()
        dt = now - self.last_time if self.last_time else 0.02
        self.last_time = now

        # actualizar cada tren visual
        for tv in list(self.trains_visual):
            others = self.trains_visual
            tv.step(dt, others)

        # repetir
        self.root.after(20, self.animation_step)


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TrainSimulatorApp(root)
        root.mainloop()
    except Exception as e:
        # si falla al ejecutarse, mostrar detalle
        import traceback
        traceback.print_exc()
        messagebox.showerror("Error al ejecutar", str(e))