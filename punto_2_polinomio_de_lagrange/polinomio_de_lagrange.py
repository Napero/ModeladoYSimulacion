# -*- coding: utf-8 -*-
"""
Interfaz educativa (Ejercicio 2):
- Construye el polinomio de Lagrange P_n(x) para f(x) y nodos dados.
- Muestra paso a paso (lista de nodos, valores, bases L_i(x), polinomio expandido y simplificado).
- Calcula error local en ξ: |f(ξ) - P(ξ)|.
- Estima cota de error global usando max |f^{(n+1)}(x)| y max |∏(x - x_i)| en el intervalo (muestreo).
- Aproxima f'(x_d) vía diferencia central usando la malla (derivada numérica) y compara con f'(x_d) real y P'(x_d).
- Grafica f(x) y P_n(x); resalta nodos y punto ξ.
Adaptable: cambiar f(x), nodos, ξ y punto de derivada.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import sympy as sp
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------- LÓGICA ----------------- #
def parse_function(expr_str):
    x = sp.Symbol('x')
    expr_str = expr_str.replace("^", "**")
    try:
        expr = sp.sympify(expr_str, {"x": x, "e": sp.E, "pi": sp.pi})
    except Exception as e:
        raise ValueError(f"Expresión inválida: {e}")
    return expr, x

def build_lagrange_polynomial(expr, x, nodes):
    # y_i
    y_vals = [sp.N(expr.subs(x, xi)) for xi in nodes]
    n = len(nodes) - 1
    L_terms = []
    for i, xi in enumerate(nodes):
        num = 1
        den = 1
        for j, xj in enumerate(nodes):
            if i != j:
                num *= (x - xj)
                den *= (xi - xj)
        L_i = sp.simplify(num/den)
        L_terms.append(L_i)
    P = sum(y_vals[i]*L_terms[i] for i in range(len(nodes)))
    return sp.simplify(sp.expand(P)), y_vals, L_terms

def product_term(x_val, nodes, x_sym):
    prod = 1
    for xi in nodes:
        prod *= (x_sym - xi)
    return sp.N(prod.subs(x_sym, x_val)), sp.expand(prod)

def estimate_max_abs(expr, x_sym, a, b, samples=800):
    f_lamb = sp.lambdify(x_sym, expr, "numpy")
    xs = np.linspace(a, b, samples)
    try:
        vals = np.abs(f_lamb(xs))
        return float(np.nanmax(vals))
    except Exception:
        # fallback evaluando punto a punto sympy
        m = 0.0
        for xv in xs:
            try:
                v = abs(complex(expr.subs(x_sym, xv)))
                if v > m:
                    m = v
            except Exception:
                pass
        return float(m)

def central_difference(P_poly, x_sym, x_d, nodes):
    nodes_sorted = sorted(nodes)
    # Asumimos malla (casi) uniforme para ejercicio: h = primer paso
    if len(nodes_sorted) < 2:
        return None, None
    h_candidates = [round(nodes_sorted[i+1] - nodes_sorted[i], 12) for i in range(len(nodes_sorted)-1)]
    h = h_candidates[0]
    # Ajustar h si no es posible central en x_d
    if not (nodes_sorted[0] <= x_d - h and x_d + h <= nodes_sorted[-1]):
        # fallback: usar derivada simbólica del polinomio
        Pprime = sp.diff(P_poly, x_sym)
        return float(Pprime.subs(x_sym, x_d)), "Derivada simbólica del polinomio (no central posible)"
    P_lamb = sp.lambdify(x_sym, P_poly, "numpy")
    deriv = (P_lamb(x_d + h) - P_lamb(x_d - h))/(2*h)
    return float(deriv), f"Diferencia central con h = {h}"

# ----------------- UI ----------------- #
class LagrangeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modelo Polinomio de Lagrange - Ejercicio 2")
        self.geometry("1180x720")
        self._build_widgets()

    def _build_widgets(self):
        frame_in = ttk.LabelFrame(self, text="Entrada")
        frame_in.pack(side="top", fill="x", padx=6, pady=4)

        ttk.Label(frame_in, text="f(x)=").grid(row=0, column=0, padx=4, pady=3, sticky="e")
        self.func_entry = ttk.Entry(frame_in, width=35)
        self.func_entry.grid(row=0, column=1, padx=4, pady=3)
        self.func_entry.insert(0, "log(x+1)")  # ln(x+1)

        ttk.Label(frame_in, text="Nodos (coma):").grid(row=0, column=2, padx=4, pady=3, sticky="e")
        self.nodes_entry = ttk.Entry(frame_in, width=25)
        self.nodes_entry.grid(row=0, column=3, padx=4, pady=3)
        self.nodes_entry.insert(0, "0,1,2")

        ttk.Label(frame_in, text="ξ (error local):").grid(row=0, column=4, padx=4, pady=3, sticky="e")
        self.xi_entry = ttk.Entry(frame_in, width=10)
        self.xi_entry.grid(row=0, column=5, padx=4, pady=3)
        self.xi_entry.insert(0, "0.45")

        ttk.Label(frame_in, text="x_d (derivada):").grid(row=0, column=6, padx=4, pady=3, sticky="e")
        self.xd_entry = ttk.Entry(frame_in, width=10)
        self.xd_entry.grid(row=0, column=7, padx=4, pady=3)
        self.xd_entry.insert(0, "1.5")

        self.btn_calc = ttk.Button(frame_in, text="Calcular", command=self.calcular)
        self.btn_calc.grid(row=0, column=8, padx=10, pady=3)

        self.btn_clear = ttk.Button(frame_in, text="Limpiar", command=self.limpiar)
        self.btn_clear.grid(row=0, column=9, padx=4, pady=3)

        # Salida textual
        frame_out = ttk.LabelFrame(self, text="Desarrollo paso a paso")
        frame_out.pack(side="left", fill="both", expand=True, padx=6, pady=4)

        self.text = ScrolledText(frame_out, wrap="word", font=("Consolas", 10))
        self.text.pack(fill="both", expand=True)

        # Gráfico
        frame_plot = ttk.LabelFrame(self, text="Gráfica f(x) vs P_n(x)")
        frame_plot.pack(side="right", fill="both", expand=True, padx=6, pady=4)

        self.fig = Figure(figsize=(5.5,5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_plot)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def limpiar(self):
        self.text.delete("1.0", tk.END)
        self.ax.clear()
        self.canvas.draw()

    def calcular(self):
        self.limpiar()
        expr_str = self.func_entry.get().strip()
        nodes_str = self.nodes_entry.get().strip()
        xi_str = self.xi_entry.get().strip()
        xd_str = self.xd_entry.get().strip()
        try:
            expr, x = parse_function(expr_str)
            nodes = [float(s) for s in nodes_str.split(",") if s.strip() != ""]
            if len(nodes) < 2:
                raise ValueError("Se requieren al menos 2 nodos.")
            nodes = sorted(nodes)
            xi_val = float(eval(xi_str, {"np": np, "pi": np.pi}))
            xd_val = float(eval(xd_str, {"np": np, "pi": np.pi}))

            P, y_vals, L_terms = build_lagrange_polynomial(expr, x, nodes)
            deg = len(nodes) - 1

            # Local error
            f_xi = float(expr.subs(x, xi_val))
            P_xi = float(P.subs(x, xi_val))
            err_local = abs(f_xi - P_xi)

            # Remainder / Cota
            deriv_order = deg + 1
            f_deriv = sp.diff(expr, x, deriv_order)
            # Max de la derivada
            a, b = nodes[0], nodes[-1]
            max_deriv = estimate_max_abs(f_deriv, x, a, b)
            # Producto en xi
            prod_xi, prod_symbolic = product_term(xi_val, nodes, x)
            # Cota local teórica
            bound_local = (max_deriv / sp.factorial(deriv_order)) * abs(prod_xi)
            # Cota global: max |∏(x - x_i)| en [a,b]
            grid = np.linspace(a, b, 1000)
            prod_lamb = sp.lambdify(x, prod_symbolic, "numpy")
            prod_vals = np.abs(prod_lamb(grid))
            max_prod = float(np.max(prod_vals))
            bound_global = (max_deriv / sp.factorial(deriv_order)) * max_prod

            # Derivada numérica central (sobre la malla) y exactas
            deriv_central, metodo_deriv = central_difference(P, x, xd_val, nodes)
            f_prime = sp.diff(expr, x)
            f_prime_exact = float(f_prime.subs(x, xd_val))
            P_prime_exact = float(sp.diff(P, x).subs(x, xd_val))
            err_deriv_central = abs(f_prime_exact - deriv_central) if deriv_central is not None else None

            # ------------------- TEXTO ------------------- #
            T = []
            T.append("=== MODELO DE CONSTRUCCIÓN DEL POLINOMIO DE LAGRANGE ===\n")
            T.append(f"Función: f(x) = {sp.sstr(expr)}")
            T.append(f"Nodos ({len(nodes)}): {nodes}")
            T.append("\n1) Tabla de valores:")
            for xi, yi in zip(nodes, y_vals):
                T.append(f"  x = {xi:.6g}  ->  f(x) = {float(yi):.12g}")

            T.append("\n2) Bases de Lagrange L_i(x):")
            for i, L in enumerate(L_terms):
                T.append(f"  L_{i}(x) = {sp.simplify(L)}")

            T.append("\n3) Polinomio P_n(x) (forma de combinación):")
            comb = " + ".join([f"f(x_{i})*L_{i}(x)" for i in range(len(nodes))])
            T.append(f"  P_{deg}(x) = {comb}")
            T.append("\n4) Reemplazando f(x_i):")
            sum_terms = " + ".join([f"({sp.N(y_vals[i])})*({sp.simplify(L_terms[i])})" for i in range(len(nodes))])
            T.append(f"  P_{deg}(x) = {sum_terms}")
            T.append("\n5) Polinomio expandido y simplificado:")
            T.append(f"  P_{deg}(x) = {sp.expand(P)}")

            T.append("\n6) Evaluación en ξ:")
            T.append(f"  ξ = {xi_val}")
            T.append(f"  f(ξ) = {f_xi:.12g}")
            T.append(f"  P(ξ) = {P_xi:.12g}")
            T.append(f"  Error local |f(ξ)-P(ξ)| = {err_local:.6e}")

            T.append("\n7) Término de resto teórico:")
            T.append(f"  f^{deriv_order}(x) = {sp.simplify(f_deriv)}")
            T.append(f"  Máx |f^{deriv_order}(x)| en [{a},{b}] ≈ {max_deriv:.6g}")
            T.append(f"  Producto ∏(ξ - x_i) = {sp.simplify(prod_symbolic)} evaluado en ξ ⇒ {prod_xi}")
            T.append(f"  Cota local ≤ (Máx deriv / {deriv_order}!) * |∏(ξ - x_i)| = {bound_local:.6e}")
            T.append(f"  Cota global ≤ (Máx deriv / {deriv_order}!) * Máx|∏(x - x_i)| = {bound_global:.6e}")

            T.append("\n8) Derivada en x_d (diferencias centrales sobre la malla / comparación):")
            T.append(f"  x_d = {xd_val}")
            T.append(f"  f'(x) = {sp.simplify(f_prime)}")
            if deriv_central is not None:
                T.append(f"  Aproximación central ({metodo_deriv}): f'(x_d) ≈ {deriv_central:.12g}")
                T.append(f"  P'(x_d) (exacta del polinomio) = {P_prime_exact:.12g}")
                T.append(f"  f'(x_d) exacta = {f_prime_exact:.12g}")
                T.append(f"  |f'(x_d) - deriv_central| = {err_deriv_central:.6e}")
            else:
                T.append("  No se pudo aplicar diferencia central fiable; se usó derivada simbólica del polinomio.")
                T.append(f"  P'(x_d) = {P_prime_exact:.12g}, f'(x_d) = {f_prime_exact:.12g}")

            T.append("\n=== RESUMEN RÁPIDO ===")
            T.append(f"  P_{deg}(x) = {sp.expand(P)}")
            T.append(f"  Error local (ξ={xi_val}) = {err_local:.6e}")
            T.append(f"  Cota local ≈ {bound_local:.6e}")
            T.append(f"  Cota global ≈ {bound_global:.6e}")
            if deriv_central is not None:
                T.append(f"  f'(x_d) ≈ {deriv_central:.6e} (central) | Exacta: {f_prime_exact:.6e}")

            self.text.insert("1.0", "\n".join(T))

            # ------------------- GRÁFICO ------------------- #
            self.ax.clear()
            xs_plot = np.linspace(nodes[0]-0.1*(nodes[-1]-nodes[0]), nodes[-1]+0.1*(nodes[-1]-nodes[0]), 400)
            f_lamb = sp.lambdify(x, expr, "numpy")
            P_lamb = sp.lambdify(x, P, "numpy")
            try:
                self.ax.plot(xs_plot, f_lamb(xs_plot), label="f(x)", color="navy")
            except Exception:
                pass
            self.ax.plot(xs_plot, P_lamb(xs_plot), "--", label=f"P_{deg}(x)", color="darkorange")
            # Nodos
            self.ax.scatter(nodes, [float(v) for v in y_vals], color="red", zorder=5, label="Nodos")
            # Punto ξ
            self.ax.scatter([xi_val], [P_xi], color="green", marker="x", s=80, label="ξ")
            self.ax.set_title("Interpolación de Lagrange")
            self.ax.grid(alpha=0.3)
            self.ax.legend()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))

# ----------------- MAIN ----------------- #
if __name__ == "__main__":
    app = LagrangeGUI()
    app.mainloop()