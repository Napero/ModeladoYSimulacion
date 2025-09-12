# -*- coding: utf-8 -*-
"""
Simulador Interactivo Lagrange 1D con tabla de malla y cota teórica
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from math import factorial

# -------------------------
# Funciones base
# -------------------------

# Polinomio de Lagrange 1D
def Lagrange_poly_1D(x, x_nodos, y_nodos):
    n = len(x_nodos)
    L = np.zeros_like(x, dtype=float)
    for i in range(n):
        Li = np.ones_like(x, dtype=float)
        for j in range(n):
            if j != i:
                Li *= (x - x_nodos[j])/(x_nodos[i] - x_nodos[j])
        L += y_nodos[i]*Li
    return L

# Diferencias finitas 1D (aproximación derivada primera)
def deriv_fd_1D(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2*h)

# Error global teórico para Lagrange 1D
def error_teorico_1D(f_deriv_max, x_nodos, x_malla):
    n = len(x_nodos)-1
    prod_max = np.max([np.abs(np.prod([x - xi for xi in x_nodos])) for x in x_malla])
    return f_deriv_max/factorial(n+1) * prod_max

# -------------------------
# GUI Tkinter
# -------------------------
class SimuladorLagrangeTabla:
    def __init__(self, master):
        self.master = master
        master.title("Simulador Lagrange 1D con Tabla y Cota Teórica")

        # Entradas
        tk.Label(master, text="Función 1D (ej: np.exp)").grid(row=0, column=0)
        self.func_entry = tk.Entry(master, width=20)
        self.func_entry.insert(0, "np.exp")
        self.func_entry.grid(row=0, column=1)

        tk.Label(master, text="Nodos x separados por comas").grid(row=1, column=0)
        self.nodos_entry = tk.Entry(master, width=20)
        self.nodos_entry.insert(0, "0,1,2")
        self.nodos_entry.grid(row=1, column=1)

        # Botón
        self.run_button = tk.Button(master, text="Calcular Lagrange", command=self.run)
        self.run_button.grid(row=2, column=0, columnspan=2)

        # Canvas para gráfico
        self.fig, self.ax = plt.subplots(1,2, figsize=(10,5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2)

        # Tabla de resultados
        self.tree = ttk.Treeview(master, columns=("x","f(x)","Pn(x)","|f-Pn|"), show='headings')
        self.tree.heading("x", text="x")
        self.tree.heading("f(x)", text="f(x)")
        self.tree.heading("Pn(x)", text="Pn(x)")
        self.tree.heading("|f-Pn|", text="|f-Pn|")
        self.tree.grid(row=4, column=0, columnspan=2)

    def run(self):
        # Limpiar tabla
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Leer función
        try:
            f = eval("lambda x: " + self.func_entry.get())
        except:
            tk.messagebox.showerror("Error","Función inválida")
            return

        # Leer nodos
        try:
            x_nodos = np.array([float(x) for x in self.nodos_entry.get().split(",")])
        except:
            tk.messagebox.showerror("Error","Nodos inválidos")
            return
        y_nodos = f(x_nodos)

        # Malla fina
        x_malla = np.linspace(min(x_nodos), max(x_nodos), 50)  # 50 puntos para la tabla
        P_n = Lagrange_poly_1D(x_malla, x_nodos, y_nodos)
        f_malla = f(x_malla)
        errores = np.abs(f_malla - P_n)

        # Llenar tabla
        for xi, fi, pi, ei in zip(x_malla, f_malla, P_n, errores):
            self.tree.insert("", "end", values=(f"{xi:.4f}", f"{fi:.6f}", f"{pi:.6f}", f"{ei:.6f}"))

        # Error global y cota teórica
        E_global = np.max(errores)
        f_deriv_max = np.max([deriv_fd_1D(f, xi) for xi in x_malla])
        E_teorico = error_teorico_1D(f_deriv_max, x_nodos, x_malla)

        print(f"Error global numérico: {E_global:.6f}")
        print(f"Cota teórica del error: {E_teorico:.6f}")

        # Graficar
        self.ax[0].cla()
        self.ax[0].plot(x_malla, f_malla, label='f(x)', color='blue')
        self.ax[0].plot(x_malla, P_n, '--', label='P_n(x)', color='red')
        self.ax[0].scatter(x_nodos, y_nodos, color='black', zorder=5, label='Nodos')
        self.ax[0].set_title("Interpolación Lagrange")
        self.ax[0].legend()
        self.ax[0].grid(True)

        self.ax[1].cla()
        self.ax[1].plot(x_malla, errores, label='Error |f-Pn|', color='green')
        self.ax[1].axhline(E_teorico, color='orange', linestyle='--', label='Cota teórica')
        self.ax[1].set_title("Error global vs. Cota teórica")
        self.ax[1].legend()
        self.ax[1].grid(True)

        self.canvas.draw()

# -------------------------
# Ejecutar GUI
# -------------------------
root = tk.Tk()
app = SimuladorLagrangeTabla(root)
root.mainloop()
