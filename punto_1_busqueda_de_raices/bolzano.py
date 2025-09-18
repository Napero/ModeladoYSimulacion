# archivo para usar el teorema de bolzano, te da una interfaz para poner una funcion y un intervalo y te dice si hay una raiz en ese intervalo

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

def eval_func(expr, x):
    # Permite usar pi, e, funciones numpy
    expr = expr.replace('pi', 'np.pi').replace('e', 'np.e')
    try:
        return eval(expr, {"np": np, "x": x})
    except Exception as ex:
        raise ValueError(f"Error al evaluar la función: {ex}")

def bolzano_test(expr, a, b):
    fa = eval_func(expr, a)
    fb = eval_func(expr, b)
    return fa, fb, fa * fb < 0

class BolzanoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Teorema de Bolzano — ¿Hay raíz en el intervalo?")
        self.geometry("400x220")
        self.resizable(False, False)

        ttk.Label(self, text="Función f(x):").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.expr_entry = ttk.Entry(self, width=30)
        self.expr_entry.grid(row=0, column=1, padx=10, pady=10)
        self.expr_entry.insert(0, "np.exp(x)-3*x**2")

        ttk.Label(self, text="Extremo a:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.a_entry = ttk.Entry(self, width=10)
        self.a_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.a_entry.insert(0, "0")

        ttk.Label(self, text="Extremo b:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.b_entry = ttk.Entry(self, width=10)
        self.b_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.b_entry.insert(0, "1")

        self.check_btn = ttk.Button(self, text="Verificar Bolzano", command=self.check_bolzano)
        self.check_btn.grid(row=3, column=0, columnspan=2, pady=15)

        self.result_label = ttk.Label(self, text="", font=("Arial", 11))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

    def check_bolzano(self):
        expr = self.expr_entry.get()
        try:
            a = float(eval(self.a_entry.get(), {"np": np}))
            b = float(eval(self.b_entry.get(), {"np": np}))
            fa, fb, hay_raiz = bolzano_test(expr, a, b)
            msg = f"f({a}) = {fa:.6g}\n" \
                  f"f({b}) = {fb:.6g}\n"
            if hay_raiz:
                msg += "⇒ Hay al menos una raíz en el intervalo."
            else:
                msg += "⇒ No se garantiza raíz en el intervalo."
            self.result_label.config(text=msg)
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

if __name__ == "__main__":
    BolzanoApp().mainloop()
