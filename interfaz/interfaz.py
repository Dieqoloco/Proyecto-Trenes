import tkinter as tk
from tkinter import ttk
from .funciones import crear_ventanas, guardar_simulacion, cerrar_ventana
from config.colores import color_bg_principal
from .listado import ventana_listado_simulaciones

def interfaze(ventana:tk.Tk) -> None:
    """Esta funcion se utilizara para crear la barra con la que se cambiaran las ventanas, 
    junto con el resto de la interfaz"""
    
    #este bloque crea el sistema de ventanas y dice como posicionarlo
    sistema_ventanas = ttk.Notebook(ventana)
    sistema_ventanas.pack(fill="both", expand=True)

    #ventana de Simulación
    Ventana_simulacion = tk.Frame(sistema_ventanas, bg=color_bg_principal)
    ventana_simulador(Ventana_simulacion, sistema_ventanas)


def ventana_creacion_simulacion(frame:tk.Frame, tabs: ttk.Notebook) -> str:
    """ Esta funcion creara la ventana creadora de simulaciones"""

    #Preguntara el nombre de la simulacion
    tk.Label(frame, text="Ingrese el nombre de la simulación", bg=color_bg_principal).pack()
    texto = tk.Entry(frame)
    texto.pack()

    #Botones
    #Este boton guardara la simulación
    tk.Button(frame, text="Guardar", 
              command=lambda: guardar_simulacion(texto, frame, tabs)).pack()
    
    #este boton cancelara el proceso y cerrara la ventana
    tk.Button(frame, text="Cancelar", command=lambda: cerrar_ventana(frame, tabs)).pack()

    #retornamos el nombre que tendra la ventana
    return "Crear Simulación"

def ventana_simulador(Frame:tk.Frame, tabs:ttk.Notebook) -> None:
    """Esta funcion creara la ventana inicio en el frame y agregara ese frame al notebook"""

    #Botones de esta ventana
    #Boton aun sin definir
    tk.Button(Frame, 
            text="Crear Simulación",
            command=lambda: crear_ventanas(tabs, ventana_creacion_simulacion)).pack()
    
    #Boton simulaciones
    tk.Button(Frame, text="Simulaciones",
              command=lambda: crear_ventanas(tabs, ventana_listado_simulaciones)).pack()    
    
    #agregamos las ventanas al sistema de ventanas, agrega el nombre a dicha ventana
    tabs.add(Frame, text="Inicio")   