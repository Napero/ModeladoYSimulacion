import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy.polynomial.legendre import leggauss
from scipy import stats
 
class MonteCarloSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Monte Carlo + Gauss-Legendre")
 
        # -------------------- Entradas --------------------
        frame_inputs = ttk.LabelFrame(root, text="Parámetros")
        frame_inputs.pack(fill="x", padx=5, pady=5)
 
        # Función y límites
        ttk.Label(frame_inputs, text="f(x) =").grid(row=0, column=0)
        self.entry_func = ttk.Entry(frame_inputs, width=25)
        self.entry_func.insert(0, "sin(x)+1") # exp(2*x - y)
        self.entry_func.grid(row=0, column=1)
 
        ttk.Label(frame_inputs, text="a =").grid(row=0, column=2)
        self.entry_a = ttk.Entry(frame_inputs, width=5)
        self.entry_a.insert(0, "0")
        self.entry_a.grid(row=0, column=3)
 
        ttk.Label(frame_inputs, text="b =").grid(row=0, column=4)
        self.entry_b = ttk.Entry(frame_inputs, width=5)
        self.entry_b.insert(0, "3.14")
        self.entry_b.grid(row=0, column=5)
 
        ttk.Label(frame_inputs, text="N =").grid(row=0, column=6)
        self.entry_N = ttk.Entry(frame_inputs, width=8)
        self.entry_N.insert(0, "500")
        self.entry_N.grid(row=0, column=7)
 
        ttk.Label(frame_inputs, text="Gauss pts =").grid(row=0, column=8)
        self.entry_gauss = ttk.Entry(frame_inputs, width=5)
        self.entry_gauss.insert(0, "5")
        self.entry_gauss.grid(row=0, column=9)
 
        # Botones principales
        ttk.Button(frame_inputs, text="Simular", command=self.simular).grid(row=0, column=10, padx=5)
        ttk.Button(frame_inputs, text="Limpiar", command=self.limpiar).grid(row=0, column=11, padx=5)
        ttk.Button(frame_inputs, text="Convergencia", command=self.ventana_convergencia).grid(row=0, column=12, padx=5)
        ttk.Button(frame_inputs, text="Ayuda", command=self.mostrar_ayuda).grid(row=0, column=13, padx=5)
        ttk.Button(frame_inputs, text="Análisis Estadístico", command=self.ventana_estadistica).grid(row=0, column=14, padx=5)
        ttk.Button(frame_inputs, text="Integrales Dobles", command=self.ventana_integrales_dobles).grid(row=0, column=15, padx=5)
 
        # -------------------- Tabla --------------------
        frame_table = ttk.LabelFrame(root, text="Muestras Monte Carlo")
        frame_table.pack(side="left", fill="y", padx=5, pady=5)
 
        cols = ("x", "y", "f(x)", "Éxito")
        self.tree = ttk.Treeview(frame_table, columns=cols, show="headings", height=20)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=70, anchor="center")
        self.tree.pack(side="left", fill="y")
 
        scroll = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
 
        # -------------------- Gráfico --------------------
        frame_plot = ttk.LabelFrame(root, text="Gráfico")
        frame_plot.pack(side="right", fill="both", expand=True, padx=5, pady=5)
 
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_plot)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
 
        # -------------------- Resultados --------------------
        self.label_result = ttk.Label(root, text="Resultados: ")
        self.label_result.pack(fill="x", padx=5, pady=5)
 
    # -------------------- Simulación MC simple --------------------
    def simular(self):
        try:
            func_str = self.entry_func.get()
            a, b = float(self.entry_a.get()), float(self.entry_b.get())
            N = int(self.entry_N.get())
            n_gauss = int(self.entry_gauss.get())
 
            x = sp.Symbol('x')
            f_expr = sp.sympify(func_str)
            f = sp.lambdify(x, f_expr, "numpy")
 
            xs_dense = np.linspace(a, b, 1000)
            ys_dense = f(xs_dense)
            y_min, y_max = min(0, np.min(ys_dense)), max(0, np.max(ys_dense))
 
            np.random.seed(0)
            xs = np.random.uniform(a, b, N)
            ys = np.random.uniform(y_min, y_max, N)
            success_mask = ((ys >= 0) & (ys <= f(xs))) | ((ys <= 0) & (ys >= f(xs)))
            count = np.sum(success_mask)
 
            rect_area = (b - a) * (y_max - y_min)
            mc_estimate = count / N * rect_area
            mc_prom = (b - a) * np.mean(f(xs))
 
            nodes, weights = leggauss(n_gauss)
            trans_nodes = 0.5*(nodes+1)*(b-a)+a
            gauss_val = 0.5*(b-a)*np.sum(weights * f(trans_nodes))
 
            self.fxs_samples = f(xs)
 
            # Tabla
            for i in self.tree.get_children():
                self.tree.delete(i)
            for i in range(min(N, 5000)):
                self.tree.insert("", "end",
                                 values=(f"{xs[i]:.3f}", f"{ys[i]:.3f}", f"{self.fxs_samples[i]:.3f}",
                                         "✔" if success_mask[i] else "✘"))
 
            # Gráfico
            self.ax.clear()
            self.ax.fill_between(xs_dense, 0, ys_dense, color='lightblue', alpha=0.3, label='Área bajo la curva')
            self.ax.plot(xs_dense, ys_dense, label=f"f(x)={func_str}", color="blue", linewidth=2)
            self.ax.scatter(xs[~success_mask], ys[~success_mask], s=15, alpha=0.5, color="red", label="Fallidos")
            self.ax.scatter(xs[success_mask], ys[success_mask], s=15, alpha=0.5, color="green", label="Éxitos")
            self.ax.axhline(0, color="black", linewidth=0.8)
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y=f(x)")
            self.ax.set_title(f"MC: {mc_estimate:.4f} | MC promedio: {mc_prom:.4f} | Gauss: {gauss_val:.4f}")
            self.ax.legend()
            self.ax.grid(True)
            self.ax.set_xlim(a, b)
            self.ax.set_ylim(y_min - 0.1*abs(y_min), y_max + 0.1*abs(y_max))
            self.canvas.draw()
 
            self.convergencia_data = (xs, self.fxs_samples, b - a, gauss_val)
 
        except Exception as e:
            messagebox.showerror("Error", str(e))
 
    # -------------------- Limpiar --------------------
    def limpiar(self):
        self.ax.clear()
        self.canvas.draw()
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.label_result.config(text="Resultados: ")
 
    # -------------------- Ventana Convergencia --------------------
    def ventana_convergencia(self):
        if not hasattr(self, 'convergencia_data'):
            messagebox.showwarning("Atención", "Primero ejecute una simulación.")
            return
 
        xs, fxs, L, gauss_val = self.convergencia_data
        cum_avg = np.cumsum(fxs)/np.arange(1, len(fxs)+1)
        std_accum = np.array([np.std(fxs[:i+1]) for i in range(len(fxs))])
 
        win = tk.Toplevel(self.root)
        win.title("Convergencia Monte Carlo")
 
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(cum_avg*L, label="MC promedio acumulado", color="green")
        ax.fill_between(range(len(cum_avg)), cum_avg*L - std_accum, cum_avg*L + std_accum,
                        color='gray', alpha=0.3, label='±1 std')
        ax.axhline(gauss_val, color="red", linestyle="--", label="Gauss-Legendre")
        ax.set_xlabel("Número de muestras")
        ax.set_ylabel("Estimación")
        ax.legend()
        ax.grid(True)
 
        canvas_conv = FigureCanvasTkAgg(fig, master=win)
        canvas_conv.get_tk_widget().pack(fill="both", expand=True)
        canvas_conv.draw()
 
    # -------------------- Análisis Estadístico --------------------
    def ventana_estadistica(self):
        if not hasattr(self, "fxs_samples"):
            messagebox.showwarning("Atención", "Primero ejecute una simulación.")
            return
 
        data = self.fxs_samples
        n = len(data)
        media = np.mean(data)
        std = np.std(data, ddof=1)
        stderr = std / np.sqrt(n)
 
        win = tk.Toplevel(self.root)
        win.title("Análisis Estadístico")
 
        ttk.Label(win, text="Nivel de confianza:").pack(padx=5, pady=5, anchor="w")
        confidence_var = tk.DoubleVar(value=95)
        conf_box = ttk.Combobox(win, textvariable=confidence_var, values=[90,95,99], width=5)
        conf_box.pack(padx=5, pady=5, anchor="w")
 
        lbl = tk.Label(win, justify="left", font=("Arial",12))
        lbl.pack(padx=10, pady=10)
 
        fig, ax = plt.subplots(figsize=(5,3))
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
 
        def actualizar(event=None):
            conf = confidence_var.get()/100
            t_val = stats.t.ppf(0.5+conf/2, n-1)
            ic_lower = media - t_val*stderr
            ic_upper = media + t_val*stderr
            lbl.config(text=f"Muestras: {n}\nMedia: {media:.4f}\nDesviación estándar: {std:.4f}\n"
                            f"Error estándar: {stderr:.4f}\nIntervalo de confianza {int(conf*100)}%: [{ic_lower:.4f}, {ic_upper:.4f}]")
            ax.clear()
            ax.hist(data, bins=min(30,n//5), color='skyblue', edgecolor='black', alpha=0.7, density=True)
            x_vals = np.linspace(min(data), max(data), 200)
            y_norm = stats.norm.pdf(x_vals, media, std)
            ax.plot(x_vals, y_norm, color='orange', linewidth=2, label='Distribución Normal')
            ax.axvline(media, color='blue', linestyle='-', linewidth=2, label='Media')
            ax.axvline(ic_lower, color='red', linestyle='--', linewidth=2, label=f'IC {int(conf*100)}%')
            ax.axvline(ic_upper, color='red', linestyle='--', linewidth=2)
            ax.set_title("Distribución muestral f(x)")
            ax.set_xlabel("f(x)")
            ax.set_ylabel("Densidad")
            ax.grid(True)
            ax.legend()
            canvas.draw()
 
        conf_box.bind("<<ComboboxSelected>>", actualizar)
        actualizar()
 
    # -------------------- Ayuda --------------------
    def mostrar_ayuda(self):
        texto = (
            "Este simulador aproxima integrales definidas usando Monte Carlo.\n\n"
            "1. Método de 'puntos de éxito' (hit-or-miss): se genera un rectángulo que contiene a la curva. Se cuentan los puntos dentro de la región bajo la curva y se estima el área.\n\n"
            "2. Método Monte Carlo promedio: se toma el promedio de f(x) evaluada en puntos aleatorios de [a,b] y se multiplica por la longitud del intervalo.\n\n"
            "3. Gauss-Legendre: método de cuadratura determinista de alta precisión que se toma como valor de referencia.\n\n"
            "La ventana de 'Convergencia' muestra cómo la estimación MC promedio se acerca al valor de Gauss-Legendre a medida que aumentan las muestras."
        )
        win = tk.Toplevel(self.root)
        win.title("Ayuda teórica")
        msg = tk.Message(win, text=texto, width=500)
        msg.pack(padx=10, pady=10)
 
    # -------------------- Integrales Dobles --------------------
    def ventana_integrales_dobles(self):
        win = tk.Toplevel(self.root)
        win.title("Integrales Dobles Monte Carlo")
        tab = ttk.Frame(win)
        tab.pack(fill="both", expand=True)
 
        ttk.Label(tab, text="f(x,y) =").grid(row=0,column=0)
        entry_func = ttk.Entry(tab, width=25)
        entry_func.insert(0,"x*y")
        entry_func.grid(row=0,column=1,columnspan=3)
 
        ttk.Label(tab, text="x: a=").grid(row=1,column=0)
        entry_ax = ttk.Entry(tab,width=5); entry_ax.insert(0,"0"); entry_ax.grid(row=1,column=1)
        ttk.Label(tab,text="b=").grid(row=1,column=2)
        entry_bx = ttk.Entry(tab,width=5); entry_bx.insert(0,"1"); entry_bx.grid(row=1,column=3)
 
        ttk.Label(tab, text="y: c=").grid(row=2,column=0)
        entry_cy = ttk.Entry(tab,width=5); entry_cy.insert(0,"0"); entry_cy.grid(row=2,column=1)
        ttk.Label(tab,text="d=").grid(row=2,column=2)
        entry_dy = ttk.Entry(tab,width=5); entry_dy.insert(0,"1"); entry_dy.grid(row=2,column=3)
 
        ttk.Label(tab,text="N=").grid(row=3,column=0)
        entry_N = ttk.Entry(tab,width=8); entry_N.insert(0,"500"); entry_N.grid(row=3,column=1)
        ttk.Label(tab,text="Gauss pts=").grid(row=3,column=2)
        entry_gauss = ttk.Entry(tab,width=5); entry_gauss.insert(0,"5"); entry_gauss.grid(row=3,column=3)
 
        # -------------------- Función simular doble --------------------
        def simular_doble():
            try:
                fx = sp.Symbol('x'); fy = sp.Symbol('y')
                func_expr = sp.sympify(entry_func.get())
                f = sp.lambdify((fx, fy), func_expr,'numpy')
 
                a,b = float(entry_ax.get()), float(entry_bx.get())
                c,d = float(entry_cy.get()), float(entry_dy.get())
                N = int(entry_N.get()); n_gauss = int(entry_gauss.get())
 
                xs = np.random.uniform(a,b,N)
                ys = np.random.uniform(c,d,N)
                f_vals = f(xs,ys)
                simular_doble.fx_vals = f_vals
                estimate_mc = (b-a)*(d-c)*np.mean(f_vals)
 
                # Gauss-Legendre doble
                nodes_x, weights_x = leggauss(n_gauss)
                nodes_y, weights_y = leggauss(n_gauss)
                trans_x = 0.5*(nodes_x+1)*(b-a)+a
                trans_y = 0.5*(nodes_y+1)*(d-c)+c
                gauss_val = 0
                for i in range(n_gauss):
                    for j in range(n_gauss):
                        gauss_val += weights_x[i]*weights_y[j]*f(trans_x[i],trans_y[j])
                gauss_val *= 0.25*(b-a)*(d-c)
 
                messagebox.showinfo("Resultado",f"MC doble: {estimate_mc:.6f}\nGauss-Legendre doble: {gauss_val:.6f}")
 
                fig2, ax2 = plt.subplots(figsize=(5,4))
                sc = ax2.scatter(xs, ys, c=f_vals, cmap='viridis', s=20)
                ax2.set_xlabel("x"); ax2.set_ylabel("y"); ax2.set_title("Distribución de puntos y f(x,y)")
                plt.colorbar(sc, ax=ax2, label='f(x,y)')
                canvas2 = FigureCanvasTkAgg(fig2, master=tab)
                canvas2.get_tk_widget().grid(row=5, column=0, columnspan=4, pady=10)
                canvas2.draw()
 
            except Exception as e:
                messagebox.showerror("Error",str(e))
 
        ttk.Button(tab,text="Simular",command=simular_doble).grid(row=4,column=0,padx=5,pady=5)
        ttk.Button(tab,text="Limpiar",command=lambda: plt.close('all')).grid(row=4,column=1,padx=5,pady=5)
 
        # -------------------- Estadístico doble --------------------
        def analisis_estadistico_doble():
            if not hasattr(simular_doble,"fx_vals"):
                messagebox.showwarning("Atención","Primero ejecute la simulación doble.")
                return
            data = simular_doble.fx_vals
            n = len(data)
            media = np.mean(data)
            std = np.std(data, ddof=1)
            stderr = std/np.sqrt(n)
 
            win2 = tk.Toplevel(tab)
            win2.title("Análisis Estadístico Integral Doble")
 
            ttk.Label(win2,text="Nivel de confianza:").pack(padx=5,pady=5, anchor="w")
            confidence_var = tk.DoubleVar(value=95)
            conf_box = ttk.Combobox(win2, textvariable=confidence_var, values=[90,95,99], width=5)
            conf_box.pack(padx=5,pady=5, anchor="w")
 
            lbl = tk.Label(win2, justify="left", font=("Arial",12))
            lbl.pack(padx=10,pady=10)
 
            fig, ax = plt.subplots(figsize=(5,3))
            canvas = FigureCanvasTkAgg(fig, master=win2)
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
 
            def actualizar(event=None):
                conf = confidence_var.get()/100
                t_val = stats.t.ppf(0.5+conf/2,n-1)
                ic_lower = media - t_val*stderr
                ic_upper = media + t_val*stderr
                lbl.config(text=f"Muestras: {n}\nMedia: {media:.4f}\nDesviación estándar: {std:.4f}\nError estándar: {stderr:.4f}\nIntervalo de confianza {int(conf*100)}%: [{ic_lower:.4f}, {ic_upper:.4f}]")
                ax.clear()
                ax.hist(data, bins=min(30,n//5), color='skyblue', edgecolor='black', alpha=0.7, density=True)
                x_vals = np.linspace(min(data),max(data),200)
                y_norm = stats.norm.pdf(x_vals, media, std)
                ax.plot(x_vals, y_norm, color='orange', linewidth=2, label='Distribución Normal')
                ax.axvline(media, color='blue', linestyle='-', linewidth=2, label='Media')
                ax.axvline(ic_lower, color='red', linestyle='--', linewidth=2, label=f'IC {int(conf*100)}%')
                ax.axvline(ic_upper, color='red', linestyle='--', linewidth=2)
                ax.set_title("Distribución muestral f(x,y)")
                ax.set_xlabel("f(x,y)")
                ax.set_ylabel("Densidad")
                ax.grid(True)
                ax.legend()
                canvas.draw()
 
            conf_box.bind("<<ComboboxSelected>>", actualizar)
            actualizar()
 
        ttk.Button(tab,text="Análisis Estadístico",command=analisis_estadistico_doble).grid(row=4,column=3,padx=5,pady=5)
 
if __name__=="__main__":
    root = tk.Tk()
    app = MonteCarloSimulator(root)
    root.mainloop()