import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import time

# --------------------------
# Datos base (como antes)
# --------------------------
STATION_ORDER = ["Estación Central", "Rancagua", "Talca", "Chillán"]

STATIONS = {
    "Estación Central": {"pos": (100, 260), "pob": 8242459, "dist": {"Rancagua": 87, "Chillán": 350}},
    "Rancagua": {"pos": (300, 260), "pob": 274407, "dist": {"Estación Central": 87, "Talca": 200}},
    "Talca": {"pos": (500, 260), "pob": 242344, "dist": {"Rancagua": 200, "Chillán": 180}},
    "Chillán": {"pos": (700, 260), "pob": 204091, "dist": {"Talca": 180, "Estación Central": 350}},
}

TRAINS = {
    "BMU (Bimodal)": {"vel": 160, "cap": 236, "color": "#FF5555"},
    "EMU EFE-SUR": {"vel": 120, "cap": 200, "color": "#66FF66"},
}

# --------------------------
# Utilidades de ruta
# --------------------------
def build_route(start_name, end_name):
    """Devuelve la lista de estaciones (names) de start->end siguiendo STATION_ORDER."""
    idx_s = STATION_ORDER.index(start_name)
    idx_e = STATION_ORDER.index(end_name)
    if idx_s <= idx_e:
        return STATION_ORDER[idx_s:idx_e+1]
    else:
        # reverse direction
        return STATION_ORDER[idx_s:idx_e-1:-1]  # slice descending

def route_distance_km(route):
    total = 0
    for i in range(len(route)-1):
        a = route[i]
        b = route[i+1]
        d = STATIONS[a]["dist"].get(b) or STATIONS[b]["dist"].get(a)
        if d:
            total += d
    return total

# --------------------------
# Clase Person (visual)
# --------------------------
class PersonVisual:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = 6
        self.color = color
        self.id = canvas.create_oval(x-self.r, y-self.r, x+self.r, y+self.r, fill=color, outline="")
        self.alive = True

    def move_towards(self, tx, ty, steps=20, step=0):
        if step >= steps:
            return
        dx = (tx - self.x) / (steps - step)
        dy = (ty - self.y) / (steps - step)
        self.canvas.move(self.id, dx, dy)
        self.x += dx
        self.y += dy
        # schedule next
        self.canvas.after(25, lambda: self.move_towards(tx, ty, steps, step+1))

    def remove(self):
        if self.alive:
            try:
                self.canvas.delete(self.id)
            except:
                pass
            self.alive = False

# --------------------------
# Clase TrainSprite (dibujo + lógica sencilla)
# --------------------------
class TrainSprite:
    def __init__(self, canvas, x, y, color, capacity):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.capacity = capacity
        self.passengers = random.randint(10, int(capacity*0.4))
        self.flow = 0
        self.width = 90
        self.height = 36
        self.group = []
        # draw body
        self.body = canvas.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height,
                                            fill=self.color, outline="#222", width=2)
        # windows
        for i in range(3):
            wx = self.x + 12 + i*24
            self.group.append(canvas.create_rectangle(wx, self.y+8, wx+14, self.y+22, fill="#222222"))
        # label text on body
        self.label = canvas.create_text(self.x + self.width/2, self.y + self.height/2, text="TREN", fill="#111",
                                        font=("Helvetica", 10, "bold"))

    def coords(self):
        return self.canvas.coords(self.body)  # x1,y1,x2,y2

    def move(self, dx, dy):
        self.canvas.move(self.body, dx, dy)
        for g in self.group:
            self.canvas.move(g, dx, dy)
        self.canvas.move(self.label, dx, dy)

    def set_position(self, x, y):
        # move absolute (compute delta)
        x1, y1, x2, y2 = self.coords()
        cur_x = x1
        cur_y = y1
        dx = x - cur_x
        dy = y - cur_y
        self.move(dx, dy)

    def remove(self):
        for g in self.group:
            try: self.canvas.delete(g)
            except: pass
        try: self.canvas.delete(self.body)
        except: pass
        try: self.canvas.delete(self.label)
        except: pass

# --------------------------
# App principal (estética panel ferroviario)
# --------------------------
class TrainApp:
    def __init__(self, root):
        self.root = root
        root.title("Simulación EFE — Panel Ferroviario")
        root.geometry("1024x540")
        root.configure(bg="#081013")  # dark panel background

        # UI frames
        self.left_frame = tk.Frame(root, bg="#071012")
        self.left_frame.place(x=8, y=8, width=300, height=524)

        self.center_frame = tk.Frame(root, bg="#071012")
        self.center_frame.place(x=320, y=8, width=696, height=524)

        self.build_left_panel()
        self.build_center_canvas()

        # State
        self.current_train = None
        self.current_route = []
        self.train_sprite = None
        self.persons = []  # active person visuals
        self.running = False

    # -------------------------
    def build_left_panel(self):
        # Title
        title = tk.Label(self.left_frame, text="EFE Sim Panel", bg="#081013", fg="#9EFF7A",
                         font=("Orbitron", 14, "bold"))
        title.pack(pady=(10,6))

        # Selectors
        lbl1 = tk.Label(self.left_frame, text="Estación inicio", bg="#071012", fg="#9EFF7A")
        lbl1.pack(anchor="w", padx=12, pady=(8,0))
        self.start_cb = ttk.Combobox(self.left_frame, values=list(STATIONS.keys()), state="readonly")
        self.start_cb.pack(fill="x", padx=12)

        lbl2 = tk.Label(self.left_frame, text="Estación destino", bg="#071012", fg="#9EFF7A")
        lbl2.pack(anchor="w", padx=12, pady=(8,0))
        self.end_cb = ttk.Combobox(self.left_frame, values=list(STATIONS.keys()), state="readonly")
        self.end_cb.pack(fill="x", padx=12)

        lbl3 = tk.Label(self.left_frame, text="Tipo de tren", bg="#071012", fg="#9EFF7A")
        lbl3.pack(anchor="w", padx=12, pady=(8,0))
        self.train_cb = ttk.Combobox(self.left_frame, values=list(TRAINS.keys()), state="readonly")
        self.train_cb.pack(fill="x", padx=12)

        # Buttons
        btn_frame = tk.Frame(self.left_frame, bg="#071012")
        btn_frame.pack(fill="x", pady=12, padx=12)
        start_btn = tk.Button(btn_frame, text="Iniciar", bg="#143F13", fg="#E8FFE8", command=self.start_simulation)
        start_btn.pack(side="left", expand=True, fill="x", padx=(0,6))
        stop_btn = tk.Button(btn_frame, text="Detener", bg="#401313", fg="#FFDADA", command=self.stop_simulation)
        stop_btn.pack(side="left", expand=True, fill="x", padx=(6,0))

        # Info area
        info_title = tk.Label(self.left_frame, text="Información", bg="#081013", fg="#9EFF7A", font=("Helvetica", 11, "bold"))
        info_title.pack(pady=(8,4))
        self.info_text = tk.Text(self.left_frame, height=10, bg="#071012", fg="#CFFFCF", bd=0)
        self.info_text.pack(fill="both", padx=12, pady=(0,12))
        self.info_text.insert(tk.END, "Seleccione y pulse Iniciar.\n")
        self.info_text.configure(state="disabled")

        # Log area
        log_label = tk.Label(self.left_frame, text="Logs", bg="#071012", fg="#9EFF7A")
        log_label.pack(anchor="w", padx=12)
        self.log_box = tk.Text(self.left_frame, height=6, bg="#000", fg="#9EFF7A", bd=0)
        self.log_box.pack(fill="both", padx=12, pady=6)

    # -------------------------
    def build_center_canvas(self):
        # canvas look
        self.canvas = tk.Canvas(self.center_frame, width=680, height=500, bg="#0B0F0B", highlightthickness=0)
        self.canvas.pack(padx=8, pady=8)
        self.draw_base_map()

    def draw_base_map(self):
        # draw "track" lines and station nodes
        for i, name in enumerate(STATION_ORDER):
            x, y = STATIONS[name]["pos"]
            # line between this and next
            if i < len(STATION_ORDER)-1:
                nx, ny = STATIONS[STATION_ORDER[i+1]]["pos"]
                self.canvas.create_line(x, y, nx, ny, fill="#1E8F1E", width=6, capstyle="round")
        # stations
        for name in STATION_ORDER:
            x, y = STATIONS[name]["pos"]
            # dark ring + bright dot
            self.canvas.create_oval(x-16, y-16, x+16, y+16, fill="#062006", outline="#083708", width=2)
            self.canvas.create_oval(x-8, y-8, x+8, y+8, fill="#9EFF7A", outline="")
            self.canvas.create_text(x, y+28, text=name, fill="#CFFFCF", font=("Helvetica", 9))

    # -------------------------
    def log(self, txt):
        ts = time.strftime("%H:%M:%S")
        self.log_box.insert(tk.END, f"[{ts}] {txt}\n")
        self.log_box.see(tk.END)

    def set_info(self, txt):
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, txt)
        self.info_text.configure(state="disabled")

    # -------------------------
    def start_simulation(self):
        start = self.start_cb.get()
        end = self.end_cb.get()
        train_key = self.train_cb.get()
        if not start or not end or not train_key:
            messagebox.showwarning("Falta selección", "Seleccione inicio, destino y tipo de tren.")
            return
        if start == end:
            messagebox.showwarning("Error", "Seleccione estaciones distintas.")
            return

        # build route
        route = build_route(start, end)
        total_km = route_distance_km(route)
        preset = TRAINS[train_key]

        # compute pixel per km: use pixel distance along canvas between start and end
        start_px = STATIONS[route[0]]["pos"]
        end_px = STATIONS[route[-1]]["pos"]
        canvas_px = math.hypot(end_px[0]-start_px[0], end_px[1]-start_px[1])
        px_per_km = canvas_px / total_km if total_km > 0 else 4.0

        # map speed km/h -> px per tick (tick=50ms)
        speed_px_per_sec = (preset["vel"] * px_per_km) / 3600.0
        speed_px_per_tick = speed_px_per_sec * 0.05  # 50ms tick

        # save state
        self.current_train = {
            "key": train_key,
            "preset": preset,
            "route": route,
            "total_km": total_km,
            "px_per_km": px_per_km,
            "speed_px_tick": speed_px_per_tick,
            "start_px": start_px,
            "end_px": end_px,
        }

        # display info
        info = (f"Tren: {train_key}\nCapacidad: {preset['cap']}\nRuta: {' -> '.join(route)}\nDistancia: {total_km} km\n"
                f"Vel: {preset['vel']} km/h")
        self.set_info(info)
        self.log(f"Iniciada ruta {route[0]} -> {route[-1]} | Dist {total_km} km")

        # create sprite at route[0] pos
        self.spawn_train_at_station(route[0], preset)
        self.running = True
        # simulation pointers
        self.route_idx = 0
        self.target_idx = 1 if len(route) > 1 else 0
        self.step_along_segment = 0.0

        # start main loop
        self.root.after(50, self.simulation_tick)

    def spawn_train_at_station(self, station_name, preset):
        # remove existing
        if self.train_sprite:
            self.train_sprite.remove()
        x, y = STATIONS[station_name]["pos"]
        # position train with offset above the track
        self.train_sprite = TrainSprite(self.canvas, x-45, y-22, preset["color"], preset["cap"])

    def simulation_tick(self):
        if not self.running:
            return
        # move train along route
        cur_route = self.current_train["route"]
        if self.route_idx >= len(cur_route)-1:
            # reached final station
            self.running = False
            self.log("Tren llegó a destino final.")
            messagebox.showinfo("Llegada", "El tren ha llegado a su destino final.")
            return

        a = cur_route[self.route_idx]
        b = cur_route[self.route_idx+1]
        ax, ay = STATIONS[a]["pos"]
        bx, by = STATIONS[b]["pos"]

        # normalized direction vector
        seg_len_px = math.hypot(bx-ax, by-ay)
        if seg_len_px == 0:
            return
        dir_x = (bx-ax)/seg_len_px
        dir_y = (by-ay)/seg_len_px

        # move by speed per tick
        spx = self.current_train["speed_px_tick"]
        self.train_sprite.move(dir_x*spx, dir_y*spx)
        self.step_along_segment += spx

        # check if reached or passed the breakpoint
        if self.step_along_segment + 1.0 >= seg_len_px:
            # snap to station b position (place train slightly left to center)
            new_x = bx - (self.train_sprite.width/2)
            new_y = by - (self.train_sprite.height/2)
            self.train_sprite.set_position(new_x, new_y)
            # perform station stop: boarding / leaving
            self.on_arrive_station(b)
            # advance indices
            self.route_idx += 1
            self.target_idx = min(self.route_idx+1, len(cur_route)-1)
            # reset step
            self.step_along_segment = 0.0
            # short dwell time: pause before moving (simulate stop)
            self.root.after(900, self.simulation_tick)  # 900 ms stop
            return

        # continue moving next tick
        self.root.after(50, self.simulation_tick)

    def on_arrive_station(self, station_name):
        # simulate people leaving and boarding (numbers)
        leaving = random.randint(0, min(20, self.train_sprite.passengers))
        boarding = random.randint(0, 30)
        # animate leaving: create small persons near train and move outwards
        tx1, ty1, tx2, ty2 = self.train_sprite.coords()
        train_center_x = (tx1 + tx2)/2
        train_center_y = (ty1 + ty2)/2

        # leaving: animate persons moving downward away from train
        for i in range(leaving):
            px = train_center_x - 20 + i*6
            py = train_center_y + 30
            p = PersonVisual(self.canvas, train_center_x, train_center_y+10, color="#FFE06A")
            # move outward (down-left or down-right)
            tx = px + random.uniform(-40, -10)
            ty = py + random.uniform(20, 50)
            p.move_towards(tx, ty, steps=18)
            self.canvas.after(800, p.remove)
            self.persons.append(p)

        # adjust passengers
        self.train_sprite.passengers = max(0, self.train_sprite.passengers - leaving)

        # boarding: create persons at station and animate towards train
        sx, sy = STATIONS[station_name]["pos"]
        for i in range(boarding):
            sx_off = sx - 30 + random.uniform(-6, 6) + (i%6)*6
            sy_off = sy + 18 + random.uniform(-4, 6)
            p = PersonVisual(self.canvas, sx_off, sy_off, color=random.choice(["#78D6FF", "#FFB78A", "#B8FF9E"]))
            # animate to train center
            p.move_towards(train_center_x, train_center_y, steps=18)
            # schedule removal after arrival and increment passengers
            self.canvas.after(700, p.remove)
            self.persons.append(p)

        # update internal counts
        self.train_sprite.passengers = min(self.train_sprite.capacity, self.train_sprite.passengers + boarding)
        self.train_sprite.flow += boarding

        # update info & logs
        self.log(f"Llegada a {station_name}: -{leaving} bajan, +{boarding} suben. A bordo: {self.train_sprite.passengers}")
        self.update_info_panel()

    def update_info_panel(self):
        if not self.current_train or not self.train_sprite:
            return
        k = self.current_train["key"]
        cap = self.current_train["preset"]["cap"]
        text = (f"Tren: {k}\nCapacidad: {cap}\nPasajeros a bordo: {self.train_sprite.passengers}\n"
                f"Flujo acumulado: {self.train_sprite.flow}\nRuta: {' -> '.join(self.current_train['route'])}\n"
                f"Distancia: {self.current_train['total_km']} km\nVel px/km: {self.current_train['px_per_km']:.2f}")
        self.set_info(text)

    def stop_simulation(self):
        self.running = False
        if self.train_sprite:
            self.train_sprite.remove()
            self.train_sprite = None
        # remove persons
        for p in self.persons:
            p.remove()
        self.persons = []
        self.log("Simulación detenida.")
        self.set_info("Simulación detenida. Seleccione nuevas opciones para reiniciar.")

# --------------------------
# Ejecutar app
# --------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TrainApp(root)
    # fix: set initial selections default for convenience
    app.start_cb.set("Estación Central")
    app.end_cb.set("Chillán")
    app.train_cb.set(list(TRAINS.keys())[0])
    root.mainloop()