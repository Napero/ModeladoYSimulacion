# Busqueda binaria de raices en python hecho por Francisco Nappa

# Podés escribir la función f(x) usando cualquier función del módulo math de Python.
# Ejemplos válidos:
#   x**2 - 2           # polinomios
#   sin(x)             # seno
#   cos(x)             # coseno
#   tan(x)             # tangente
#   exp(x)             # exponencial
#   log(x)             # logaritmo natural (base e)
#   log(x)/log(10)     # logaritmo en base 10
#   sqrt(x)            # raíz cuadrada
#   abs(x)             # valor absoluto
#   pow(x, 3)          # potencia
# Podés combinar funciones y operaciones:
#   sin(x) + log(x) - x**2
#   exp(-x) * cos(x)
# Recordá: 
# - Usa "x" como variable.
# - Para logaritmo en base n: log(x)/log(n)
# - Todas las funciones deben estar escritas en minúsculas.
# - No uses funciones que no estén en el módulo

import tkinter as tk
from tkinter import ttk, messagebox
import math
import ast

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def make_func(expr):
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    allowed_names.update({"abs": abs, "pow": pow})
    expr_ast = ast.parse(expr, mode='eval')
    code = compile(expr_ast, '<string>', 'eval')
    def f(x):
        return eval(code, {'__builtins__': {}}, {**allowed_names, 'x': x})
    return f

def biseccion(f, a, b, tol=1e-8, max_iter=50):
    history = []
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos")
    for n in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        diff = abs(b - a)  # <-- NUEVO: diferencia entre extremos
        history.append((n, a, b, c, fc, diff))  # <-- NUEVO: agrega diff
        if abs(fc) < tol or diff < tol:
            return c, history
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return None, history

class BiseccionGUI:
    def __init__(self, master):
        self.master = master
        master.title("Búsqueda Binaria de Raíces (Bisección)")
        self._build_widgets()

    def _build_widgets(self):
        frm = ttk.Frame(self.master, padding=10)
        frm.grid(row=0, column=0, sticky='nsew')

        ttk.Label(frm, text="f(x):").grid(row=0, column=0)
        self.expr_var = tk.StringVar(value="x**3 - x - 2")
        ttk.Entry(frm, textvariable=self.expr_var, width=30).grid(row=0, column=1, columnspan=2)

        ttk.Label(frm, text="a:").grid(row=1, column=0)
        self.a_var = tk.StringVar(value="1")
        ttk.Entry(frm, textvariable=self.a_var, width=10).grid(row=1, column=1)

        ttk.Label(frm, text="b:").grid(row=1, column=2)
        self.b_var = tk.StringVar(value="2")
        ttk.Entry(frm, textvariable=self.b_var, width=10).grid(row=1, column=3)

        ttk.Label(frm, text="Tolerancia:").grid(row=2, column=0)
        self.tol_var = tk.StringVar(value="1e-8")
        ttk.Entry(frm, textvariable=self.tol_var, width=10).grid(row=2, column=1)

        ttk.Button(frm, text="Buscar raíz", command=self.run_biseccion).grid(row=2, column=2, columnspan=2)

        cols = ("n", "a", "b", "c", "f(c)", "|b-a|")  # <-- NUEVO: agrega columna
        self.tree = ttk.Treeview(frm, columns=cols, show='headings', height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=80, anchor='center')
        self.tree.grid(row=3, column=0, columnspan=4, pady=10)

        self.result_var = tk.StringVar(value="Raíz: -")
        ttk.Label(frm, textvariable=self.result_var).grid(row=4, column=0, columnspan=4, sticky='w')

        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frm)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=4)

    def _populate_table(self, history):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for rec in history:
            self.tree.insert('', 'end', values=tuple(f"{v:.6g}" if isinstance(v, float) else v for v in rec))

    def _plot(self, f, a, b, root):
        X = [a + i*(b-a)/400 for i in range(401)]
        Y = [f(x) for x in X]
        self.ax.clear()
        self.ax.plot(X, Y, label='f(x)')
        self.ax.axhline(0, color='k', ls='--')
        self.ax.axvline(root, color='r', ls='-', label='Raíz')
        self.ax.axvline(a, color='g', ls=':', label='a')
        self.ax.axvline(b, color='b', ls=':', label='b')
        self.ax.legend()
        self.canvas.draw()

    def run_biseccion(self):
        try:
            f = make_func(self.expr_var.get())
            a = float(self.a_var.get())
            b = float(self.b_var.get())
            tol = float(self.tol_var.get())
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        try:
            root, hist = biseccion(f, a, b, tol)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self._populate_table(hist)
        self.result_var.set(f"Raíz: {root}" if root else "No convergió")
        self._plot(f, a, b, root if root else a)

def main():
    root = tk.Tk()
    BiseccionGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()