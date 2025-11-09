import tkinter as tk
from tkinter import ttk, messagebox as msgbox
from config.colores import color_bg_principal
from logica import crear_carpeta
 
    

def crear_ventanas(notebook:ttk.Notebook, funcion) -> None:
    """Crea tabs dependiendo de la función que se quiera crear"""

    #Crea el frame que se utilizara para hacer el tab
    nueva_ventana = tk.Frame(notebook, bg=color_bg_principal)

    #llama a la función que se quiera utilizar para definir la ventana que se creara
    funcion_y_nombre_ventana = funcion(nueva_ventana, notebook)

    #Despues de definir la ventana la agregaremos al notebook(sistema_de_ventanas)
    notebook.add(nueva_ventana, text=funcion_y_nombre_ventana)

    #el select cambie de la ventana principal a la nueva ventana
    notebook.select(nueva_ventana)


def guardar_simulacion(nombre:tk.Entry, frame: tk.Frame, tab: ttk.Notebook) -> None:
    """Esta funcion guardara la nueva simulación"""

    # esta funcion creara la carpeta en la que se guardaran los datos de la simulación
    contenido = nombre.get()
    crear_carpeta(contenido)

    # al finalizar cerraremos la ventana de creación
    cerrar_ventana(frame, tab)


def cerrar_ventana(frame:tk.Frame, tab: ttk.Notebook) -> None:
    """Funcion para cerrar tabs"""
    tab.forget(frame)

def main():
    #ventana = tk.Tk()
    #ventana.state("zoomed")
    #interfaz(ventana)
    #tk.mainloop()
    ...