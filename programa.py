import tkinter as tk
from tkinter import ttk
from config.configuraciones import titulo_ventana
from interfaz.interfaz import interfaze, ventana_simulador, ventana_creacion_simulacion, crear_ventanas

def main():
    """Inicia el programa completo"""
    #configuración de la ventana
    ventana = tk.Tk() 
    ventana.state("zoomed")
    ventana.title(titulo_ventana)

    #Creamos la interfaz
    interfaze(ventana)

    #Creación del bucle
    tk.mainloop()
if __name__ == "__main__":
    main()
