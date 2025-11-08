import tkinter as tk
import os 

def carpetas_en() -> list:
    carpetas = []
    ruta = "simulaciones"
    for carpeta in os.listdir(ruta):
        if os.path.isdir(os.path.join(ruta, carpeta)):
            carpetas.append(carpeta)
    
    return carpetas