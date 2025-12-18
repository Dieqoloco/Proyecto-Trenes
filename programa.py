import tkinter as tk
from tkinter import ttk
from config.configuraciones import titulo_ventana
from interfaz.interfaz import interfaze

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