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
    

def crear_carpeta(nombre:str) -> str:
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
        return carpeta_destino
    
    except Exception as e:
            print("Error al guardar la simulación:", e)


def crear_archivo(carpeta:str, nombre:str, tipo:str) -> str:
    """ esta funcion creara archivos de la siguiente manera nombre.tipo y retornara la ruta generada"""

    try:
        arch = f"{carpeta}/{nombre}.{tipo}"
        with open(arch, "x") as archivo:
            return arch
    except FileExistsError:
        pass

def leer_archivo(ruta:str) -> list[str]:
    """ Esta función leera los datos dentro de los archivos y los regresara como str en una lista"""

    with open(ruta, "r") as archivo:
        contenido = archivo.readlines()
    
    return contenido

def escribir_archivo_csv(ruta:str, datos:list[list]):
    """ Esta funcion se encargara de escribir los datos en la direccion que le hallamos pasado """
    with open(ruta, "w") as archivo:
        for fila in datos:
            linea = "j".join(map(str, fila))
            archivo.write(linea +"\n")

#carpeta = crear_carpeta("hola")
#crear_archivo(carpeta,"adios", "csv")
