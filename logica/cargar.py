import tkinter as tk
import os 
import shutil

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
