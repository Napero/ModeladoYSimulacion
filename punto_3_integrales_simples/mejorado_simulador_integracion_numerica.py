# -*- coding: utf-8 -*-
"""
Simulador de Integración Numérica Final
- Métodos: Rectángulo Medio, Trapecio, Simpson 1/3, Simpson 3/8, Boole, Gauss-Legendre
- Tabla compacta, no redimensionable
- Teclado siempre visible
- Gráfica con nodos y opción de mostrar áreas
- Cálculo simbólico y error de truncamiento
- Entrada de constantes simbólicas pi y E
- Botón de ayuda con explicación de fórmulas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure   # <-- AÑADIDO

# ---------------- FUNCIONES AUXILIARES ---------------- #
def f_expr(expr_str):
    x = sp.symbols('x')
    expr_str = expr_str.replace("^","**").replace("pi","sp.pi").replace("π","sp.pi").replace("E","sp.E")
    try:
        return sp.sympify(expr_str), x
    except:
        raise ValueError("Función inválida")

def f_num(expr_str):
    expr, x = f_expr(expr_str)
    return sp.lambdify(x, expr, 'numpy')

def valor_entry(s):
    # Convierte a float, admite pi y E
    s = s.replace("pi","np.pi").replace("π","np.pi").replace("E","np.e")
    return float(eval(s))

# ---------------- MÉTODOS DE INTEGRACIÓN ---------------- #
def regla_rectangulo_medio(f,a,b,n):
    h=(b-a)/n
    xi=a+h/2+np.arange(n)*h
    I=h*np.sum(f(xi))
    tabla=[(i, xi[i], f(xi[i]), "") for i in range(n)]   # i desde 0
    return I,tabla,xi

def regla_trapecio(f,a,b,n):
    h=(b-a)/n
    x=np.linspace(a,b,n+1)
    I=h*(0.5*f(x[0])+np.sum(f(x[1:-1]))+0.5*f(x[-1]))
    tabla=[(i, x[i], f(x[i]), "") for i in range(n+1)]   # i desde 0
    return I,tabla,x

def regla_simpson13(f,a,b,n):
    if n%2!=0: n+=1
    h=(b-a)/n
    x=np.linspace(a,b,n+1)
    I=h/3*(f(x[0])+2*np.sum(f(x[2:-1:2]))+4*np.sum(f(x[1::2]))+f(x[-1]))
    tabla=[(i, x[i], f(x[i]), "") for i in range(n+1)]   # i desde 0
    return I,tabla,x

def regla_simpson38(f,a,b,n):
    if n%3!=0: n+=(3-n%3)
    h=(b-a)/n
    x=np.linspace(a,b,n+1)
    s=f(x[0])+f(x[-1])+3*np.sum(f(x[1:-1][np.arange(1,n)%3!=0]))+2*np.sum(f(x[3:-1:3]))
    I=3*h/8*s
    tabla=[(i, x[i], f(x[i]), "") for i in range(n+1)]   # i desde 0
    return I,tabla,x

def regla_boole(f,a,b,n):
    if n%4!=0: n+=(4-n%4)
    h=(b-a)/n
    x=np.linspace(a,b,n+1)
    s=7*(f(x[0])+f(x[-1])) + 32*np.sum(f(x[1:-1:2])) + 12*np.sum(f(x[2:-2:4])) + 14*np.sum(f(x[4:-1:4]))
    I=2*h/45*s
    tabla=[(i, x[i], f(x[i]), "") for i in range(n+1)]   # i desde 0
    return I,tabla,x

def cuadratura_gauss(f,a,b,n):
    xk,wk=np.polynomial.legendre.leggauss(n)
    x_mapped=0.5*(b-a)*xk + 0.5*(a+b)
    fx=f(x_mapped)
    I=0.5*(b-a)*np.dot(wk,fx)
    tabla=[(i, x_mapped[i], fx[i], wk[i]) for i in range(n)]   # i desde 0
    return I,tabla,x_mapped

# ---------------- ERROR DE TRUNCAMIENTO ---------------- #
def error_truncamiento(expr_str, regla, a, b, n):
    x=sp.symbols('x')
    expr,_=f_expr(expr_str)
    orden={"Trapecio":2,"Simpson 1/3":4,"Simpson 3/8":4,"Boole":6,"Rectángulo Medio":2}
    if regla not in orden: return "No disponible", None
    deriv=sp.diff(expr,x,orden[regla])
    deriv_max=sp.lambdify(x,sp.Abs(deriv),"numpy")
    xs=np.linspace(a,b,200)
    M=np.max(deriv_max(xs))
    h=(b-a)/n
    if regla=="Trapecio": return "-(b-a)/12*h²*f''(ξ)", -((b-a)/12)*h**2*M
    elif regla=="Simpson 1/3": return "-(b-a)/180*h⁴*f''''(ξ)", -((b-a)/180)*h**4*M
    elif regla=="Simpson 3/8": return "-(b-a)/80*h⁴*f''''(ξ)", -((b-a)/80)*h**4*M
    elif regla=="Boole": return "-(b-a)/9450*h⁶*f⁶(ξ)", -((b-a)/9450)*h**6*M
    elif regla=="Rectángulo Medio": return "-(b-a)/24*h²*f''(ξ)", -((b-a)/24)*h**2*M
    else: return "No disponible", None

# ---------------- NUEVAS FUNCIONES DETALLADAS (Ejercicio 3) ---------------- #
def trapecio_detallado(expr_str, a, b, n):
    """
    Devuelve (I_aprox, texto_desarrollo, tabla_nodos)
    tabla_nodos: lista de (i, x_i, f(x_i))
    """
    expr_sym, x = f_expr(expr_str)
    f = sp.lambdify(x, expr_sym, 'numpy')
    h = (b - a) / n
    xs = np.linspace(a, b, n+1)
    fx = f(xs)
    suma_interior = np.sum(fx[1:-1])
    I = h * (0.5*fx[0] + suma_interior + 0.5*fx[-1])
    texto = []
    texto.append(f"--- Trapecio compuesto (n = {n}) ---")
    texto.append(f"h = (b-a)/n = ({b}-{a})/{n} = {h:.6f}")
    texto.append("Nodos y valores f(x_i):")
    for i, (xx, ff) in enumerate(zip(xs, fx)):
        texto.append(f"  i={i:2d}  x_{i}={xx:.6f}  f(x_{i})={ff:.10f}")
    texto.append(f"Suma interior Σ f(x_i) (i=1..n-1) = {suma_interior:.10f}")
    texto.append(f"I_T = h * [ 0.5 f(x0) + Σ f(xi) + 0.5 f(xn) ]")
    texto.append(f"I_T = {h:.6f} * [0.5*{fx[0]:.10f} + {suma_interior:.10f} + 0.5*{fx[-1]:.10f}] = {I:.10f}")
    return I, "\n".join(texto), [(i, xs[i], fx[i]) for i in range(len(xs))]

def simpson13_detallado(expr_str, a, b, n):
    """
    Detalle Simpson 1/3 compuesto (ajusta n a par si no lo es).
    Devuelve (n_real, I_aprox, texto, tabla_nodos)
    """
    expr_sym, x = f_expr(expr_str)
    f = sp.lambdify(x, expr_sym, 'numpy')
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    xs = np.linspace(a, b, n+1)
    fx = f(xs)
    pares = fx[2:-1:2]
    impares = fx[1::2]
    I = h/3 * (fx[0] + 2*np.sum(pares) + 4*np.sum(impares) + fx[-1])
    texto = []
    texto.append(f"--- Simpson 1/3 compuesto (n = {n}) ---")
    texto.append(f"h = (b-a)/n = ({b}-{a})/{n} = {h:.6f}")
    texto.append("Clasificación de nodos:")
    for i, (xx, ff) in enumerate(zip(xs, fx)):
        if i == 0 or i == n:
            w = "1 (extremo)"
        elif i % 2 == 0:
            w = "2 (par)"
        else:
            w = "4 (impar)"
        texto.append(f"  i={i:2d}  x_{i}={xx:.6f}  f(x_{i})={ff:.10f}  peso={w}")
    texto.append("Fórmula: I ≈ h/3 [ f0 + 4 f1 + 2 f2 + 4 f3 + ... + fn ]")
    texto.append(f"Suma pares (coef 2): {np.sum(pares):.10f}")
    texto.append(f"Suma impares (coef 4): {np.sum(impares):.10f}")
    texto.append(f"I_S = {h:.6f}/3 * ( {fx[0]:.10f} + 2*{np.sum(pares):.10f} + 4*{np.sum(impares):.10f} + {fx[-1]:.10f} ) = {I:.10f}")
    return n, I, "\n".join(texto), [(i, xs[i], fx[i]) for i in range(len(xs))]

def error_teorico_trapecio_en_xi(expr_str, a, b, n, xi):
    """
    Error teórico usando E ≈ -(b-a)/12 * h^2 * f''(ξ)
    """
    expr_sym, x = f_expr(expr_str)
    f2 = sp.diff(expr_sym, x, 2)
    h = (b - a) / n
    f2_xi = float(sp.N(f2.subs(x, xi)))
    E = - (b - a)/12 * h**2 * f2_xi
    return f2, f2_xi, E

def error_teorico_simpson_en_xi(expr_str, a, b, n, xi):
    """
    Error Simpson 1/3: E ≈ -(b-a)/180 * h^4 * f^{(4)}(ξ)
    """
    expr_sym, x = f_expr(expr_str)
    f4 = sp.diff(expr_sym, x, 4)
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    f4_xi = float(sp.N(f4.subs(x, xi)))
    E = - (b - a)/180 * h**4 * f4_xi
    return f4, f4_xi, E

# ---------------- (MODIFICADO) INTERFAZ ---------------- #
class Simulador:
    def __init__(self,root):
        self.root=root
        self.root.title("Simulador Integración Numérica Final")
        self.root.geometry("1420x760")

        # Notebook: pestaña original + pestaña Ejercicio 3
        self.nb = ttk.Notebook(root)
        self.nb.pack(fill="both", expand=True)

        self.frame_main = ttk.Frame(self.nb)
        self.nb.add(self.frame_main, text="Simulador General")

        self.frame_ej3 = ttk.Frame(self.nb)
        self.nb.add(self.frame_ej3, text="Ejercicio 3 Paso a Paso")

        self._build_main_ui()
        self._build_ej3_ui()

    # ---------------- UI ORIGINAL (sin cambios funcionales previos) ---------------- #
    def _build_main_ui(self):
        frame = self.frame_main
        panel_left=ttk.Frame(frame,padding=10)
        panel_left.pack(side="left",fill="y")

        ttk.Label(panel_left,text="f(x):").grid(row=0,column=0)
        self.funcion_entry=ttk.Entry(panel_left,width=25); self.funcion_entry.grid(row=0,column=1); self.funcion_entry.insert(0,"sin(x)")
        ttk.Label(panel_left,text="a:").grid(row=1,column=0)
        self.a_entry=ttk.Entry(panel_left,width=10); self.a_entry.grid(row=1,column=1); self.a_entry.insert(0,"0")
        ttk.Label(panel_left,text="b:").grid(row=2,column=0)
        self.b_entry=ttk.Entry(panel_left,width=10); self.b_entry.grid(row=2,column=1); self.b_entry.insert(0,"pi")
        ttk.Label(panel_left,text="n:").grid(row=3,column=0)
        self.n_entry=ttk.Entry(panel_left,width=10); self.n_entry.grid(row=3,column=1); self.n_entry.insert(0,"5")

        ttk.Label(panel_left,text="Método:").grid(row=4,column=0)
        self.metodo_combo=ttk.Combobox(panel_left,values=["Rectángulo Medio","Trapecio","Simpson 1/3","Simpson 3/8","Boole","Gauss-Legendre"])
        self.metodo_combo.grid(row=4,column=1)
        self.metodo_combo.current(0)

        ttk.Button(panel_left,text="Calcular",command=self.calcular).grid(row=5,column=0,columnspan=2,pady=5)
        ttk.Button(panel_left,text="Graficar",command=self.graficar).grid(row=6,column=0,columnspan=2,pady=5)
        self.show_area_var=tk.IntVar()
        ttk.Checkbutton(panel_left,text="Mostrar áreas",variable=self.show_area_var,command=self.graficar).grid(row=7,column=0,columnspan=2)
        ttk.Button(panel_left,text="Ayuda",command=self.mostrar_ayuda).grid(row=8,column=0,columnspan=2,pady=5)

        teclado_frame=ttk.LabelFrame(panel_left,text="Teclado")
        teclado_frame.grid(row=9,column=0,columnspan=2,pady=5)
        botones=["sin","cos","tan","exp","log","sqrt","pi","E","^","(",")","x"]
        for i,b in enumerate(botones):
            ttk.Button(teclado_frame,text=b,command=lambda b=b:self.insertar(b)).grid(row=i//3,column=i%3,padx=2,pady=2)

        panel_right=ttk.Frame(frame)
        panel_right.pack(side="right",fill="both",expand=True)

        self.result_label=ttk.Label(panel_right,text="Resultado: "); self.result_label.pack(anchor="w")
        self.simbol_label=ttk.Label(panel_right,text="Integral simbólica: "); self.simbol_label.pack(anchor="w")
        self.error_label=ttk.Label(panel_right,text="Error: "); self.error_label.pack(anchor="w")

        self.tree=ttk.Treeview(panel_right,columns=("i","x","f(x)","w"),show="headings",height=12)
        for c,t in zip(("i","x","f(x)","w"),("i","x","f(x)","Peso w_i")):
            self.tree.heading(c,text=t)
            self.tree.column(c,width=90,anchor="center")
        self.tree.pack(fill="x",pady=5)

        self.fig, self.ax=plt.subplots(figsize=(6,4))
        self.canvas=FigureCanvasTkAgg(self.fig,panel_right)
        self.canvas.get_tk_widget().pack(fill="both",expand=True)

    # ---------------- NUEVA PESTAÑA EJERCICIO 3 ---------------- #
    def _build_ej3_ui(self):
        frame = self.frame_ej3

        # Panel de entrada
        panel_in = ttk.LabelFrame(frame, text="Parámetros Ejercicio 3")
        panel_in.pack(side="top", fill="x", padx=5, pady=5)

        ttk.Label(panel_in, text="f(x):").grid(row=0, column=0, sticky="e", padx=3, pady=2)
        self.ej3_func = ttk.Entry(panel_in, width=28)
        self.ej3_func.grid(row=0, column=1, padx=3, pady=2)
        self.ej3_func.insert(0, "sqrt(2)*exp(x)")

        ttk.Label(panel_in, text="a:").grid(row=0, column=2, sticky="e")
        self.ej3_a = ttk.Entry(panel_in, width=8); self.ej3_a.grid(row=0,column=3); self.ej3_a.insert(0,"0")
        ttk.Label(panel_in, text="b:").grid(row=0, column=4, sticky="e")
        self.ej3_b = ttk.Entry(panel_in, width=8); self.ej3_b.grid(row=0,column=5); self.ej3_b.insert(0,"1")

        ttk.Label(panel_in, text="n Trap 1:").grid(row=1, column=0, sticky="e")
        self.ej3_n1 = ttk.Entry(panel_in, width=8); self.ej3_n1.grid(row=1,column=1); self.ej3_n1.insert(0,"4")
        ttk.Label(panel_in, text="n Trap 2:").grid(row=1, column=2, sticky="e")
        self.ej3_n2 = ttk.Entry(panel_in, width=8); self.ej3_n2.grid(row=1,column=3); self.ej3_n2.insert(0,"10")
        ttk.Label(panel_in, text="n Simpson:").grid(row=1, column=4, sticky="e")
        self.ej3_ns = ttk.Entry(panel_in, width=8); self.ej3_ns.grid(row=1,column=5); self.ej3_ns.insert(0,"4")

        ttk.Label(panel_in, text="ξ (errores):").grid(row=2, column=0, sticky="e")
        self.ej3_xi = ttk.Entry(panel_in, width=8); self.ej3_xi.grid(row=2,column=1); self.ej3_xi.insert(0,"0.5")

        ttk.Button(panel_in, text="Generar Informe Paso a Paso", command=self.generar_ej3).grid(row=2, column=2, columnspan=2, padx=4, pady=4)
        ttk.Button(panel_in, text="Graficar", command=self.graficar_ej3).grid(row=2, column=4, columnspan=2, padx=4, pady=4)

        # Texto desarrollo
        panel_text = ttk.LabelFrame(frame, text="Desarrollo Detallado")
        panel_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.ej3_text = ScrolledText(panel_text, wrap="word", font=("Consolas", 10))
        self.ej3_text.pack(fill="both", expand=True)

        # Gráfico
        panel_plot = ttk.LabelFrame(frame, text="Gráfico f(x)")
        panel_plot.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.fig_ej3 = Figure(figsize=(5.8,5), dpi=100)
        self.ax_ej3 = self.fig_ej3.add_subplot(111)
        self.canvas_ej3 = FigureCanvasTkAgg(self.fig_ej3, master=panel_plot)
        self.canvas_ej3.get_tk_widget().pack(fill="both", expand=True)

    # ---------------- LÓGICA EJERCICIO 3 ---------------- #
    def generar_ej3(self):
        self.ej3_text.delete("1.0", tk.END)
        try:
            expr_str = self.ej3_func.get().strip()
            a = valor_entry(self.ej3_a.get())
            b = valor_entry(self.ej3_b.get())
            n1 = int(self.ej3_n1.get())
            n2 = int(self.ej3_n2.get())
            ns = int(self.ej3_ns.get())
            xi = float(self.ej3_xi.get())

            expr_sym, x = f_expr(expr_str)
            integral_exacta = sp.integrate(expr_sym, (x, a, b))
            I_exact = float(sp.N(integral_exacta))

            # Trapecio n1
            It1, txt1, _ = trapecio_detallado(expr_str, a, b, n1)
            f2, f2_xi_1, Eteo1 = error_teorico_trapecio_en_xi(expr_str, a, b, n1, xi)
            E_real1 = I_exact - It1

            # Trapecio n2
            It2, txt2, _ = trapecio_detallado(expr_str, a, b, n2)
            f2, f2_xi_2, Eteo2 = error_teorico_trapecio_en_xi(expr_str, a, b, n2, xi)
            E_real2 = I_exact - It2

            # Simpson
            ns_real, Is, txtS, _ = simpson13_detallado(expr_str, a, b, ns)
            f4, f4_xi, E_simpson_teo = error_teorico_simpson_en_xi(expr_str, a, b, ns_real, xi)
            E_realS = I_exact - Is

            # Relación de errores trapecio (teórico y real)
            rel_teo = abs(Eteo1 / Eteo2) if Eteo2 != 0 else float('inf')
            rel_real = abs(E_real1 / E_real2) if E_real2 != 0 else float('inf')
            esperado = ((b - a)/n1) / ((b - a)/n2)
            esperado = esperado**2  # orden h^2

            # Armar informe
            L=[]
            L.append("=== EJERCICIO 3: INTEGRACIÓN NUMÉRICA DETALLADA ===\n")
            L.append(f"Función f(x) = {sp.sstr(expr_sym)}")
            L.append(f"Intervalo: [{a}, {b}]")
            L.append(f"Integral exacta (simbólica) = {integral_exacta} ≈ {I_exact:.10f}")
            L.append(f"ξ usado para errores teóricos: ξ = {xi}\n")

            L.append(txt1)
            L.append(f"\nDerivada segunda f''(x) = {sp.simplify(sp.diff(expr_sym,x,2))}")
            L.append(f"f''(ξ) = {f2_xi_1:.10f}")
            L.append(f"Error teórico trapecio (n={n1}): E ≈ - (b-a)/12 * h^2 * f''(ξ) = {Eteo1:.6e}")
            L.append(f"Error real trapecio (n={n1}): I_exact - I_T = {E_real1:.6e}")

            L.append("\n" + txt2)
            L.append(f"\n(f''(ξ) igual porque ξ fijo) Error teórico trapecio (n={n2}) = {Eteo2:.6e}")
            L.append(f"Error real trapecio (n={n2}) = {E_real2:.6e}")

            L.append("\nComparación reducción de error Trapecio:")
            L.append(f"Relación teórica E(n1)/E(n2) = {rel_teo:.4f} | Esperado ≈ ((h1)/(h2))^2 = {esperado:.4f}")
            L.append(f"Relación real    E(n1)/E(n2) = {rel_real:.4f}")

            L.append("\n" + txtS)
            L.append(f"\nDerivada cuarta f''''(x) = {sp.simplify(sp.diff(expr_sym,x,4))}")
            L.append(f"f''''(ξ) = {f4_xi:.10f}")
            L.append(f"Error teórico Simpson 1/3 (n={ns_real}) = {E_simpson_teo:.6e}")
            L.append(f"Error real Simpson 1/3 (n={ns_real}) = {E_realS:.6e}")

            L.append("\nComparación final (precisión):")
            L.append(f"Trapecio n={n1}: I_T = {It1:.10f}  | Error real = {E_real1:.2e}")
            L.append(f"Trapecio n={n2}: I_T = {It2:.10f}  | Error real = {E_real2:.2e}")
            L.append(f"Simpson  n={ns_real}: I_S = {Is:.10f} | Error real = {E_realS:.2e}")
            L.append("\nConclusión: Simpson 1/3 mejora el orden (O(h^4)) y ofrece menor error con la misma n respecto a Trapecio (O(h^2)).")

            self.ej3_text.insert("1.0", "\n".join(L))

        except Exception as e:
            messagebox.showerror("Error Ej3", str(e))

    def graficar_ej3(self):
        try:
            expr_str = self.ej3_func.get().strip()
            a = valor_entry(self.ej3_a.get())
            b = valor_entry(self.ej3_b.get())
            expr_sym, x = f_expr(expr_str)
            f = sp.lambdify(x, expr_sym, 'numpy')
            xs_plot = np.linspace(a, b, 400)
            ys = f(xs_plot)
            self.ax_ej3.clear()
            self.ax_ej3.plot(xs_plot, ys, label="f(x)", color="navy")
            # Nodos trapecio n1 y n2 y Simpson (solo para referencia)
            n1 = int(self.ej3_n1.get())
            n2 = int(self.ej3_n2.get())
            ns = int(self.ej3_ns.get())
            xs1 = np.linspace(a, b, n1+1)
            xs2 = np.linspace(a, b, n2+1)
            if ns % 2 != 0: ns += 1
            xsS = np.linspace(a, b, ns+1)
            self.ax_ej3.scatter(xs1, f(xs1), color="red", label=f"Nodos Trap n={n1}")
            self.ax_ej3.scatter(xs2, f(xs2), color="orange", label=f"Nodos Trap n={n2}", s=20)
            self.ax_ej3.scatter(xsS, f(xsS), color="green", label=f"Nodos Simpson n={ns}", s=15, marker="x")
            self.ax_ej3.set_title("f(x) y nodos usados (Ejercicio 3)")
            self.ax_ej3.grid(alpha=0.3)
            self.ax_ej3.legend()
            self.canvas_ej3.draw()
        except Exception as e:
            messagebox.showerror("Error Gráfico Ej3", str(e))

    # ---------------- (resto de métodos originales sin cambios) ---------------- #
    def insertar(self,texto):
        self.funcion_entry.insert(tk.END,texto)

    def mostrar_ayuda(self):
        ayuda_win=tk.Toplevel(self.root)
        ayuda_win.title("Ayuda: Métodos de Integración")
        ayuda_win.geometry("500x400")
        texto=("Métodos disponibles:\n\n"
               "Rectángulo Medio:\n  I ≈ h * Σ f(x_i*), h=(b-a)/n, x_i* = centro de subintervalo\n\n"
               "Trapecio:\n  I ≈ h*(f(x0)/2 + Σ f(xi) + f(xn)/2), h=(b-a)/n\n\n"
               "Simpson 1/3:\n  I ≈ h/3*(f0 + 4f1 + 2f2 + 4f3 + ... + fn), n par\n\n"
               "Simpson 3/8:\n  I ≈ 3h/8*(f0 + 3f1 + 3f2 + 2f3 + ... + fn), n múltiplo de 3\n\n"
               "Boole:\n  I ≈ 2h/45*(7f0 + 32f1 + 12f2 + 32f3 + 14f4 + ... + 7fn), n múltiplo de 4\n\n"
               "Gauss-Legendre:\n  I ≈ Σ w_i * f(x_i), x_i y w_i son los nodos y pesos de Gauss\n\n"
               "Nota: puede ingresar 'pi' o 'π' como valor de a o b.")
        label=ttk.Label(ayuda_win,text=texto,justify="left")
        label.pack(padx=10,pady=10)

    def calcular(self):
        try:
            f=f_num(self.funcion_entry.get())
            a=valor_entry(self.a_entry.get())
            b=valor_entry(self.b_entry.get())
            n=int(self.n_entry.get())
            metodo=self.metodo_combo.get()

            if metodo=="Rectángulo Medio": I,tabla,xs=regla_rectangulo_medio(f,a,b,n); regla="Rectángulo Medio"
            elif metodo=="Trapecio": I,tabla,xs=regla_trapecio(f,a,b,n); regla="Trapecio"
            elif metodo=="Simpson 1/3": I,tabla,xs=regla_simpson13(f,a,b,n); regla="Simpson 1/3"
            elif metodo=="Simpson 3/8": I,tabla,xs=regla_simpson38(f,a,b,n); regla="Simpson 3/8"
            elif metodo=="Boole": I,tabla,xs=regla_boole(f,a,b,n); regla="Boole"
            elif metodo=="Gauss-Legendre": I,tabla,xs=cuadratura_gauss(f,a,b,n); regla="Gauss"
            else: raise ValueError("Método no válido")

            expr,_=f_expr(self.funcion_entry.get())
            integral_simbol=sp.integrate(expr,(sp.symbols('x'),a,b))
            self.simbol_label.config(text=f"Integral simbólica: {integral_simbol}")

            formula,err=error_truncamiento(self.funcion_entry.get(),regla,a,b,n)
            self.result_label.config(text=f"Resultado numérico: {I:.6f}")
            if err is not None: self.error_label.config(text=f"Error: {formula}, Valor ≈ {err:.6e}")
            else: self.error_label.config(text="Error: No disponible")

            for row in self.tree.get_children(): self.tree.delete(row)
            for t in tabla: 
                self.tree.insert("", "end", values=(t[0], f"{t[1]:.6f}", f"{t[2]:.6f}", f"{t[3]}" if t[3]!="" else ""))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def graficar(self):
        try:
            self.ax.clear()
            f=f_num(self.funcion_entry.get())
            a=valor_entry(self.a_entry.get())
            b=valor_entry(self.b_entry.get())
            n=int(self.n_entry.get())
            xs_plot=np.linspace(a,b,400)
            ys_plot=f(xs_plot)
            self.ax.plot(xs_plot,ys_plot,label="f(x)",color="blue")
            self.ax.axhline(0,color="black")
            self.ax.axvline(0,color="black")
            self.ax.grid(True)
            self.ax.legend()
            self.ax.set_title("Gráfico de f(x) con nodos y áreas")

            metodo=self.metodo_combo.get()
            if metodo=="Rectángulo Medio":
                xi=a+(b-a)/(2*n)+np.arange(n)*(b-a)/n
            elif metodo in ["Trapecio","Simpson 1/3","Simpson 3/8","Boole"]:
                xi=np.linspace(a,b,n+1)
            elif metodo=="Gauss-Legendre":
                xi,_=cuadratura_gauss(f,a,b,n)[2],None
            self.ax.scatter(xi,f(xi),color="red",zorder=5,label="Nodos")

            if self.show_area_var.get() and metodo!="Gauss-Legendre":
                h=(b-a)/n
                for i in range(len(xi)-1):
                    x_fill=np.linspace(xi[i],xi[i+1],20)
                    y_fill=f(x_fill)
                    color="orange"
                    if metodo=="Trapecio": color="orange"
                    elif metodo=="Simpson 1/3": color="green"
                    elif metodo=="Simpson 3/8": color="purple"
                    elif metodo=="Boole": color="pink"
                    elif metodo=="Rectángulo Medio":
                        x_fill=[xi[i]-h/2,xi[i]+h/2]
                        y_fill=[f(xi[i]),f(xi[i])]
                    self.ax.fill_between(x_fill,0,y_fill,color=color,alpha=0.3)

            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__=="__main__":
    root=tk.Tk()
    app=Simulador(root)
    root.mainloop()


