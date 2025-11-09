import tkinter as tk
import shutil
import os

def carpetas_en() -> list:
    """ Esta funcion extrae los nombres de las carpetas que estan dentro de la capeta simulaciones
    y las añade a una lista que despues retorna"""
    #creamos la carpeta
    carpetas = []

    #definimos la ruta
    ruta = "simulaciones"

    #acemos el bucle para que busque los nombres y los agrege a la lista
    for carpeta in os.listdir(ruta):
        if os.path.isdir(os.path.join(ruta, carpeta)):
            carpetas.append(carpeta)

    #devolvemos la lista con los nombres    
    return carpetas

def eliminar_carpeta(nombre:str):
    """ Esta funcion eliminara las carpetas que contengan los datos de las simulaciones"""
    shutil.rmtree("simulaciones/"+nombre)
    ruta = os.path.join("simulaciones", nombre)

    # Verificar que la carpeta exista antes de eliminar
    if not os.path.exists(ruta):
        print(f"La carpeta '{nombre}' no existe dentro de 'simulaciones'.")
        return False

    try:
        shutil.rmtree(ruta)
        print(f"Carpeta '{nombre}' eliminada correctamente.")
        return True
    except Exception as e:
        print(f"Error al eliminar la carpeta '{nombre}': {e}")
        return False

def crear_carpeta(nombre:str) -> None:
    """ Esta función servira para crear las carpetas con los datos de las simulaciones """
    "Si la carpeta no tiene nombre se guardara como 'Nueva simulación'"
    try:
        if nombre == "":
            nombre = "Nueva_Simulacion"
        # buscara la carpeta simulaciones y considerara la carpeta con nombre
        carpeta_destino = os.path.join("simulaciones", nombre) #
        # el bucle evitara errores por nombres duplicados
        contador = 0
        while os.path.exists(carpeta_destino):
            carpeta_destino = os.path.join("simulaciones", nombre + f"({contador})") 
            contador += 1

        os.makedirs(carpeta_destino)
    except Exception as e:
            print("Error al guardar la simulación:", e)
