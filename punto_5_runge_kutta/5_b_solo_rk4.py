# -*- coding: utf-8 -*-
"""
Script independiente para resolver EDOs de primer orden con el método de Runge-Kutta 4 (RK4)
Interfaz gráfica Tkinter, personalizable para cualquier función, intervalo, condición inicial y h.
Muestra paso a paso, tabla de pendientes k1, k2, k3, k4 y resultados, solución analítica (si existe),
gráfica comparativa y tabla de errores, todo listo para copiar a mano.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RK4PasoAPasoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EDO Runge-Kutta 4 Paso a Paso")
        self.root.geometry("1200x900")
        self.solution_expr = None

        # Variables de entrada
        self.func_str = tk.StringVar(value="y*sin(x)")
        self.x0 = tk.DoubleVar(value=0.0)
        self.y0 = tk.DoubleVar(value=1.0)
        self.xf = tk.DoubleVar(value=float(np.pi))
        self.h = tk.DoubleVar(value=float(np.pi/10))

        self._crear_widgets()

    def _crear_widgets(self):
        frame_in = tk.LabelFrame(self.root, text="Parámetros de Entrada", padx=5, pady=5)
        frame_in.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_in, text="f(x,y)=").grid(row=0,column=0)
        tk.Entry(frame_in, textvariable=self.func_str, width=20).grid(row=0,column=1)
        tk.Label(frame_in, text="x0").grid(row=0,column=2)
        tk.Entry(frame_in, textvariable=self.x0, width=8).grid(row=0,column=3)
        tk.Label(frame_in, text="y0").grid(row=0,column=4)
        tk.Entry(frame_in, textvariable=self.y0, width=8).grid(row=0,column=5)
        tk.Label(frame_in, text="x_fin").grid(row=0,column=6)
        tk.Entry(frame_in, textvariable=self.xf, width=8).grid(row=0,column=7)
        tk.Label(frame_in, text="h").grid(row=0,column=8)
        tk.Entry(frame_in, textvariable=self.h, width=8).grid(row=0,column=9)
        tk.Button(frame_in, text="Calcular RK4", bg="#4CAF50", fg="white", command=self.calcular_rk4).grid(row=0,column=10,padx=5)
        tk.Button(frame_in, text="Solución Analítica", bg="#9C27B0", fg="white", command=self.calcular_analitica).grid(row=0,column=11,padx=5)

        # Paneles de salida
        self.paned = tk.PanedWindow(self.root, orient="horizontal")
        self.paned.pack(fill="both", expand=True, padx=10, pady=5)

        # Panel izquierdo: Explicación paso a paso
        frame_pasos = tk.LabelFrame(self.paned, text="Explicación Paso a Paso (RK4)")
        self.paned.add(frame_pasos, stretch="always")
        self.text_pasos = tk.Text(frame_pasos, wrap="word", height=30, font=("Consolas",11))
        self.text_pasos.pack(fill="both", expand=True)

        # Panel derecho: Tabla de pendientes y resultados
        frame_tabla = tk.LabelFrame(self.paned, text="Tabla RK4 (k1, k2, k3, k4, y)")
        self.paned.add(frame_tabla, stretch="always")
        self.rk4_table = ttk.Treeview(frame_tabla, columns=("n","x_n","y_n","k1","k2","k3","k4","y_{n+1}","y_exact","Error"),
                                      show="headings", height=30)
        self.rk4_table.pack(fill="both", expand=True)
        for col in self.rk4_table["columns"]:
            self.rk4_table.heading(col, text=col)
            self.rk4_table.column(col, width=100, anchor="center")

        # Panel gráfico
        self.frame_plot = tk.LabelFrame(self.root, text="Gráfica Comparativa")
        self.frame_plot.pack(fill="both", expand=True, padx=10, pady=5)
        self.fig, self.ax = plt.subplots(figsize=(8,4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def f(self, x, y):
        x_sym, y_sym = sp.symbols("x y")
        expr = sp.sympify(self.func_str.get())
        f_lamb = sp.lambdify((x_sym, y_sym), expr, "numpy")
        return f_lamb(x, y)

    def calcular_rk4(self):
        self.text_pasos.delete("1.0", tk.END)
        self.rk4_table.delete(*self.rk4_table.get_children())
        x0, y0, xf, h = self.x0.get(), self.y0.get(), self.xf.get(), self.h.get()
        n_steps = int(np.round((xf - x0) / h))
        x_vals = [x0]
        y_vals = [y0]
        tabla_rows = []
        explicaciones = []

        x, y = x0, y0
        for i in range(n_steps):
            k1 = self.f(x, y)
            k2 = self.f(x + h/2, y + h*k1/2)
            k3 = self.f(x + h/2, y + h*k2/2)
            k4 = self.f(x + h, y + h*k3)
            y_next = y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
            x_next = x + h

            # Explicación detallada para cada paso
            explicacion = (
                f"Iteración {i+1}:\n"
                f"x_n = {x:.8f}, y_n = {y:.10f}\n"
                f"k1 = f(x_n, y_n) = f({x:.8f}, {y:.10f}) = {k1:.10f}\n"
                f"k2 = f(x_n + h/2, y_n + h*k1/2) = f({x+h/2:.8f}, {y+h*k1/2:.10f}) = {k2:.10f}\n"
                f"k3 = f(x_n + h/2, y_n + h*k2/2) = f({x+h/2:.8f}, {y+h*k2/2:.10f}) = {k3:.10f}\n"
                f"k4 = f(x_n + h, y_n + h*k3) = f({x+h:.8f}, {y+h*k3:.10f}) = {k4:.10f}\n"
                f"y_(n+1) = y_n + (h/6)*(k1 + 2*k2 + 2*k3 + k4)\n"
                f"       = {y:.10f} + ({h:.8f}/6)*({k1:.10f} + 2*{k2:.10f} + 2*{k3:.10f} + {k4:.10f})\n"
                f"       = {y_next:.10f}\n"
                "-------------------------------------------------------------\n"
            )
            explicaciones.append(explicacion)

            # Solución exacta y error
            y_exact = "-"
            error = "-"
            if self.solution_expr is not None:
                try:
                    y_exact_val = float(self.solution_expr.subs("x", x_next))
                    y_exact = f"{y_exact_val:.10f}"
                    error_val = abs(y_next - y_exact_val)
                    error = f"{error_val:.2e}"
                except:
                    pass

            tabla_rows.append([
                i, f"{x:.8f}", f"{y:.10f}", f"{k1:.10f}", f"{k2:.10f}", f"{k3:.10f}", f"{k4:.10f}",
                f"{y_next:.10f}", y_exact, error
            ])
            x, y = x_next, y_next
            x_vals.append(x)
            y_vals.append(y)

        self.text_pasos.insert(tk.END, "DETALLE DE CADA ITERACIÓN (RK4)\n")
        self.text_pasos.insert(tk.END, "="*65 + "\n\n")
        self.text_pasos.insert(tk.END, "".join(explicaciones))

        for row in tabla_rows:
            self.rk4_table.insert("", "end", values=row)

        # Gráfica
        self.ax.clear()
        self.ax.plot(x_vals, y_vals, label="RK4", marker="o")
        if self.solution_expr is not None:
            x_dense = np.linspace(x0, xf, 400)
            y_dense = [float(self.solution_expr.subs("x", xx)) for xx in x_dense]
            self.ax.plot(x_dense, y_dense, "k--", label="Exacta")
        self.ax.set_title("RK4 vs Solución Analítica")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y(x)")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

    def calcular_analitica(self):
        x_sym = sp.symbols("x")
        y_func = sp.Function("y")
        try:
            expr = sp.sympify(self.func_str.get())
            ode = sp.Eq(sp.Derivative(y_func(x_sym), x_sym), expr.subs({"y": y_func(x_sym)}))
            sol = sp.dsolve(ode, ics={y_func(self.x0.get()): self.y0.get()})
            self.solution_expr = sol.rhs
            messagebox.showinfo("Solución Analítica", f"y(x) = {sp.pretty(sol.rhs)}")
        except Exception as e:
            self.solution_expr = None
            messagebox.showerror("Error", f"No se pudo calcular la solución analítica.\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RK4PasoAPasoApp(root)
    root.mainloop()