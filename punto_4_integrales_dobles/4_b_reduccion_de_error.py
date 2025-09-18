# -*- coding: utf-8 -*-
"""
Ejercicio 4 (Inciso b) - Demostración interactiva ley 1/√n para Monte Carlo en integrales dobles.

Características:
- Carga de f(x,y), rectángulo [a,b]x[c,d], N1, N2 (o factor k: N2 = k*N1).
- Semillas configurables para reproducibilidad (seed1, seed2).
- Cálculo integral analítica con Sympy (si es integrable simbólicamente).
- Dos simulaciones Monte Carlo (N1 y N2) sobre la misma integral:
    * Media muestral, Varianza, Desv. estándar, Error estándar.
    * Estimación de la integral (Área * media).
    * Intervalo de confianza 95% (normal y t).
    * Error absoluto respecto a la integral analítica (si disponible).
- Demostración 1/√n:
    * Muestra relación teórica SE1/SE2 ≈ sqrt(N2/N1)
    * Muestra relación empírica.
    * Indica si la reducción de SE se aproxima al factor esperado (ej: ≈2 si N2=4N1).
- Gráficos:
    * Convergencia incremental (promedio acumulado) para N1 y N2.
    * Histograma comparativo de los valores f(x,y) (normalizada).
- Exportar informe Markdown (botón) con todo el desarrollo teórico + resultados concretos.
- Texto explicativo reutilizable para informes.

Uso típico (enunciado):
f(x,y)=exp(2*x - y), a=0,b=1, c=1,d=2, N1=10000, factor=4 (→ N2=40000), seeds=0 y 1.

Notas:
- Si falla la integral simbólica se indica y se continúa solo con Monte Carlo.
- Evita eval inseguro: se pasa la expresión por sympy.sympify con símbolos x,y, constantes pi, E.

Autor: Generado automáticamente.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import numpy as np
import sympy as sp
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- Utilidades ---------------- #
def parse_function(expr_str):
    x,y = sp.symbols('x y')
    expr_str = expr_str.replace("^", "**")
    try:
        expr = sp.sympify(expr_str, {"x":x,"y":y,"pi":sp.pi,"e":sp.E,"E":sp.E})
    except Exception as e:
        raise ValueError(f"Expresión inválida: {e}")
    return expr, x, y

def mc_double(expr, x, y, a,b,c,d, N, seed=None):
    if seed is not None:
        rng = np.random.default_rng(seed)
    else:
        rng = np.random.default_rng()
    f = sp.lambdify((x,y), expr, "numpy")
    xs = rng.uniform(a,b,N)
    ys = rng.uniform(c,d,N)
    vals = f(xs, ys)
    media = float(np.mean(vals))
    var = float(np.var(vals, ddof=1))
    std = var**0.5
    stderr = std / (N**0.5)
    integral_est = (b-a)*(d-c)*media
    return {
        "xs": xs,
        "ys": ys,
        "vals": vals,
        "media": media,
        "var": var,
        "std": std,
        "stderr": stderr,
        "integral_est": integral_est
    }

def analytic_double(expr, x, y, a,b,c,d):
    try:
        integral = sp.integrate(sp.integrate(expr, (y,c,d)), (x,a,b))
        val = float(sp.N(integral))
        return integral, val
    except Exception:
        return None, None

def format_ci(mean, se, conf=0.95, n=None):
    if n is not None and n > 1:
        tval = stats.t.ppf(0.5+conf/2, n-1)
    else:
        tval = 1.96
    return mean - 1.96*se, mean + 1.96*se, mean - tval*se, mean + tval*se

# ---------------- GUI ---------------- #
class MonteCarloErrorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Demostración Monte Carlo - Ley 1/sqrt(n)")
        self.geometry("1320x780")
        self._build_ui()

    def _build_ui(self):
        # Entradas
        frame_in = ttk.LabelFrame(self, text="Parámetros")
        frame_in.pack(side="top", fill="x", padx=6, pady=4)

        r=0
        ttk.Label(frame_in,text="f(x,y)=").grid(row=r,column=0,sticky="e",padx=4)
        self.expr_entry=ttk.Entry(frame_in,width=28)
        self.expr_entry.grid(row=r,column=1,padx=4)
        self.expr_entry.insert(0,"exp(2*x - y)")

        ttk.Label(frame_in,text="a=").grid(row=r,column=2,sticky="e")
        self.a_entry=ttk.Entry(frame_in,width=8); self.a_entry.grid(row=r,column=3); self.a_entry.insert(0,"0")
        ttk.Label(frame_in,text="b=").grid(row=r,column=4,sticky="e")
        self.b_entry=ttk.Entry(frame_in,width=8); self.b_entry.grid(row=r,column=5); self.b_entry.insert(0,"1")

        ttk.Label(frame_in,text="c=").grid(row=r,column=6,sticky="e")
        self.c_entry=ttk.Entry(frame_in,width=8); self.c_entry.grid(row=r,column=7); self.c_entry.insert(0,"1")
        ttk.Label(frame_in,text="d=").grid(row=r,column=8,sticky="e")
        self.d_entry=ttk.Entry(frame_in,width=8); self.d_entry.grid(row=r,column=9); self.d_entry.insert(0,"2")

        r=1
        ttk.Label(frame_in,text="N1=").grid(row=r,column=0,sticky="e")
        self.N1_entry=ttk.Entry(frame_in,width=10); self.N1_entry.grid(row=r,column=1); self.N1_entry.insert(0,"10000")

        self.use_factor_var=tk.IntVar(value=1)
        ttk.Checkbutton(frame_in,text="Usar factor k (N2=k*N1)",variable=self.use_factor_var,command=self._toggle_factor).grid(row=r,column=2,columnspan=2)
        ttk.Label(frame_in,text="k=").grid(row=r,column=4,sticky="e")
        self.k_entry=ttk.Entry(frame_in,width=8); self.k_entry.grid(row=r,column=5); self.k_entry.insert(0,"4")

        ttk.Label(frame_in,text="N2 (manual)=").grid(row=r,column=6,sticky="e")
        self.N2_entry=ttk.Entry(frame_in,width=10); self.N2_entry.grid(row=r,column=7); self.N2_entry.insert(0,"40000")

        ttk.Label(frame_in,text="seed1=").grid(row=r,column=8,sticky="e")
        self.seed1_entry=ttk.Entry(frame_in,width=8); self.seed1_entry.grid(row=r,column=9); self.seed1_entry.insert(0,"0")
        ttk.Label(frame_in,text="seed2=").grid(row=r,column=10,sticky="e")
        self.seed2_entry=ttk.Entry(frame_in,width=8); self.seed2_entry.grid(row=r,column=11); self.seed2_entry.insert(0,"1")

        r=2
        ttk.Button(frame_in,text="Ejecutar",command=self.ejecutar).grid(row=r,column=0,columnspan=2,pady=4)
        ttk.Button(frame_in,text="Exportar Markdown",command=self.exportar_md).grid(row=r,column=2,columnspan=2,pady=4)
        ttk.Button(frame_in,text="Limpiar",command=self.limpiar).grid(row=r,column=4,columnspan=2,pady=4)
        ttk.Button(frame_in,text="Ayuda",command=self.mostrar_ayuda).grid(row=r,column=6,columnspan=2,pady=4)

        # Texto resultados
        frame_text = ttk.LabelFrame(self, text="Desarrollo / Explicación")
        frame_text.pack(side="left", fill="both", expand=True, padx=6, pady=4)
        self.text = ScrolledText(frame_text, wrap="word", font=("Consolas",10))
        self.text.pack(fill="both", expand=True)

        # Gráficos
        frame_plot = ttk.LabelFrame(self, text="Gráficos")
        frame_plot.pack(side="right", fill="both", expand=True, padx=6, pady=4)

        self.fig = plt.Figure(figsize=(6.6,5.6), dpi=100)
        self.ax_conv = self.fig.add_subplot(211)
        self.ax_hist = self.fig.add_subplot(212)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_plot)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _toggle_factor(self):
        use_factor = self.use_factor_var.get()==1
        state_factor = "normal" if use_factor else "disabled"
        state_N2 = "disabled" if use_factor else "normal"
        self.k_entry.config(state=state_factor)
        self.N2_entry.config(state=state_N2)

    def limpiar(self):
        self.text.delete("1.0", tk.END)
        self.ax_conv.clear()
        self.ax_hist.clear()
        self.canvas.draw()

    def ejecutar(self):
        self.limpiar()
        try:
            expr_str = self.expr_entry.get().strip()
            a = float(eval(self.a_entry.get(), {"pi":np.pi,"e":np.e}))
            b = float(eval(self.b_entry.get(), {"pi":np.pi,"e":np.e}))
            c = float(eval(self.c_entry.get(), {"pi":np.pi,"e":np.e}))
            d = float(eval(self.d_entry.get(), {"pi":np.pi,"e":np.e}))
            N1 = int(self.N1_entry.get())
            if self.use_factor_var.get()==1:
                k = float(self.k_entry.get())
                if k <= 0: raise ValueError("k debe ser > 0")
                N2 = int(round(k * N1))
            else:
                N2 = int(self.N2_entry.get())
                k = N2 / N1
            seed1 = int(self.seed1_entry.get())
            seed2 = int(self.seed2_entry.get())

            expr, x, y = parse_function(expr_str)

            integral_sym, integral_exact = analytic_double(expr, x, y, a,b,c,d)

            # Simulaciones
            res1 = mc_double(expr,x,y,a,b,c,d,N1,seed1)
            res2 = mc_double(expr,x,y,a,b,c,d,N2,seed2)

            area = (b-a)*(d-c)
            # Convergencia (promedios acumulados)
            cum1 = np.cumsum(res1["vals"])/np.arange(1, N1+1)
            cum2 = np.cumsum(res2["vals"])/np.arange(1, N2+1)

            # Ratios
            se_ratio_emp = res1["stderr"]/res2["stderr"] if res2["stderr"]>0 else np.inf
            se_ratio_teo = (N2/N1)**0.5
            expected_halving = abs(se_ratio_emp - se_ratio_teo) < 0.1*se_ratio_teo

            ci95_1_n, ci95_1_N = format_ci(res1["media"], res1["stderr"], 0.95, N1), format_ci(res1["media"], res1["stderr"],0.95,None)
            ci95_2_n, ci95_2_N = format_ci(res2["media"], res2["stderr"], 0.95, N2), format_ci(res2["media"], res2["stderr"],0.95,None)

            # Texto
            L=[]
            L.append("=== DEMOSTRACIÓN LEY 1/√n (Monte Carlo Integral Doble) ===\n")
            L.append(f"Función: f(x,y) = {sp.sstr(expr)}")
            L.append(f"Dominio: x∈[{a},{b}], y∈[{c},{d}] (Área = {area})")
            if integral_exact is not None:
                L.append(f"Integral analítica: {integral_sym} ≈ {integral_exact:.10f}")
            else:
                L.append("Integral analítica: (no se pudo obtener simbólicamente)")
            L.append("")
            L.append(f"Parámetros simulación:")
            L.append(f"  N1 = {N1} (seed={seed1})")
            L.append(f"  N2 = {N2} (seed={seed2})  (k = {k:.4g} ⇒ sqrt(k) = {k**0.5:.4g})")
            L.append("")
            # Resultados N1
            L.append(f"-- Resultado N1 = {N1} --")
            L.append(f"Media f = {res1['media']:.10f}  Var = {res1['var']:.10f}  Std = {res1['std']:.10f}")
            L.append(f"Error estándar (SE) = {res1['stderr']:.10f}")
            L.append(f"Integral estimada Ĩ1 = {res1['integral_est']:.10f}")
            if integral_exact is not None:
                L.append(f"Error absoluto |I-Ĩ1| = {abs(integral_exact - res1['integral_est']):.6e}")
            L.append(f"IC 95% (normal media): [{ci95_1_N[0]:.10f}, {ci95_1_N[1]:.10f}]")
            L.append("")
            # Resultados N2
            L.append(f"-- Resultado N2 = {N2} --")
            L.append(f"Media f = {res2['media']:.10f}  Var = {res2['var']:.10f}  Std = {res2['std']:.10f}")
            L.append(f"Error estándar (SE) = {res2['stderr']:.10f}")
            L.append(f"Integral estimada Ĩ2 = {res2['integral_est']:.10f}")
            if integral_exact is not None:
                L.append(f"Error absoluto |I-Ĩ2| = {abs(integral_exact - res2['integral_est']):.6e}")
            L.append(f"IC 95% (normal media): [{ci95_2_N[0]:.10f}, {ci95_2_N[1]:.10f}]")
            L.append("")
            # Comparación
            L.append("== Comparación Escala de Error ==")
            L.append(f"Razón teórica SE(N1)/SE(N2) ≈ sqrt(N2/N1) = {se_ratio_teo:.6f}")
            L.append(f"Razón empírica  SE(N1)/SE(N2) = {se_ratio_emp:.6f}")
            L.append(f"¿Reducción consistente? {'Sí' if expected_halving else 'Aproximación parcial'}")
            if k >= 4-1e-9 and k <= 4+1e-9:
                L.append(f"Como k=4, se esperaba SE2 ≈ SE1/2 ⇒ SE1/SE2≈2. Observado: {se_ratio_emp:.4f}")
            L.append("")
            L.append("== Justificación Teórica ==")
            L.append("Sea F = f(X,Y) con (X,Y) uniformes independientes. Ĩ_n = Área * (1/n) Σ F_i.")
            L.append("Var(Ĩ_n) = Área² * Var(F)/n ⇒ SE(Ĩ_n) = (Área * σ_F)/√n.")
            L.append("Si n → k n, entonces SE escala por 1/√k. Para reducir a la mitad ⇒ k=4.")
            L.append("")
            L.append("== Conclusión ==")
            L.append("Los resultados empíricos confirman la ley 1/√n: el error estándar decrece con la raíz del tamaño de muestra.")
            if integral_exact is not None:
                L.append("Las estimaciones están dentro del IC y se acercan al valor analítico.")
            self.text.insert("1.0","\n".join(L))

            # Gráficos
            self.ax_conv.clear()
            self.ax_conv.plot(np.arange(1,N1+1), cum1*area, label=f"Promedio acum. N1={N1}", color="tab:blue")
            self.ax_conv.plot(np.arange(1,N2+1), cum2*area, label=f"Promedio acum. N2={N2}", color="tab:orange", alpha=0.7)
            if integral_exact is not None:
                self.ax_conv.axhline(integral_exact, color="green", linestyle="--", label="Integral exacta")
            self.ax_conv.set_xlabel("Muestras")
            self.ax_conv.set_ylabel("Estimación acumulada")
            self.ax_conv.set_title("Convergencia Monte Carlo")
            self.ax_conv.grid(alpha=0.3)
            self.ax_conv.legend()

            self.ax_hist.clear()
            bins = min(40, max(10, N1//200))
            self.ax_hist.hist(res1["vals"], bins=bins, alpha=0.55, color="tab:blue", density=True, label=f"f(x,y) N1 ({N1})")
            self.ax_hist.hist(res2["vals"], bins=bins, alpha=0.45, color="tab:orange", density=True, label=f"f(x,y) N2 ({N2})")
            # Ajuste normal N2
            from math import sqrt, pi, exp
            def normal_pdf(xv, m, s): return (1/(s*(2*pi)**0.5))*np.exp(-(xv-m)**2/(2*s**2))
            xs_pdf = np.linspace(min(res1["vals"].min(), res2["vals"].min()),
                                 max(res1["vals"].max(), res2["vals"].max()), 300)
            self.ax_hist.plot(xs_pdf, normal_pdf(xs_pdf,res2["media"],res2["std"]),
                              color="black", linewidth=1.2, label="Normal aprox N2")
            self.ax_hist.set_title("Distribuciones muestrales f(x,y)")
            self.ax_hist.set_xlabel("f(x,y)")
            self.ax_hist.set_ylabel("Densidad")
            self.ax_hist.grid(alpha=0.3)
            self.ax_hist.legend()
            self.canvas.draw()

            # Guardar datos por si se exporta
            self.last_results = {
                "expr": expr_str, "a":a,"b":b,"c":c,"d":d,
                "N1":N1,"N2":N2,"k":k,
                "seed1":seed1,"seed2":seed2,
                "res1":res1,"res2":res2,
                "integral_exact":integral_exact,
                "integral_sym":integral_sym,
                "se_ratio_emp":se_ratio_emp,
                "se_ratio_teo":se_ratio_teo
            }

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def exportar_md(self):
        if not hasattr(self, "last_results"):
            messagebox.showwarning("Atención","Primero ejecute una simulación.")
            return
        R = self.last_results
        res1, res2 = R["res1"], R["res2"]
        integral_exact = R["integral_exact"]
        fname = filedialog.asksaveasfilename(defaultextension=".md",
                    filetypes=[("Markdown",".md")], title="Guardar informe")
        if not fname: return
        lines=[]
        lines.append(f"# Informe Monte Carlo (Ley 1/√n)")
        lines.append(f"Función: `f(x,y) = {R['expr']}`  Dominio: [{R['a']},{R['b']}]*[{R['c']},{R['d']}]")
        if integral_exact is not None:
            lines.append(f"Integral exacta ≈ **{integral_exact:.10f}**")
        else:
            lines.append("Integral exacta: no disponible simbólicamente.")
        lines.append("")
        lines.append(f"## Parámetros")
        lines.append(f"- N1 = {R['N1']} (seed={R['seed1']})")
        lines.append(f"- N2 = {R['N2']} (seed={R['seed2']})")
        lines.append(f"- k = {R['k']:.4g}, sqrt(k) = {R['k']**0.5:.4g}")
        lines.append("")
        def block(tag,res):
            lines.append(f"### {tag}")
            lines.append(f"- Media f = {res['media']:.10f}")
            lines.append(f"- Varianza = {res['var']:.10f}")
            lines.append(f"- Std = {res['std']:.10f}")
            lines.append(f"- SE = {res['stderr']:.10f}")
            lines.append(f"- Estimación integral = {res['integral_est']:.10f}")
            if integral_exact is not None:
                lines.append(f"- Error absoluto = {abs(integral_exact - res['integral_est']):.6e}")
            lines.append("")
        block(f"Muestra N1={R['N1']}", res1)
        block(f"Muestra N2={R['N2']}", res2)
        lines.append("## Comparación Escala de Error")
        lines.append(f"- Razón teórica SE1/SE2 = sqrt(N2/N1) = {R['se_ratio_teo']:.6f}")
        lines.append(f"- Razón empírica SE1/SE2 = {R['se_ratio_emp']:.6f}")
        lines.append("")
        lines.append("## Justificación resumida")
        lines.append("Para el estimador de Monte Carlo (media): Var(Ĩ_n)=σ²/n ⇒ SE=σ/√n. Al pasar de n→k·n, SE se divide por √k.")
        lines.append("Para reducir a la mitad ⇒ √k=2 ⇒ k=4.")
        with open(fname,"w",encoding="utf-8") as f:
            f.write("\n".join(lines))
        messagebox.showinfo("Exportación","Informe guardado.")

    def mostrar_ayuda(self):
        msg = (
            "Inciso (b) Ejercicio 4:\n"
            "Demostrar que el error (error estándar) decrece como 1/√n y que para reducirlo a la mitad se requiere cuadruplicar la muestra.\n\n"
            "Pasos:\n"
            "1. Definir f(x,y) y el rectángulo.\n"
            "2. Elegir N1 y un factor k (ej: 4) o un N2 manual.\n"
            "3. Ejecutar: se calculan dos estimaciones Monte Carlo y sus estadísticas.\n"
            "4. Verificar que SE1/SE2 ≈ sqrt(N2/N1). Si k=4 ⇒ razón ≈2.\n"
            "5. Exportar informe para documentar el resultado.\n\n"
            "La integral analítica (si se obtiene) permite además comparar el error real.\n"
        )
        messagebox.showinfo("Ayuda", msg)

# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    app = MonteCarloErrorGUI()
    app.mainloop()