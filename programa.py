import tkinter as tk
from tkinter import messagebox, ttk
from config.configuraciones import escala_ventana,titulo_ventana

def main():
    """Inicia el programa completo"""
    #configuración de la ventana
    ventana = tk.Tk() 
    ventana.geometry(escala_ventana)
    ventana.title(titulo_ventana)

    #Aqui agregar algo

    #Creación del bucle
    tk.mainloop()
if __name__ == "__main__":
    main()
