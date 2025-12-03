import tkinter as tk
from tkinter import ttk
import math

def crear_via_curva(canvas, cx, cy, radio, ang_i, ang_f, pasos=50):
    puntos = []
    for i in range(pasos+1):
        ang = ang_i + (ang_f - ang_i) * i / pasos
        x = cx + radio * math.cos(math.radians(ang))
        y = cy + radio * math.sin(math.radians(ang))
        puntos.append((x, y))

    # dibujar segmentos
    for i in range(len(puntos)-1):
        x1, y1 = puntos[i]
        x2, y2 = puntos[i+1]
        canvas.create_line(x1, y1, x2, y2, width=3, fill="black")

    return puntos  # devolver los puntos para mover el tren más tarde

def desplegarVentanaSimulacion(vetana:tk.Tk):
    ventana_simulacion = tk.Toplevel(vetana)
    ventana_simulacion.title("Simulación")
    
    global mapa 
    mapa = tk.PhotoImage(file="mapa.png")
    canvas = tk.Canvas(ventana_simulacion, width=mapa.width(), height=mapa.height())
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=mapa)
    ventana_simulacion.geometry(f"{mapa.width()}x{mapa.height()}")

    puntos = crear_via_curva(canvas, 300, 300, 200, 0, 180)

    x = 100
    tren = canvas.create_rectangle(x, 200, x+20, 220, fill="blue")

