# -*- coding: utf-8 -*-
"""
Simulador Runge-Kutta Profesional - Compatible con Mac
Resuelve ecuaciones diferenciales ordinarias usando métodos numéricos
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import math

class RungeKuttaPro:
    def __init__(self, root):
        self.root = root
        self.root.title("🔬 Simulador Runge-Kutta Profesional - Mac Compatible")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f0f0f0')
        
        # Variables de estado
        self.solution_expr = None
        self.show_rk4_table = tk.BooleanVar(value=False)
        
        # Variables de entrada
        self.func_str = tk.StringVar(value="y*sin(t)")
        self.t0 = tk.DoubleVar(value=0.0)
        self.y0 = tk.DoubleVar(value=1.0)
        self.t_end = tk.DoubleVar(value=math.pi)
        self.h = tk.DoubleVar(value=math.pi/10)
        self.method = tk.StringVar(value="Euler")
        
        # Configurar matplotlib para Mac
        plt.rcParams['font.size'] = 10
        plt.rcParams['figure.facecolor'] = 'white'
        
        self.create_widgets()
        self.setup_initial_data()

    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        
        # --- Frame Principal con Scroll ---
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # --- Frame de Entrada ---
        self.create_input_frame(main_frame)
        
        # --- Frame Principal con PanedWindow ---
        self.create_main_panels(main_frame)
        
        # --- Frame de Solución Analítica ---
        self.create_analytical_frame(main_frame)

    def create_input_frame(self, parent):
        """Crear el frame de entrada de parámetros"""
        frame_in = tk.LabelFrame(parent, text="📊 Parámetros de Entrada", 
                                padx=10, pady=10, bg='#e8f4fd', relief="raised", bd=2)
        frame_in.pack(fill="x", pady=(0, 10))
        
        # Primera fila - Parámetros básicos
        row1 = tk.Frame(frame_in, bg='#e8f4fd')
        row1.pack(fill="x", pady=5)
        
        tk.Label(row1, text="f(t,y) =", bg='#e8f4fd', font=('Arial', 12, 'bold')).pack(side="left", padx=5)
        func_entry = tk.Entry(row1, textvariable=self.func_str, width=20, font=('Arial', 11))
        func_entry.pack(side="left", padx=5)
        
        tk.Label(row1, text="t₀ =", bg='#e8f4fd', font=('Arial', 12, 'bold')).pack(side="left", padx=5)
        tk.Entry(row1, textvariable=self.t0, width=8, font=('Arial', 11)).pack(side="left", padx=5)
        
        tk.Label(row1, text="y₀ =", bg='#e8f4fd', font=('Arial', 12, 'bold')).pack(side="left", padx=5)
        tk.Entry(row1, textvariable=self.y0, width=8, font=('Arial', 11)).pack(side="left", padx=5)
        
        tk.Label(row1, text="t_end =", bg='#e8f4fd', font=('Arial', 12, 'bold')).pack(side="left", padx=5)
        tk.Entry(row1, textvariable=self.t_end, width=8, font=('Arial', 11)).pack(side="left", padx=5)
        
        tk.Label(row1, text="h =", bg='#e8f4fd', font=('Arial', 12, 'bold')).pack(side="left", padx=5)
        tk.Entry(row1, textvariable=self.h, width=8, font=('Arial', 11)).pack(side="left", padx=5)
        
        # Segunda fila - Método y botones
        row2 = tk.Frame(frame_in, bg='#e8f4fd')
        row2.pack(fill="x", pady=5)
        
        tk.Label(row2, text="Método:", bg='#e8f4fd', font=('Arial', 12, 'bold')).pack(side="left", padx=5)
        method_combo = ttk.Combobox(row2, textvariable=self.method, 
                                   values=["Euler", "Heun", "Midpoint", "RK2", "Ralston", "RK4"],
                                   width=12, font=('Arial', 11))
        method_combo.pack(side="left", padx=5)
        
        tk.Checkbutton(row2, text="Mostrar Pendientes RK4", variable=self.show_rk4_table,
                      bg='#e8f4fd', font=('Arial', 11)).pack(side="left", padx=10)
        
        # Botones principales
        button_frame = tk.Frame(row2, bg='#e8f4fd')
        button_frame.pack(side="right", padx=10)
        
        tk.Button(button_frame, text="🧮 Calcular", bg="#4CAF50", fg="white", 
                 command=self.solve, font=('Arial', 11, 'bold')).pack(side="left", padx=2)
        
        tk.Button(button_frame, text="📐 Solución Analítica", bg="#9C27B0", fg="white", 
                 command=self.calc_analytical, font=('Arial', 11, 'bold')).pack(side="left", padx=2)
        
        tk.Button(button_frame, text="📊 Comparar Métodos", bg="#FF9800", fg="white", 
                 command=self.compare_methods, font=('Arial', 11, 'bold')).pack(side="left", padx=2)
        
        tk.Button(button_frame, text="❓ Ayuda", bg="#2196F3", fg="white", 
                 command=self.show_help, font=('Arial', 11, 'bold')).pack(side="left", padx=2)

    def create_main_panels(self, parent):
        """Crear los paneles principales con PanedWindow"""
        self.paned = tk.PanedWindow(parent, orient="horizontal", sashrelief="sunken", bg='#f0f0f0')
        self.paned.pack(fill="both", expand=True, pady=10)
        
        # --- Panel Izquierdo: Tablas ---
        self.create_tables_panel()
        
        # --- Panel Derecho: Gráfica ---
        self.create_plot_panel()

    def create_tables_panel(self):
        """Crear el panel de tablas"""
        tables_frame = tk.Frame(self.paned, bg='#f0f0f0')
        self.paned.add(tables_frame, stretch="always")
        
        # Notebook para las pestañas
        self.tab_frame = ttk.Notebook(tables_frame)
        self.tab_frame.pack(fill="both", expand=True)
        
        # Tabla Normal
        self.create_normal_table()
        
        # Tabla Comparativa
        self.create_comparative_table()
        
        # Tabla RK4 Pendientes
        self.create_rk4_table()

    def create_normal_table(self):
        """Crear la tabla normal"""
        self.table_frame = tk.Frame(self.tab_frame, bg='white')
        self.tab_frame.add(self.table_frame, text="📋 Tabla Normal")
        
        # Frame para la tabla con scroll
        table_container = tk.Frame(self.table_frame, bg='white')
        table_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(table_container, orient="vertical")
        h_scroll = ttk.Scrollbar(table_container, orient="horizontal")
        
        # Treeview
        self.table = ttk.Treeview(table_container, 
                                 columns=("n", "t", "y_num", "y_exact", "Error"),
                                 show="headings", height=15,
                                 yscrollcommand=v_scroll.set,
                                 xscrollcommand=h_scroll.set)
        
        # Configurar scrollbars
        v_scroll.config(command=self.table.yview)
        h_scroll.config(command=self.table.xview)
        
        # Posicionar elementos
        self.table.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        
        # Configurar columnas
        headers = ["n", "t", "y_num", "y_exact", "Error"]
        for h in headers:
            self.table.heading(h, text=h)
            self.table.column(h, width=120, anchor="center")

    def create_comparative_table(self):
        """Crear la tabla comparativa"""
        self.comp_frame = tk.Frame(self.tab_frame, bg='white')
        self.tab_frame.add(self.comp_frame, text="📊 Tabla Comparativa")
        
        # Frame para la tabla con scroll
        table_container = tk.Frame(self.comp_frame, bg='white')
        table_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(table_container, orient="vertical")
        h_scroll = ttk.Scrollbar(table_container, orient="horizontal")
        
        # Treeview
        self.comp_table = ttk.Treeview(table_container, show="headings", height=15,
                                      yscrollcommand=v_scroll.set,
                                      xscrollcommand=h_scroll.set)
        
        # Configurar scrollbars
        v_scroll.config(command=self.comp_table.yview)
        h_scroll.config(command=self.comp_table.xview)
        
        # Posicionar elementos
        self.comp_table.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

    def create_rk4_table(self):
        """Crear la tabla de pendientes RK4"""
        self.rk4_frame = tk.Frame(self.tab_frame, bg='white')
        self.tab_frame.add(self.rk4_frame, text="🔢 Pendientes RK4")
        
        # Frame para la tabla con scroll
        table_container = tk.Frame(self.rk4_frame, bg='white')
        table_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(table_container, orient="vertical")
        h_scroll = ttk.Scrollbar(table_container, orient="horizontal")
        
        # Treeview
        self.rk4_table = ttk.Treeview(table_container, show="headings", height=15,
                                     yscrollcommand=v_scroll.set,
                                     xscrollcommand=h_scroll.set)
        
        # Configurar scrollbars
        v_scroll.config(command=self.rk4_table.yview)
        h_scroll.config(command=self.rk4_table.xview)
        
        # Posicionar elementos
        self.rk4_table.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

    def create_plot_panel(self):
        """Crear el panel de gráfica"""
        self.plot_frame = tk.Frame(self.paned, bg='white')
        self.paned.add(self.plot_frame, stretch="always")
        
        # Crear figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 6), facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Toolbar de matplotlib
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.update()
        
        # Configurar gráfica inicial
        self.ax.set_title("Solución Numérica vs Analítica", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("t", fontsize=12)
        self.ax.set_ylabel("y(t)", fontsize=12)
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()

    def create_analytical_frame(self, parent):
        """Crear el frame de solución analítica"""
        self.analytic_frame = tk.LabelFrame(parent, 
                                           text="🔍 SOLUCIÓN ANALÍTICA (LaTeX) - Hacé clic en 'Solución Analítica'",
                                           padx=10, pady=10, bg='#fff3cd', relief="raised", bd=3)
        self.analytic_frame.pack(fill="x", pady=(10, 0))
        
        # Crear figura para LaTeX
        self.fig_analytic, self.ax_analytic = plt.subplots(figsize=(14, 3), facecolor='white')
        self.ax_analytic.axis("off")
        
        # Canvas para la figura
        self.canvas_analytic = FigureCanvasTkAgg(self.fig_analytic, master=self.analytic_frame)
        self.canvas_analytic.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Mensaje inicial
        self.ax_analytic.text(0.5, 0.5, "Hacé clic en '📐 Solución Analítica' para ver la fórmula", 
                             fontsize=16, ha="center", va="center", 
                             bbox=dict(boxstyle="round,pad=0.5", facecolor="yellow", alpha=0.8))
        self.canvas_analytic.draw()

    def setup_initial_data(self):
        """Configurar datos iniciales para el ejercicio 5"""
        # Datos del ejercicio 5: dy/dx = y*sin(x), y(0) = 1, x ∈ [0, π]
        self.func_str.set("y*sin(t)")
        self.t0.set(0.0)
        self.y0.set(1.0)
        self.t_end.set(math.pi)
        self.h.set(math.pi/10)
        self.method.set("Euler")

    def f(self, t, y):
        """Evaluar la función f(t,y)"""
        try:
            t_sym, y_sym = sp.symbols("t y")
            expr = sp.sympify(self.func_str.get())
            f_lamb = sp.lambdify((t_sym, y_sym), expr, "numpy")
            return f_lamb(t, y)
        except Exception as e:
            messagebox.showerror("Error", f"Error al evaluar la función: {str(e)}")
            return 0

    def solve(self):
        """Resolver la EDO usando el método seleccionado"""
        try:
            # Limpiar tabla
            self.table.delete(*self.table.get_children())
            
            # Obtener parámetros
            t0, y0, t_end, h = self.t0.get(), self.y0.get(), self.t_end.get(), self.h.get()
            n_steps = int((t_end - t0) / h)
            
            # Arrays para almacenar resultados
            t_values = [t0]
            y_values = [y0]
            rk4_pendientes = []
            
            # Resolver paso a paso
            t, y = t0, y0
            for i in range(n_steps):
                if self.method.get() == "Euler":
                    y += h * self.f(t, y)
                elif self.method.get() == "Heun":
                    k1 = self.f(t, y)
                    k2 = self.f(t + h, y + h * k1)
                    y += h * (k1 + k2) / 2
                elif self.method.get() == "Midpoint":
                    k1 = self.f(t, y)
                    k2 = self.f(t + h/2, y + h * k1/2)
                    y += h * k2
                elif self.method.get() == "RK2":
                    k1 = self.f(t, y)
                    k2 = self.f(t + h/2, y + h * k1/2)
                    y += h * k2
                elif self.method.get() == "Ralston":
                    k1 = self.f(t, y)
                    k2 = self.f(t + 3*h/4, y + 3*h * k1/4)
                    y += h * (k1 + k2/3)
                elif self.method.get() == "RK4":
                    k1 = self.f(t, y)
                    k2 = self.f(t + h/2, y + h * k1/2)
                    k3 = self.f(t + h/2, y + h * k2/2)
                    k4 = self.f(t + h, y + h * k3)
                    y_next = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
                    
                    if self.show_rk4_table.get():
                        rk4_pendientes.append([i, t, y, k1, k2, k3, k4, y_next])
                    
                    y = y_next
                
                t += h
                t_values.append(t)
                y_values.append(y)
            
            # Llenar tabla normal
            self.fill_normal_table(t_values, y_values)
            
            # Llenar tabla RK4 si es necesario
            if self.show_rk4_table.get() and rk4_pendientes:
                self.fill_rk4_table(rk4_pendientes)
            
            # Actualizar gráfica
            self.update_plot(t_values, y_values)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al resolver la EDO: {str(e)}")

    def fill_normal_table(self, t_values, y_values):
        """Llenar la tabla normal con los resultados"""
        for i, (ti, yi) in enumerate(zip(t_values, y_values)):
            y_exact_str, err_str = "-", "-"
            
            if self.solution_expr is not None:
                try:
                    y_exact_val = float(self.solution_expr.subs("t", ti))
                    err_val = abs(yi - y_exact_val)
                    y_exact_str = f"{y_exact_val:.6f}"
                    err_str = f"{err_val:.6e}" if err_val < 1e-6 else f"{err_val:.6f}"
                except:
                    pass
            
            self.table.insert("", "end", values=(
                i, f"{ti:.3f}", f"{yi:.6f}", y_exact_str, err_str
            ))

    def fill_rk4_table(self, rk4_pendientes):
        """Llenar la tabla de pendientes RK4"""
        self.rk4_table.delete(*self.rk4_table.get_children())
        
        cols = ["n", "t_n", "y_n", "k1", "k2", "k3", "k4", "y_{n+1}"]
        self.rk4_table["columns"] = cols
        
        for c in cols:
            self.rk4_table.heading(c, text=c)
            self.rk4_table.column(c, width=100, anchor="center")
        
        for row in rk4_pendientes:
            formatted_row = [f"{v:.6f}" if isinstance(v, float) else str(v) for v in row]
            self.rk4_table.insert("", "end", values=formatted_row)

    def update_plot(self, t_values, y_values):
        """Actualizar la gráfica con los resultados"""
        self.ax.clear()
        
        # Graficar solución numérica
        self.ax.plot(t_values, y_values, label=self.method.get(), 
                    marker="o", markersize=4, linewidth=2)
        
        # Graficar solución exacta si está disponible
        if self.solution_expr is not None:
            try:
                t_dense = np.linspace(self.t0.get(), self.t_end.get(), 200)
                y_dense = [float(self.solution_expr.subs("t", tt)) for tt in t_dense]
                self.ax.plot(t_dense, y_dense, "k--", label="Exacta", linewidth=2)
            except:
                pass
        
        self.ax.set_title(f"Solución Numérica vs Analítica - {self.method.get()}", 
                         fontsize=14, fontweight='bold')
        self.ax.set_xlabel("t", fontsize=12)
        self.ax.set_ylabel("y(t)", fontsize=12)
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()
        
        self.canvas.draw()

    def calc_analytical(self):
        """Calcular la solución analítica"""
        try:
            self.ax_analytic.clear()
            
            t_sym = sp.symbols("t")
            y_func = sp.Function("y")
            
            # Crear la EDO
            ode = sp.Eq(sp.Derivative(y_func(t_sym), t_sym), 
                       sp.sympify(self.func_str.get()).subs({"y": y_func(t_sym)}))
            
            # Resolver con condición inicial
            sol = sp.dsolve(ode, ics={y_func(self.t0.get()): self.y0.get()})
            self.solution_expr = sol.rhs
            
            # Convertir a LaTeX
            sol_latex = sp.latex(sol)
            
            # Mostrar en la gráfica
            self.ax_analytic.text(0.5, 0.5, f"${sol_latex}$", 
                                 fontsize=18, ha="center", va="center",
                                 bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.8))
            
            self.ax_analytic.axis("off")
            self.canvas_analytic.draw()
            
            messagebox.showinfo("Éxito", "Solución analítica calculada correctamente!")
            
        except Exception as e:
            self.solution_expr = None
            self.ax_analytic.text(0.5, 0.5, "No se pudo encontrar solución analítica", 
                                 fontsize=16, ha="center", va="center",
                                 bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcoral", alpha=0.8))
            self.ax_analytic.axis("off")
            self.canvas_analytic.draw()
            
            messagebox.showwarning("Advertencia", f"No se pudo calcular la solución analítica: {str(e)}")

    def compare_methods(self):
        """Comparar todos los métodos numéricos"""
        try:
            methods = ["Euler", "Heun", "Midpoint", "RK2", "Ralston", "RK4"]
            t0, y0, t_end, h = self.t0.get(), self.y0.get(), self.t_end.get(), self.h.get()
            
            self.ax.clear()
            
            for method in methods:
                t, y = t0, y0
                t_vals, y_vals = [t0], [y0]
                n_steps = int((t_end - t0) / h)
                
                for _ in range(n_steps):
                    if method == "Euler":
                        y += h * self.f(t, y)
                    elif method == "Heun":
                        k1 = self.f(t, y)
                        k2 = self.f(t + h, y + h * k1)
                        y += h * (k1 + k2) / 2
                    elif method == "Midpoint":
                        k1 = self.f(t, y)
                        k2 = self.f(t + h/2, y + h * k1/2)
                        y += h * k2
                    elif method == "RK2":
                        k1 = self.f(t, y)
                        k2 = self.f(t + h/2, y + h * k1/2)
                        y += h * k2
                    elif method == "Ralston":
                        k1 = self.f(t, y)
                        k2 = self.f(t + 3*h/4, y + 3*h * k1/4)
                        y += h * (k1 + k2/3)
                    elif method == "RK4":
                        k1 = self.f(t, y)
                        k2 = self.f(t + h/2, y + h * k1/2)
                        k3 = self.f(t + h/2, y + h * k2/2)
                        k4 = self.f(t + h, y + h * k3)
                        y += h * (k1 + 2*k2 + 2*k3 + k4) / 6
                    
                    t += h
                    t_vals.append(t)
                    y_vals.append(y)
                
                self.ax.plot(t_vals, y_vals, label=method, marker="o", markersize=3, linewidth=1.5)
            
            # Agregar solución exacta si está disponible
            if self.solution_expr is not None:
                try:
                    t_dense = np.linspace(t0, t_end, 200)
                    y_dense = [float(self.solution_expr.subs("t", tt)) for tt in t_dense]
                    self.ax.plot(t_dense, y_dense, "k--", label="Exacta", linewidth=3)
                except:
                    pass
            
            self.ax.set_title("Comparación de Todos los Métodos", fontsize=14, fontweight='bold')
            self.ax.set_xlabel("t", fontsize=12)
            self.ax.set_ylabel("y(t)", fontsize=12)
            self.ax.grid(True, alpha=0.3)
            self.ax.legend()
            
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al comparar métodos: {str(e)}")

    def show_help(self):
        """Mostrar ayuda sobre los métodos"""
        help_text = """
🔬 MÉTODOS RUNGE-KUTTA DISPONIBLES:

1. 📈 Euler: y_{n+1} = y_n + h·f(t_n, y_n)
   - Método más simple, orden 1

2. 🔄 Heun: y_{n+1} = y_n + h·(k1 + k2)/2
   - Predictor-Corrector, orden 2

3. 🎯 Midpoint: y_{n+1} = y_n + h·f(t_n + h/2, y_n + h·k1/2)
   - Punto medio, orden 2

4. 📊 RK2: y_{n+1} = y_n + h·k2
   - Runge-Kutta de orden 2

5. ⚡ Ralston: y_{n+1} = y_n + h·(k1 + k2/3)
   - Variante de RK2, orden 2

6. 🚀 RK4: y_{n+1} = y_n + h·(k1 + 2k2 + 2k3 + k4)/6
   - Runge-Kutta de orden 4 (más preciso)

Donde k1, k2, k3, k4 son las pendientes intermedias.

📝 INSTRUCCIONES:
1. Ingresá la función f(t,y)
2. Configurá los parámetros iniciales
3. Seleccioná el método
4. Hacé clic en "Calcular"
5. Para ver la solución exacta, hacé clic en "Solución Analítica"
        """
        
        # Crear ventana de ayuda
        help_window = tk.Toplevel(self.root)
        help_window.title("Ayuda - Métodos Runge-Kutta")
        help_window.geometry("600x500")
        help_window.configure(bg='#f0f0f0')
        
        # Texto con scroll
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, 
                                               font=('Arial', 11), bg='white')
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("1.0", help_text)
        text_widget.config(state="disabled")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = RungeKuttaPro(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al ejecutar la aplicación: {e}")
        messagebox.showerror("Error Fatal", f"Error al ejecutar la aplicación: {e}")