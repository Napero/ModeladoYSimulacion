# -*- coding: utf-8 -*-
"""
Aplicación Tkinter para:
1. Ingresar una EDO de primer orden: dy/dx = f(x,y)
2. Parámetros: f(x,y), x0, y0, x_fin, h
3. Seleccionar método numérico: Euler, RK2 (Heun), RK2 (Punto Medio), RK4
4. Mostrar paso a paso (explicación detallada) de la 1ra y 2da iteración (apto para copiar a mano).
5. Calcular solución numérica en todo el intervalo.
6. Intentar obtener solución analítica (si Sympy puede) y comparar (errores y gráfica).
7. Graficar solución aproximada y exacta (si existe).
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -------------------------------------------------------------------------------------------------
# Métodos Numéricos Implementados
# -------------------------------------------------------------------------------------------------

def metodo_euler(f, x, y, h):
    return y + h * f(x, y)

def metodo_rk2_heun(f, x, y, h):
    k1 = f(x, y)
    k2 = f(x + h, y + h * k1)
    return y + (h / 2.0) * (k1 + k2)

def metodo_rk2_puntomedio(f, x, y, h):
    k1 = f(x, y)
    k2 = f(x + h / 2.0, y + (h / 2.0) * k1)
    return y + h * k2

def metodo_rk4(f, x, y, h):
    k1 = f(x, y)
    k2 = f(x + h / 2.0, y + (h / 2.0) * k1)
    k3 = f(x + h / 2.0, y + (h / 2.0) * k2)
    k4 = f(x + h, y + h * k3)
    return y + (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

METODOS = {
    "Euler": metodo_euler,
    "RK2 - Heun": metodo_rk2_heun,
    "RK2 - Punto Medio": metodo_rk2_puntomedio,
    "RK4": metodo_rk4
}

# -------------------------------------------------------------------------------------------------
# Clase principal
# -------------------------------------------------------------------------------------------------

class AppIteracionesPasoAPaso:
    def __init__(self, root):
        self.root = root
        self.root.title("Iteraciones Paso a Paso - Métodos Numéricos EDO")
        self.root.geometry("1080x780")

        self.func_str = tk.StringVar(value="y*sin(x)")
        self.x0_var = tk.DoubleVar(value=0.0)
        self.y0_var = tk.DoubleVar(value=1.0)
        self.xf_var = tk.DoubleVar(value=float(np.pi))
        self.h_var = tk.DoubleVar(value=float(np.pi/10))
        self.metodo_var = tk.StringVar(value="Euler")

        self._crear_widgets()

        self.fig, self.ax = plt.subplots(figsize=(6,4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------------------------------------------------------------------------------------------
    # GUI
    # ---------------------------------------------------------------------------------------------
    def _crear_widgets(self):
        frame_top = tk.LabelFrame(self.root, text="Parámetros de Entrada", padx=6, pady=6)
        frame_top.pack(fill="x", padx=8, pady=6)

        tk.Label(frame_top, text="f(x,y) =").grid(row=0, column=0, sticky="e")
        tk.Entry(frame_top, textvariable=self.func_str, width=20).grid(row=0, column=1, padx=4)

        tk.Label(frame_top, text="x0").grid(row=0, column=2, sticky="e")
        tk.Entry(frame_top, textvariable=self.x0_var, width=8).grid(row=0, column=3, padx=4)

        tk.Label(frame_top, text="y0").grid(row=0, column=4, sticky="e")
        tk.Entry(frame_top, textvariable=self.y0_var, width=8).grid(row=0, column=5, padx=4)

        tk.Label(frame_top, text="x_fin").grid(row=0, column=6, sticky="e")
        tk.Entry(frame_top, textvariable=self.xf_var, width=8).grid(row=0, column=7, padx=4)

        tk.Label(frame_top, text="h").grid(row=0, column=8, sticky="e")
        tk.Entry(frame_top, textvariable=self.h_var, width=8).grid(row=0, column=9, padx=4)

        tk.Label(frame_top, text="Método").grid(row=0, column=10, sticky="e")
        ttk.Combobox(frame_top, textvariable=self.metodo_var, values=list(METODOS.keys()),
                     state="readonly", width=16).grid(row=0, column=11, padx=4)

        tk.Button(frame_top, text="Calcular", command=self.calcular_todo, width=12).grid(row=0, column=12, padx=6)
        tk.Button(frame_top, text="Limpiar", command=self.limpiar_salida, width=10).grid(row=0, column=13, padx=4)

        frame_textos = tk.PanedWindow(self.root, orient="horizontal")
        frame_textos.pack(fill="both", expand=True, padx=8, pady=4)

        frame_izq = tk.LabelFrame(frame_textos, text="Paso a Paso (1ra y 2da Iteración)")
        frame_der = tk.LabelFrame(frame_textos, text="Resumen / Tabla / Exacta")

        frame_textos.add(frame_izq)
        frame_textos.add(frame_der)

        self.text_pasos = tk.Text(frame_izq, wrap="word", height=22)
        self.text_pasos.pack(fill="both", expand=True)
        self.text_resumen = tk.Text(frame_der, wrap="word", height=22)
        self.text_resumen.pack(fill="both", expand=True)

        self.frame_plot = tk.LabelFrame(self.root, text="Gráfica")
        self.frame_plot.pack(fill="both", expand=True, padx=8, pady=6)

    # ---------------------------------------------------------------------------------------------
    # Utilidades
    # ---------------------------------------------------------------------------------------------
    def limpiar_salida(self):
        self.text_pasos.delete("1.0", tk.END)
        self.text_resumen.delete("1.0", tk.END)
        self.ax.clear()
        self.canvas.draw()

    def _construir_funcion(self):
        f_str = self.func_str.get()
        x, y = sp.symbols("x y")
        try:
            expr = sp.sympify(f_str, {"sin": sp.sin, "cos": sp.cos, "exp": sp.exp,
                                      "log": sp.log, "sqrt": sp.sqrt, "tan": sp.tan,
                                      "pi": sp.pi, "E": sp.E})
        except Exception as e:
            raise ValueError(f"Expresión inválida: {e}")
        f_lambda = sp.lambdify((x, y), expr, "numpy")
        return expr, f_lambda

    def _intentar_sol_analitica(self, expr, x0, y0):
        x = sp.symbols("x")
        y = sp.Function("y")
        try:
            ode = sp.Eq(sp.diff(y(x), x), expr.subs({sp.Symbol("y"): y(x)}))
            sol = sp.dsolve(ode, ics={y(x0): y0})
            return sol  # Eq(y(x), ...)
        except Exception:
            return None

    # ---------------------------------------------------------------------------------------------
    # Generación Paso a Paso
    # ---------------------------------------------------------------------------------------------
    def _explicacion_iteracion(self, metodo_nombre, f_expr, f_eval, x_n, y_n, h, n):
        x_sym, y_sym = sp.symbols("x y")
        fmt = lambda v: f"{v:.10f}"
        lines = []
        lines.append(f"--- Iteración {n+1} (desde n={n}) --------------------------------------------------")
        lines.append(f"x_{n} = {fmt(x_n)}, y_{n} = {fmt(y_n)}, h = {fmt(h)}")
        lines.append(f"Método: {metodo_nombre}")
        f_sub_expr = f_expr.subs({x_sym: x_n, y_sym: y_n})
        try:
            f_num = float(f_sub_expr.evalf())
        except Exception:
            f_num = f_eval(x_n, y_n)

        if metodo_nombre == "Euler":
            lines.append("Fórmula: y_{n+1} = y_n + h * f(x_n, y_n)")
            lines.append(f"1. Evaluar f(x_n, y_n): f({fmt(x_n)}, {fmt(y_n)}) = {sp.simplify(f_sub_expr)} = {fmt(f_num)}")
            y_next = metodo_euler(f_eval, x_n, y_n, h)
            lines.append(f"2. Sustituir: y_{n+1} = {fmt(y_n)} + {fmt(h)} * {fmt(f_num)}")
            lines.append(f"3. Resultado: y_{n+1} = {fmt(y_next)}")

        elif metodo_nombre == "RK2 - Heun":
            lines.append("Fórmula Heun (RK2 explícito):")
            lines.append("k1 = f(x_n, y_n)")
            lines.append("k2 = f(x_n + h, y_n + h*k1)")
            lines.append("y_{n+1} = y_n + (h/2)*(k1 + k2)")
            k1_expr = f_sub_expr
            k1_num = f_num
            x_k2 = x_n + h
            y_k2_pred = y_n + h * k1_num
            k2_expr_sym = f_expr.subs({x_sym: x_k2, y_sym: y_k2_pred})
            k2_num = float(k2_expr_sym.evalf())
            y_next = metodo_rk2_heun(f_eval, x_n, y_n, h)
            lines.append(f"1. k1 = f({fmt(x_n)}, {fmt(y_n)}) = {sp.simplify(k1_expr)} = {fmt(k1_num)}")
            lines.append(f"2. k2: x_n + h = {fmt(x_k2)}, y_n + h*k1 = {fmt(y_k2_pred)}")
            lines.append(f"   k2 = f({fmt(x_k2)}, {fmt(y_k2_pred)}) = {sp.simplify(k2_expr_sym)} = {fmt(k2_num)}")
            lines.append(f"3. y_{n+1} = {fmt(y_n)} + {fmt(h)}/2 * ({fmt(k1_num)} + {fmt(k2_num)}) = {fmt(y_next)}")

        elif metodo_nombre == "RK2 - Punto Medio":
            lines.append("Fórmula RK2 (Punto Medio):")
            lines.append("k1 = f(x_n, y_n)")
            lines.append("k2 = f(x_n + h/2, y_n + (h/2)*k1)")
            lines.append("y_{n+1} = y_n + h*k2")
            k1_expr = f_sub_expr
            k1_num = f_num
            x_mid = x_n + h/2.0
            y_mid = y_n + (h/2.0)*k1_num
            k2_expr_sym = f_expr.subs({x_sym: x_mid, y_sym: y_mid})
            k2_num = float(k2_expr_sym.evalf())
            y_next = metodo_rk2_puntomedio(f_eval, x_n, y_n, h)
            lines.append(f"1. k1 = f({fmt(x_n)}, {fmt(y_n)}) = {sp.simplify(k1_expr)} = {fmt(k1_num)}")
            lines.append(f"2. k2: x_n + h/2 = {fmt(x_mid)}, y_n + h/2*k1 = {fmt(y_mid)}")
            lines.append(f"   k2 = f({fmt(x_mid)}, {fmt(y_mid)}) = {sp.simplify(k2_expr_sym)} = {fmt(k2_num)}")
            lines.append(f"3. y_{n+1} = {fmt(y_n)} + {fmt(h)} * {fmt(k2_num)} = {fmt(y_next)}")

        elif metodo_nombre == "RK4":
            lines.append("Fórmula RK4:")
            lines.append("k1 = f(x_n, y_n)")
            lines.append("k2 = f(x_n + h/2, y_n + (h/2)*k1)")
            lines.append("k3 = f(x_n + h/2, y_n + (h/2)*k2)")
            lines.append("k4 = f(x_n + h, y_n + h*k3)")
            lines.append("y_{n+1} = y_n + (h/6)*(k1 + 2k2 + 2k3 + k4)")
            k1_expr = f_sub_expr
            k1_num = f_num
            x2 = x_n + h/2.0
            y2 = y_n + (h/2.0)*k1_num
            k2_expr_sym = f_expr.subs({x_sym: x2, y_sym: y2})
            k2_num = float(k2_expr_sym.evalf())
            y3 = y_n + (h/2.0)*k2_num
            k3_expr_sym = f_expr.subs({x_sym: x2, y_sym: y3})
            k3_num = float(k3_expr_sym.evalf())
            x4 = x_n + h
            y4 = y_n + h * k3_num
            k4_expr_sym = f_expr.subs({x_sym: x4, y_sym: y4})
            k4_num = float(k4_expr_sym.evalf())
            y_next = metodo_rk4(f_eval, x_n, y_n, h)
            lines.append(f"1. k1 = f({fmt(x_n)}, {fmt(y_n)}) = {sp.simplify(k1_expr)} = {fmt(k1_num)}")
            lines.append(f"2. k2: x = {fmt(x2)}, y = {fmt(y2)} -> {sp.simplify(k2_expr_sym)} = {fmt(k2_num)}")
            lines.append(f"3. k3: x = {fmt(x2)}, y = {fmt(y3)} -> {sp.simplify(k3_expr_sym)} = {fmt(k3_num)}")
            lines.append(f"4. k4: x = {fmt(x4)}, y = {fmt(y4)} -> {sp.simplify(k4_expr_sym)} = {fmt(k4_num)}")
            lines.append(f"5. y_{n+1} = {fmt(y_n)} + {fmt(h)}/6 * ({fmt(k1_num)} + 2*{fmt(k2_num)} + 2*{fmt(k3_num)} + {fmt(k4_num)}) = {fmt(y_next)}")

        lines.append("")
        return "\n".join(lines)

    # ---------------------------------------------------------------------------------------------
    # Cálculo principal
    # ---------------------------------------------------------------------------------------------
    def calcular_todo(self):
        try:
            f_expr, f_eval = self._construir_funcion()
            x0 = float(self.x0_var.get())
            y0 = float(self.y0_var.get())
            xf = float(self.xf_var.get())
            h = float(self.h_var.get())
            metodo_nombre = self.metodo_var.get()
            metodo_fn = METODOS[metodo_nombre]

            if h <= 0:
                raise ValueError("h debe ser > 0")
            if xf <= x0:
                raise ValueError("x_fin debe ser > x0")

            n_steps_real = (xf - x0) / h
            n_steps = int(round(n_steps_real + 1e-12))
            if abs(n_steps * h - (xf - x0)) > 1e-9:
                messagebox.showwarning("Aviso",
                    "El intervalo no es múltiplo exacto de h. Se ajustará el número de pasos.")
            xs = [x0]
            ys = [y0]

            self.text_pasos.delete("1.0", tk.END)
            self.text_resumen.delete("1.0", tk.END)

            y_n = y0
            x_n = x0
            pasos_detalle = []
            for n in range(n_steps):
                if n < 2:
                    explicacion = self._explicacion_iteracion(metodo_nombre, f_expr, f_eval, x_n, y_n, h, n)
                    pasos_detalle.append(explicacion)
                y_next = metodo_fn(f_eval, x_n, y_n, h)
                x_next = x_n + h
                xs.append(x_next)
                ys.append(y_next)
                y_n = y_next
                x_n = x_next

            self.text_pasos.insert(tk.END, "DETALLE DE PRIMERA Y SEGUNDA ITERACIÓN\n")
            self.text_pasos.insert(tk.END, "="*62 + "\n\n")
            self.text_pasos.insert(tk.END, "\n".join(pasos_detalle))

            sol_analitica = self._intentar_sol_analitica(f_expr, x0, y0)
            x_sym = sp.symbols("x")

            resumen_lines = []
            resumen_lines.append("RESUMEN DE LA SOLUCIÓN NUMÉRICA")
            resumen_lines.append("-"*60)
            resumen_lines.append(f"Método: {metodo_nombre}")
            resumen_lines.append(f"f(x,y) = {sp.simplify(f_expr)}")
            resumen_lines.append(f"Intervalo: [{x0}, {xf}]   h = {h}   Pasos = {n_steps}")
            resumen_lines.append("")
            if sol_analitica is not None and hasattr(sol_analitica, 'rhs'):
                resumen_lines.append("Solución analítica encontrada:")
                resumen_lines.append(f"y(x) = {sp.simplify(sol_analitica.rhs)}")
            else:
                resumen_lines.append("No se encontró solución analítica simbólica con dsolve().")

            resumen_lines.append("")
            resumen_lines.append("Tabla de nodos:")
            header = f"{'i':>3} | {'x_i':>12} | {'y_num':>18}"
            tiene_exacta = sol_analitica is not None and hasattr(sol_analitica, 'rhs')
            if tiene_exacta:
                header += f" | {'y_exacta':>18} | {'|error|':>14}"
            resumen_lines.append(header)
            resumen_lines.append("-"*len(header))

            y_exact_vals = []
            if tiene_exacta:
                y_exact_expr = sol_analitica.rhs
                for xv in xs:
                    y_exact_vals.append(float(y_exact_expr.subs({x_sym: xv}).evalf()))

            max_err = None
            for i, (xv, yv) in enumerate(zip(xs, ys)):
                if tiene_exacta:
                    ye = y_exact_vals[i]
                    err = abs(ye - yv)
                    if max_err is None or err > max_err:
                        max_err = err
                    resumen_lines.append(f"{i:3d} | {xv:12.8f} | {yv:18.10f} | {ye:18.10f} | {err:14.6e}")
                else:
                    resumen_lines.append(f"{i:3d} | {xv:12.8f} | {yv:18.10f}")

            if tiene_exacta:
                resumen_lines.append("")
                resumen_lines.append(f"Error máximo (nodos): {max_err:.6e}")

            self.text_resumen.insert(tk.END, "\n".join(resumen_lines))

            self.ax.clear()
            self.ax.plot(xs, ys, 'o-', label="Aproximación Numérica", color="#1f77b4")
            if tiene_exacta:
                x_dense = np.linspace(x0, xf, 400)
                y_exact_expr = sol_analitica.rhs
                y_dense = [float(y_exact_expr.subs({x_sym: xv}).evalf()) for xv in x_dense]
                self.ax.plot(x_dense, y_dense, '-', label="Solución Analítica", color="#d62728")

            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.set_title("Solución Numérica vs Analítica")
            self.ax.grid(True, alpha=0.3)
            self.ax.legend()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"{type(e).__name__}: {e}")

# -------------------------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = AppIteracionesPasoAPaso(root)
    root.mainloop()