from tkinter import messagebox, Toplevel, Label
import tkinter as tk

hora = 0
minuto = 0
segundo = 0
label = None


def configurar_hora(h, m, s):
    global hora, minuto, segundo
    hora = h
    minuto = m
    segundo = s


def validar_y_guardar_hora(h, m, s):
    try:
        h = int(h)
        m = int(m)
        s = int(s)
    except ValueError:
        return False

    if 0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60:
        configurar_hora(h, m, s)
        return True

    return False


def confirmar_y_iniciar_simulacion(e_hora, e_min, e_seg, ventana_config):
    h = e_hora.get()
    m = e_min.get()
    s = e_seg.get()

    if validar_y_guardar_hora(h, m, s):
        ventana_config.destroy()

        ventana_sim = Toplevel()
        ventana_sim.title("Simulación de Trenes")
        ventana_sim.geometry("800x600")

        label_hora = Label(ventana_sim, font=("Arial", 12))
        label_hora.place(x=10, y=10)
        iniciar_reloj(label_hora, ventana_sim)

    else:
        messagebox.showerror("Error", "Ingrese valores válidos (0–23 / 0–59)")


def iniciar_reloj(label_widget, ventana):
    global label
    label = label_widget
    actualizar_reloj(ventana)


def actualizar_reloj(ventana):
    global hora, minuto, segundo, label

    label.config(text=f"{hora:02}:{minuto:02}:{segundo:02}")

    segundo += 1
    if segundo >= 60:
        minuto += 1
        segundo = 0
    if minuto >= 60:
        hora += 1
        minuto = 0
    if hora >= 24:
        hora = 0

    ventana.after(1000, lambda: actualizar_reloj(ventana))
