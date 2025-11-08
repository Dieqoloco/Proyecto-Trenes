import tkinter as tk
import os

def crear_carpeta(nombre:str) -> None:
    """ Esta funcion servira para crear las carpetas con los datos de las simulaciones """

    "Si la carpeta no tiene nombre se guardara como 'Nueva simulación'"
    if nombre == "":
        nombre = "Nueva_Simulacion"

    # buscara la carpeta simulaciones y considerara la carpeta con nombre
    carpeta_destino = os.path.join("simulaciones", nombre)

    # el bucl evitara errores por nombres duplicados
    contador = 0
    while os.path.exists(carpeta_destino):
        carpeta_destino = os.path.join("simulaciones", nombre + f"({contador})")
        contador += 1
    os.makedirs(carpeta_destino)
