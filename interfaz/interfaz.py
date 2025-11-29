import tkinter as tk
from tkinter import ttk, messagebox
from .funciones import crear_ventanas, guardar_simulacion, cerrar_ventana
from config.colores import color_bg_principal
from .listado import ventana_listado_simulaciones
from logica.cargarguardar import escribir_archivo_csv

rutas_guardadas = []

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

    # Preguntara el nombre de la simulacion
    tk.Label(frame, text="Ingrese el nombre de la simulación", bg=color_bg_principal).pack()
    nombre = tk.Entry(frame)
    nombre.pack()
    rutas_temporales = []

    # Crearemos 3 espacios para agregar la hora los minutos y los segundos
    tk.Label(frame, text="Ingrese la hora de inicio (hora/minutos/segundos)", bg=color_bg_principal).pack()
    hora = tk.Entry(frame, width=10)
    hora.pack()
    minutos = tk.Entry(frame, width=10)
    minutos.pack()
    segundos = tk.Entry(frame, width=10)
    segundos.pack()

    #Creamos el boton rutas
    tk.Button(frame, text="rutas", 
              command=lambda: ventana_rutas(rutas_temporales, rutas_guardadas)).pack()
    print(rutas_guardadas)   

    # Este boton guardara la simulación
    tk.Button(frame, text="Guardar", 
              command=lambda: guardar_simulacion(nombre, frame, tabs, hora, minutos, segundos, rutas_guardadas)).pack()   
    
    # este boton cancelara el proceso y cerrara la ventana
    tk.Button(frame, text="Cancelar", command=lambda: cerrar_ventana(frame, tabs)).pack()

    # retornamos el nombre que tendra la ventana
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


def ventana_rutas(lista_temporal:list, lista_real:list):
    """ Esta funcion creara una ventana que creara las rutas y las mostrara"""

    #Generamos una ventana perteneciente a la ventana original
    ventana = tk.Toplevel()
    ventana.title("Gestion de Rutas")
    ventana.geometry("800x600")

    # Generamos y configuramos un canva para el listado de rutas
    canvas = tk.Canvas(ventana)
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Botones
    botones_frame = tk.Frame(ventana)
    botones_frame.pack(fill="x", pady=5)

    tk.Button(
        botones_frame,
        text="Agregar ruta",
        command=lambda: agregar_ruta(scrollable_frame, lista_temporal)
    ).pack(side="left", padx=10)

    tk.Button(
        botones_frame,
        text="Guardar",
        command=lambda: guardar_datos(ventana, lista_temporal, lista_real)
    ).pack(side="right", padx=10) 
    
    tk.Button(
        botones_frame,
        text="Cancelar",
        command=lambda: cancelar(ventana)).pack(side="right", padx=10) 

    # Vemos las rutas que ya habian
    mostrar_rutas(scrollable_frame, lista_real)

def agregar_ruta(frame:tk.Frame, lista_temporal:list, origen_val="",destino_val="", km_val = "", ):
    """ Esta funcion crea frames que serviran de contenedores"""
    lista_para_la_lista = []
    # Creamos los contenedores y sus entrys
    frame_ruta = tk.Frame(frame, bg="#f5f5f5", relief="solid", bd=1, padx=5, pady=5)
    frame_ruta.pack(fill="x", pady=5, padx=10)

    # Entradas
    tk.Label(frame_ruta, text="Origen:").grid(row=0, column=0, padx=5, pady=2)
    entry_origen = tk.Entry(frame_ruta, width=15)
    entry_origen.grid(row=0, column=1, padx=5)
    entry_origen.insert(0, origen_val)

    tk.Label(frame_ruta, text="Destino:").grid(row=0, column=2, padx=5, pady=2)
    entry_destino = tk.Entry(frame_ruta, width=15)
    entry_destino.grid(row=0, column=3, padx=5)
    entry_destino.insert(0, destino_val)

    tk.Label(frame_ruta, text="Km:").grid(row=0, column=4, padx=5, pady=2)
    entry_km = tk.Entry(frame_ruta, width=8)
    entry_km.grid(row=0, column=5, padx=5)
    entry_km.insert(0, km_val)

    # Botón para eliminar
    tk.Button(
        frame_ruta,
        text="Eliminar",
        command=lambda: eliminar_ruta(frame_ruta, lista_para_la_lista, (entry_origen, entry_destino, entry_km)),
        bg="#ffcccc"
    ).grid(row=0, column=6, padx=10)
    lista_temporal.append(entry_origen) 
    lista_temporal.append(entry_destino) 
    lista_temporal.append(entry_km)

def eliminar_ruta(frame:tk.Frame, lista:list, tres_entrys):
    if messagebox.askyesno("Eliminar ruta", "¿Deseas eliminar esta ruta?"):
        frame.destroy()
        if tres_entrys in lista:
            lista.remove(tres_entrys)

def guardar_datos(ventana:tk.Toplevel, lista:list[tk.Entry], lista_real:list) :
    """
    Esta función recoge lo que halla en los entrys y lo almecena en una lista que viene desde lo mas arriba del programa
    lista: recive los entrys y los almacena
    lista_real: es la lista es la lista en la que quiero que se guarden los datos filtrados ej: [[o,d,1]]"""

    lista_temporal = []
    if len(lista)==0:
        return None
    
    for i in range(len(lista[0:3])):
        # Si el elemento ya no existe o fue destruido, lo ignoramos
        if isinstance(lista[i], tk.Entry):
            try:
                lista_temporal.append(lista[i].get())
            except tk.TclError:
                continue  # el Entry ya fue destruido
        else:
            lista_temporal.append(str(lista[i]))

    if not lista_temporal:
        messagebox.showwarning("Error", "No se han ingresado datos")
        return

    lista_real.append(lista_temporal)
    guardar_datos(ventana, lista[3:], lista_real)
    print(lista_real)
    messagebox.showinfo("Guardado", "Rutas guardadas correctamente.")
    ventana.destroy()

def cancelar(nueva_ventana:tk.Toplevel):
    """Cierra la ventana sin guardar"""
    if messagebox.askyesno("Cancelar", "¿Deseas cerrar sin cambiar nada?"):
        nueva_ventana.destroy()

def mostrar_rutas(ventana:tk.Frame, lista:list[list[str]]):
    for o,d,k in lista:
        frame = tk.Frame(ventana, bg="#ffffff")
        frame.pack(fill="x",pady=5, padx=10)
        tk.Label(frame, text=f"{o}---->{d}", bg="#fff4b9").pack()