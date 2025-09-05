# Método de Montecarlo para aproximar el valor de pi hecho por Francisco Nappa

import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.stats import norm

class MontecarloPiGUI:
    def __init__(self, master):
        self.master = master
        master.title("Montecarlo para aproximar π")
        self.resultados = []  # <-- Guarda los resultados para recalcular IC
        self._build_widgets()

    def _build_widgets(self):
        frm = ttk.Frame(self.master, padding=10)
        frm.grid(row=0, column=0, sticky='nsew')

        ttk.Label(frm, text="Número de puntos:").grid(row=0, column=0)
        self.n_var = tk.StringVar(value="1000")
        ttk.Entry(frm, textvariable=self.n_var, width=10).grid(row=0, column=1)

        ttk.Label(frm, text="Confianza (%):").grid(row=0, column=2)
        self.ic_var = tk.StringVar(value="99")
        ttk.Entry(frm, textvariable=self.ic_var, width=5).grid(row=0, column=3)

        ttk.Button(frm, text="Generar", command=self.run_montecarlo).grid(row=0, column=4)
        ttk.Button(frm, text="Regenerar IC", command=self.regenerar_ic).grid(row=0, column=5)

        self.result_var = tk.StringVar(value="π ≈ -")
        ttk.Label(frm, textvariable=self.result_var).grid(row=1, column=0, columnspan=6, sticky='w')

        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frm)
        self.canvas.get_tk_widget().grid(row=2, column=0, columnspan=6)

    def run_montecarlo(self):
        try:
            n = int(self.n_var.get())
            if n <= 0:
                raise ValueError("El número de puntos debe ser positivo.")
            ic = float(self.ic_var.get())
            if not (0 < ic < 100):
                raise ValueError("El intervalo de confianza debe estar entre 0 y 100.")
        except Exception as e:
            self.result_var.set(f"Error: {e}")
            return

        inside_x, inside_y = [], []
        outside_x, outside_y = [], []
        self.resultados = []
        puntos_dentro = 0
        puntos_fuera = 0
        for _ in range(n):
            x, y = random.uniform(0, 1), random.uniform(0, 1)
            dentro = x**2 + y**2 <= 1
            self.resultados.append(4 if dentro else 0)
            if dentro:
                inside_x.append(x)
                inside_y.append(y)
                puntos_dentro += 1
            else:
                outside_x.append(x)
                outside_y.append(y)
                puntos_fuera += 1
        self._mostrar_resultado(ic, puntos_dentro, puntos_fuera)

        self.ax.clear()
        circle = plt.Circle((0, 0), 1, color='gray', fill=False)
        self.ax.add_artist(circle)
        self.ax.scatter(inside_x, inside_y, color='orange', s=5, label='Dentro')
        self.ax.scatter(outside_x, outside_y, color='blue', s=5, label='Fuera')
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_aspect('equal')
        self.ax.legend()
        self.canvas.draw()

    def regenerar_ic(self):
        try:
            ic = float(self.ic_var.get())
            if not (0 < ic < 100):
                raise ValueError("El intervalo de confianza debe estar entre 0 y 100.")
        except Exception as e:
            self.result_var.set(f"Error: {e}")
            return
        if not self.resultados:
            self.result_var.set("Primero genera los puntos.")
            return
        puntos_dentro = sum(1 for r in self.resultados if r == 4)
        puntos_fuera = sum(1 for r in self.resultados if r == 0)
        self._mostrar_resultado(ic, puntos_dentro, puntos_fuera)

    def _mostrar_resultado(self, ic, puntos_dentro, puntos_fuera):
        n = len(self.resultados)
        pi_aprox = np.mean(self.resultados)
        sigma = np.std(self.resultados, ddof=1)
        EE = sigma / np.sqrt(n)
        alpha = 1 - ic / 100
        z = norm.ppf(1 - alpha / 2)
        ic_val = (pi_aprox - z * EE, pi_aprox + z * EE)
        texto = (
            f"π ≈ {pi_aprox:.6f}\n"
            f"Desviación estándar: {sigma:.6f}\n"
            f"Error estándar: {EE:.6f}\n"
            f"IC {ic:.2f}%: [{ic_val[0]:.6f}, {ic_val[1]:.6f}]\n"
            f"Puntos dentro: {puntos_dentro}\n"
            f"Puntos fuera: {puntos_fuera}"
        )
        self.result_var.set(texto)

def main():
    root = tk.Tk()
    MontecarloPiGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
