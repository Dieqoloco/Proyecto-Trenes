import tkinter as tk
from tkinter import ttk, messagebox as msgbox
from .funciones import cerrar_ventana,crear_ventanas
from logica.cargarguardar import carpetas_en, eliminar_carpeta
from .simulacion import desplegarVentanaSimulacion

def ventana_listado_simulaciones(frame: tk.Frame, tab:ttk.Notebook) -> str:
    """Esta funcion creara la ventana que muestra la lista de simulaciones"""

    #definimos el ancho del frame
    ancho_frame = 400

    #Titulo de la ventana
    tk.Label(frame, text="Listado", anchor="center", font=("Arial", 32)).pack(fill="x")

    #creamos el frame scrolleable
    marco = tk.Frame(frame, bg="#fffd8d" )
    marco.pack(fill="y")

    #creamos el canva
    canvas = tk.Canvas(marco, width=ancho_frame, bg="#ffb7b7")
    canvas.pack(side="left", )

    #Creamos la barra de scroll
    barra_scroll = ttk.Scrollbar(marco, orient="vertical", command=canvas.yview)
    barra_scroll.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=barra_scroll.set)
    

    #frame donde iran los contenedores
    frame_interno = tk.Frame(canvas, bg="#e9ffb3")
    canvas.create_window((0, 0), window=frame_interno, anchor="nw")

    def actualizar_scroll(event):
    # Calcula el tamaño real de todo el contenido
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_interno.bind("<Configure>", actualizar_scroll)

    #creamos diccionario que usaremos mas adelante
    diccionario = dict()

    #creamos el bucle para generar frames por cada carpeta
    for i in carpetas_en():
        contenedor = tk.Frame(frame_interno, bg="white", width=ancho_frame, height=100, relief="solid",)
        contenedor.pack(padx=0, pady=0)
        contenedor.pack_propagate(False)
        contenedor_de_simulaciones(i, contenedor, tab, frame)
        diccionario[i] = contenedor

    #creamos un boton de cancelar en caso de no querer hacer nada con las simulaciones
    tk.Button(frame, text="Cancelar", command=lambda: cerrar_ventana(frame, tab)).pack()

    print(diccionario)

    return "Listado"

def contenedor_de_simulaciones(nombre, ventana, tab, frame):
    """ Esta funcion llenara contenedores con opciones para alterar los datos de la simulacion"""

    #Añadimos un label con el nombre de la simulacion
    tk.Label(ventana, text=nombre, font=("arial", 25)).pack()

    #hacemos un frame para agrupar de mejor manera los botones
    botones = tk.Frame(ventana)
    botones.pack()

    #creamos los botones
    tk.Button(botones, text="Empezar",
              command = lambda: desplegarVentanaSimulacion(ventana)).grid(row=0, column=1)
    tk.Button(botones, text="Modificar").grid(row=0, column=2)
    tk.Button(botones, text="Eliminar", 
              command = lambda: alerta_eliminacion(nombre, frame,tab)).grid(row=0, column=3)

def alerta_eliminacion(nombre:str, frame:tk.Frame, tab:ttk.Notebook):
    """Esta funcion saltara un mensaje confirmando que queremos eliminar la simulacion,
    en caso de que querramos eliminar la simulacion, lo hara y 'refrezcara' el tab"""

    if msgbox.askyesno("Eliminar", f"Seguro que desea elminar '{nombre}', por siempre y para siempre?"):
        eliminar_carpeta(nombre)
        cerrar_ventana(frame, tab)
        crear_ventanas(tab, ventana_listado_simulaciones)