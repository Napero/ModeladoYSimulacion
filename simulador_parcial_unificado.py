# -*- coding: utf-8 -*-
"""
Simulador Unificado de Métodos Numéricos - Parcial UADE
Integra todos los ejercicios del parcial con interfaz por pestañas
Incluye guías paso a paso para resolver en la hoja
DATOS DEL PARCIAL ACTUAL COMO BASE + FUNCIONES PERSONALIZADAS
"""

import ast
import math
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from typing import Callable, Optional, List, Tuple, Dict
import numpy as np
import sympy as sp
from scipy import stats

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from matplotlib.figure import Figure
except Exception:
    FigureCanvasTkAgg = None
    plt = None
    FuncAnimation = None

# =============================================================================
# DATOS DEL PARCIAL ACTUAL (COMO BASE)
# =============================================================================

PARCIAL_DATA = {
    "ejercicio_1": {
        "funcion": "exp(x) - 3*x**2",
        "intervalo": [0, 1],
        "semilla": 0.5,
        "descripcion": "Encontrar raíz de f(x) = e^x - 3x² en (0,1)",
        "solucion_esperada": 0.9100075725
    },
    "ejercicio_2": {
        "funcion": "log(x + 1)",
        "nodos": [0, 1, 2],
        "punto_evaluacion": 0.45,
        "punto_derivada": 1.5,
        "descripcion": "Interpolación de f(x) = ln(x+1) en nodos [0,1,2]"
    },
    "ejercicio_3": {
        "funcion": "sqrt(2) * exp(x**2)",
        "intervalo": [0, 1],
        "descripcion": "Integración de f(x) = √2 * e^(x²) en [0,1]",
        "solucion_esperada": 2.068501936091
    },
    "ejercicio_4": {
        "funcion": "exp(2*x - y)",
        "dominio_x": [0, 1],
        "dominio_y": [1, 2],
        "descripcion": "Integral doble de f(x,y) = e^(2x-y) en [0,1]×[1,2]",
        "solucion_esperada": 0.742868647
    },
    "ejercicio_5": {
        "funcion": "y * sin(t)",
        "condicion_inicial": [0, 1],
        "intervalo": [0, "pi"],
        "paso": "pi/10",
        "descripcion": "EDO y' = y*sin(t), y(0)=1, t∈[0,π]"
    }
}

# ============================================================================
# UTILIDADES COMUNES
# ============================================================================

def cargar_datos_parcial(ejercicio: str) -> dict:
    """Carga los datos del parcial actual para un ejercicio específico."""
    return PARCIAL_DATA.get(ejercicio, {})

def generar_funcion_punto_fijo(funcion_str: str) -> str:
    """Genera automáticamente la función g(x) para el método de punto fijo."""
    try:
        # Simplificar la expresión
        x = sp.Symbol('x')
        expr = sp.sympify(funcion_str)
        
        # Intentar diferentes despejes para g(x)
        # Opción 1: x = sqrt(expr/coeficiente) si es cuadrática
        if expr.has(x**2):
            # Para e^x - 3x² = 0 → x = sqrt(e^x/3)
            if 'exp' in funcion_str.lower() or 'e**' in funcion_str:
                return "sqrt(exp(x)/3)"
            # Para otras cuadráticas: x = sqrt(expr/coef)
            coef_x2 = expr.coeff(x**2)
            if coef_x2 != 0:
                resto = expr - coef_x2 * x**2
                if resto != 0:
                    return f"sqrt(-({resto})/{coef_x2})"
        
        # Opción 2: x = expr/coeficiente si es lineal
        if expr.has(x) and not expr.has(x**2):
            coef_x = expr.coeff(x)
            if coef_x != 0:
                resto = expr - coef_x * x
                return f"-({resto})/{coef_x}"
        
        # Opción 3: x = expr + x (método general)
        return f"x - ({funcion_str})"
        
    except Exception:
        # Si falla, devolver una opción genérica
        return f"x - ({funcion_str})"

def calcular_derivada(funcion_str: str) -> str:
    """Calcula automáticamente la derivada de la función para Newton-Raphson."""
    try:
        x = sp.Symbol('x')
        expr = sp.sympify(funcion_str)
        derivada = sp.diff(expr, x)
        return str(derivada)
    except Exception:
        # Si falla, devolver una derivada genérica
        return f"d/dx({funcion_str})"

def generar_instrucciones_ejercicio_1(funcion: str, intervalo: list, semilla: float) -> str:
    """Genera instrucciones detalladas para el ejercicio 1 con todas las ecuaciones."""
    a, b = intervalo[0], intervalo[1]
    g_func = generar_funcion_punto_fijo(funcion)
    derivada = calcular_derivada(funcion)
    
    return f"""📝 INSTRUCCIONES DETALLADAS PARA LA HOJA - EJERCICIO 1

═══════════════════════════════════════════════════════════════════════════════

🔍 PASO 1: VERIFICAR EXISTENCIA DE RAÍZ (Teorema de Bolzano)

📋 Escribir en la hoja:
   f(x) = {funcion}
   
   Evaluar en los extremos del intervalo [{a}, {b}]:
   
   f({a}) = {funcion.replace('x', str(a))}
   f({b}) = {funcion.replace('x', str(b))}
   
   Como f({a}) y f({b}) tienen signos opuestos, por el Teorema de Bolzano
   existe al menos una raíz en el intervalo ({a}, {b}).

═══════════════════════════════════════════════════════════════════════════════

🚀 PARTE A: MÉTODO DE NEWTON-RAPHSON

📋 Escribir en la hoja:

   Fórmula de Newton-Raphson:
   x_{{n+1}} = x_n - f(x_n)/f'(x_n)
   
   donde:
   f(x) = {funcion}
   f'(x) = {derivada}
   
   Condición inicial: x₀ = {semilla}
   
   Tabla de iteraciones de Newton-Raphson:
   
   | n | x_n | f(x_n) | f'(x_n) | x_{{n+1}} = x_n - f(x_n)/f'(x_n) | Error |
   |---|-----|--------|---------|-----------------------------------|-------|
   | 0 | {semilla} | f({semilla}) = [calcular] | f'({semilla}) = [calcular] | {semilla} - [f({semilla})]/[f'({semilla})] = [resultado] | [calcular] |
   | 1 | [x_1] | f(x_1) = [calcular] | f'(x_1) = [calcular] | x_1 - [f(x_1)]/[f'(x_1)] = [resultado] | [calcular] |
   | 2 | [x_2] | f(x_2) = [calcular] | f'(x_2) = [calcular] | x_2 - [f(x_2)]/[f'(x_2)] = [resultado] | [calcular] |
   | ... | ... | ... | ... | ... | ... |
   
   Criterio de parada: |x_{{n+1}} - x_n| < 10⁻⁸

═══════════════════════════════════════════════════════════════════════════════

🔧 PARTE B: MÉTODO DE PUNTO FIJO + ACELERACIÓN DE AITKEN

📋 Escribir en la hoja:

   Para aplicar el método de punto fijo, despejamos x de la ecuación:
   {funcion} = 0
   
   Despejando x obtenemos:
   x = {g_func}
   
   Definimos: g(x) = {g_func}
   
   Fórmula de iteración de punto fijo:
   x_{{n+1}} = g(x_n)
   
   Fórmula de aceleración de Aitken:
   x̂_n = x_n - (x_{{n+1}} - x_n)² / (x_{{n+2}} - 2x_{{n+1}} + x_n)
   
   Condición inicial: x₀ = {semilla}
   
   Tabla de iteraciones de Punto Fijo + Aitken:
   
   | n | x_n | g(x_n) | x_{{n+1}} | x_{{n+2}} | x̂_n (Aitken) | Error |
   |---|-----|--------|-----------|-----------|---------------|-------|
   | 0 | {semilla} | g({semilla}) = [calcular] | [calcular] | [calcular] | [calcular] | [calcular] |
   | 1 | [resultado anterior] | g(x_1) = [calcular] | [calcular] | [calcular] | [calcular] | [calcular] |
   | 2 | ... | ... | ... | ... | ... | ... |
   
   Criterio de parada: |x_{{n+1}} - x_n| < 10⁻⁸

═══════════════════════════════════════════════════════════════════════════════

📊 PASO 3: COMPARACIÓN DE MÉTODOS

📋 Escribir en la hoja:

   Comparar ambos métodos:
   
   | Método | Iteraciones | Raíz aproximada | Error final |
   |--------|-------------|-----------------|-------------|
   | Newton-Raphson | [número] | x* ≈ [valor] | [error] |
   | Punto Fijo + Aitken | [número] | x* ≈ [valor] | [error] |
   
   Observaciones:
   • Newton-Raphson converge más rápido (orden 2)
   • Punto Fijo + Aitken es más estable
   • Ambos métodos convergen a la misma raíz

═══════════════════════════════════════════════════════════════════════════════

✅ PASO 4: RESULTADO FINAL

📋 Escribir en la hoja:
   
   La raíz aproximada es: x* ≈ [valor con 6 decimales]
   
   Verificación: f(x*) = {funcion.replace('x', 'x*')} ≈ [valor muy pequeño]
   
   Ambos métodos convergen a la misma solución, validando el resultado.

═══════════════════════════════════════════════════════════════════════════════"""

def generar_instrucciones_ejercicio_2(funcion: str, nodos: list, punto_eval: float) -> str:
    """Genera instrucciones detalladas para el ejercicio 2 con todas las ecuaciones."""
    x0, x1, x2 = nodos[0], nodos[1], nodos[2]
    
    return f"""📝 INSTRUCCIONES DETALLADAS PARA LA HOJA - EJERCICIO 2

═══════════════════════════════════════════════════════════════════════════════

📊 PASO 1: TABLA DE VALORES

📋 Escribir en la hoja:
   f(x) = {funcion}
   
   Nodos: x₀ = {x0}, x₁ = {x1}, x₂ = {x2}
   
   | i | x_i | y_i = f(x_i) |
   |---|-----|---------------|
   | 0 | {x0}  | {funcion.replace('x', str(x0))} |
   | 1 | {x1}  | {funcion.replace('x', str(x1))} |
   | 2 | {x2}  | {funcion.replace('x', str(x2))} |

═══════════════════════════════════════════════════════════════════════════════

🔧 PASO 2: CONSTRUCCIÓN DEL POLINOMIO DE LAGRANGE P₂(x)

📋 Escribir en la hoja:

   Fórmula general: P_n(x) = Σᵢ₌₀ⁿ y_i · L_i(x)
   
   Para n = 2: P₂(x) = y₀·L₀(x) + y₁·L₁(x) + y₂·L₂(x)
   
   Bases de Lagrange:
   
   L₀(x) = (x - x₁)(x - x₂) / (x₀ - x₁)(x₀ - x₂)
   L₀(x) = (x - {x1})(x - {x2}) / ({x0} - {x1})({x0} - {x2})
   L₀(x) = (x - {x1})(x - {x2}) / {x0-x1}·{x0-x2}
   
   L₁(x) = (x - x₀)(x - x₂) / (x₁ - x₀)(x₁ - x₂)
   L₁(x) = (x - {x0})(x - {x2}) / ({x1} - {x0})({x1} - {x2})
   L₁(x) = (x - {x0})(x - {x2}) / {x1-x0}·{x1-x2}
   
   L₂(x) = (x - x₀)(x - x₁) / (x₂ - x₀)(x₂ - x₁)
   L₂(x) = (x - {x0})(x - {x1}) / ({x2} - {x0})({x2} - {x1})
   L₂(x) = (x - {x0})(x - {x1}) / {x2-x0}·{x2-x1}

═══════════════════════════════════════════════════════════════════════════════

📈 PASO 3: EVALUACIÓN EN x = {punto_eval}

📋 Escribir en la hoja:

   Evaluar P₂(x) en x = {punto_eval}:
   
   L₀({punto_eval}) = ({punto_eval} - {x1})({punto_eval} - {x2}) / {x0-x1}·{x0-x2}
   L₀({punto_eval}) = [calcular] / [calcular] = [resultado]
   
   L₁({punto_eval}) = ({punto_eval} - {x0})({punto_eval} - {x2}) / {x1-x0}·{x1-x2}
   L₁({punto_eval}) = [calcular] / [calcular] = [resultado]
   
   L₂({punto_eval}) = ({punto_eval} - {x0})({punto_eval} - {x1}) / {x2-x0}·{x2-x1}
   L₂({punto_eval}) = [calcular] / [calcular] = [resultado]
   
   P₂({punto_eval}) = y₀·L₀({punto_eval}) + y₁·L₁({punto_eval}) + y₂·L₂({punto_eval})
   P₂({punto_eval}) = [y₀]·[L₀] + [y₁]·[L₁] + [y₂]·[L₂] = [resultado]
   
   Valor real: f({punto_eval}) = {funcion.replace('x', str(punto_eval))} = [resultado]
   
   Error absoluto: |f({punto_eval}) - P₂({punto_eval})| = |[real] - [interpolado]| = [error]

═══════════════════════════════════════════════════════════════════════════════

📐 PASO 4: DERIVADA POR DIFERENCIAS FINITAS

📋 Escribir en la hoja:

   Fórmula de diferencia central:
   f'(x) ≈ [f(x+h) - f(x-h)] / (2h)
   
   Usando el polinomio P₂(x) y h = 0.5:
   
   P₂'(1.5) ≈ [P₂(2.0) - P₂(1.0)] / (2·0.5)
   P₂'(1.5) ≈ [P₂(2.0) - P₂(1.0)] / 1.0
   P₂'(1.5) ≈ [calcular P₂(2.0)] - [calcular P₂(1.0)] = [resultado]
   
   Valor real: f'(1.5) = [derivada de {funcion} evaluada en 1.5] = [resultado]

═══════════════════════════════════════════════════════════════════════════════"""

def generar_instrucciones_ejercicio_3(funcion: str, intervalo: list) -> str:
    """Genera instrucciones detalladas para el ejercicio 3 con todas las ecuaciones."""
    a, b = intervalo[0], intervalo[1]
    
    return f"""📝 INSTRUCCIONES DETALLADAS PARA LA HOJA - EJERCICIO 3

═══════════════════════════════════════════════════════════════════════════════

🎯 PASO 1: IDENTIFICAR EL PROBLEMA

📋 Escribir en la hoja:
   Integrando: f(x) = {funcion}
   Intervalo: [{a}, {b}]
   
   Calcular: I = ∫_{a}^{b} {funcion} dx
   
   Como la primitiva de {funcion} no es elemental, usamos métodos numéricos.

═══════════════════════════════════════════════════════════════════════════════

📐 PASO 2: MÉTODO DEL TRAPECIO COMPUESTO

📋 Escribir en la hoja:

   Fórmula del trapecio compuesto:
   T_n = h/2 [f(a) + 2∑ᵢ₌₁ⁿ⁻¹ f(x_i) + f(b)]
   
   donde: h = (b-a)/n = ({b}-{a})/n = {b-a}/n
   
   Para n = 4:
   h = {b-a}/4 = {(b-a)/4}
   
   Puntos: x_i = a + i·h = {a} + i·{(b-a)/4}
   
   | i | x_i | f(x_i) = {funcion.replace('x', 'x_i')} |
   |---|-----|----------------------------------------|
   | 0 | {a}   | f({a}) = {funcion.replace('x', str(a))} |
   | 1 | {a + (b-a)/4} | f({a + (b-a)/4}) = {funcion.replace('x', str(a + (b-a)/4))} |
   | 2 | {a + 2*(b-a)/4} | f({a + 2*(b-a)/4}) = {funcion.replace('x', str(a + 2*(b-a)/4))} |
   | 3 | {a + 3*(b-a)/4} | f({a + 3*(b-a)/4}) = {funcion.replace('x', str(a + 3*(b-a)/4))} |
   | 4 | {b}   | f({b}) = {funcion.replace('x', str(b))} |
   
   T_4 = {(b-a)/4}/2 [f({a}) + 2f({a + (b-a)/4}) + 2f({a + 2*(b-a)/4}) + 2f({a + 3*(b-a)/4}) + f({b})]
   T_4 = {(b-a)/8} [f({a}) + 2f({a + (b-a)/4}) + 2f({a + 2*(b-a)/4}) + 2f({a + 3*(b-a)/4}) + f({b})]
   T_4 = [calcular] = [resultado]

═══════════════════════════════════════════════════════════════════════════════

📊 PASO 3: MÉTODO DE SIMPSON 1/3

📋 Escribir en la hoja:

   Fórmula de Simpson 1/3:
   S_n = h/3 [f(a) + 4∑f(x_impar) + 2∑f(x_par) + f(b)]
   
   Para n = 4 (debe ser par):
   h = {b-a}/4 = {(b-a)/4}
   
   S_4 = {(b-a)/4}/3 [f({a}) + 4f({a + (b-a)/4}) + 2f({a + 2*(b-a)/4}) + 4f({a + 3*(b-a)/4}) + f({b})]
   S_4 = {(b-a)/12} [f({a}) + 4f({a + (b-a)/4}) + 2f({a + 2*(b-a)/4}) + 4f({a + 3*(b-a)/4}) + f({b})]
   S_4 = [calcular] = [resultado]

═══════════════════════════════════════════════════════════════════════════════

📈 PASO 4: COMPARACIÓN Y ANÁLISIS

📋 Escribir en la hoja:

   | Método | n | Resultado | Error estimado |
   |--------|---|-----------|----------------|
   | Trapecio | 4 | T_4 = [resultado] | O(h²) |
   | Trapecio | 10 | T_10 = [resultado] | O(h²) |
   | Simpson | 4 | S_4 = [resultado] | O(h⁴) |
   
   Observaciones:
   • Simpson es más preciso que Trapecio para el mismo n
   • El error de Simpson es O(h⁴) vs O(h²) del Trapecio
   • Al aumentar n, ambos métodos convergen al valor real

═══════════════════════════════════════════════════════════════════════════════"""

def generar_instrucciones_ejercicio_4(funcion: str, dominio_x: list, dominio_y: list) -> str:
    """Genera instrucciones detalladas para el ejercicio 4 con todas las ecuaciones."""
    x_min, x_max = dominio_x[0], dominio_x[1]
    y_min, y_max = dominio_y[0], dominio_y[1]
    area = (x_max - x_min) * (y_max - y_min)
    
    return f"""📝 INSTRUCCIONES DETALLADAS PARA LA HOJA - EJERCICIO 4

═══════════════════════════════════════════════════════════════════════════════

🎯 PASO 1: IDENTIFICAR EL PROBLEMA

📋 Escribir en la hoja:
   Función: f(x,y) = {funcion}
   Dominio: x ∈ [{x_min}, {x_max}], y ∈ [{y_min}, {y_max}]
   
   Calcular: I = ∫_{x_min}^{x_max} ∫_{y_min}^{y_max} {funcion} dy dx
   
   Área del dominio: A = ({x_max} - {x_min}) × ({y_max} - {y_min}) = {x_max-x_min} × {y_max-y_min} = {area}

═══════════════════════════════════════════════════════════════════════════════

🎲 PASO 2: MÉTODO DE MONTE CARLO

📋 Escribir en la hoja:

   Método del promedio:
   Î_N = (1/N) ∑ᵢ₌₁ᴺ f(x_i, y_i) × A
   
   donde:
   • N = número de puntos aleatorios
   • (x_i, y_i) ~ Uniforme en [{x_min}, {x_max}] × [{y_min}, {y_max}]
   • A = {area} (área del dominio)
   
   Para N = 10000:
   
   | i | x_i | y_i | f(x_i, y_i) = {funcion.replace('x', 'x_i').replace('y', 'y_i')} |
   |---|-----|-----|----------------------------------------------------------------|
   | 1 | [random] | [random] | [calcular] |
   | 2 | [random] | [random] | [calcular] |
   | ... | ... | ... | ... |
   | 10000 | [random] | [random] | [calcular] |
   
   Î_10000 = (1/10000) × {area} × ∑ᵢ₌₁¹⁰⁰⁰⁰ f(x_i, y_i)
   Î_10000 = {area/10000} × [suma de todos los f(x_i, y_i)]
   Î_10000 = [resultado]

═══════════════════════════════════════════════════════════════════════════════

📊 PASO 3: ANÁLISIS ESTADÍSTICO

📋 Escribir en la hoja:

   Varianza muestral:
   s² = (1/(N-1)) ∑ᵢ₌₁ᴺ (f(x_i, y_i) - f̄)²
   
   donde f̄ = (1/N) ∑ᵢ₌₁ᴺ f(x_i, y_i)
   
   Error estándar:
   SE = s/√N
   
   Intervalo de confianza al 95%:
   IC_95% = Î_N ± 1.96 × SE × A
   
   Cálculos:
   f̄ = [promedio de f(x_i, y_i)] = [resultado]
   s² = [varianza] = [resultado]
   s = √s² = [resultado]
   SE = s/√10000 = [resultado]
   
   IC_95% = [Î_10000] ± 1.96 × [SE] × {area}
   IC_95% = [Î_10000] ± [margen de error]
   IC_95% = [[límite inferior], [límite superior]]

═══════════════════════════════════════════════════════════════════════════════

✅ PASO 4: RESULTADO FINAL

📋 Escribir en la hoja:

   Estimación Monte Carlo: Î ≈ [resultado]
   
   Intervalo de confianza al 95%: [[límite inferior], [límite superior]]
   
   Error relativo: |Î - I_exacto|/|I_exacto| × 100% = [porcentaje]%

═══════════════════════════════════════════════════════════════════════════════"""

def generar_instrucciones_ejercicio_5(funcion: str, condicion_inicial: list, intervalo: list, paso: str) -> str:
    """Genera instrucciones detalladas para el ejercicio 5 con todas las ecuaciones."""
    t0, y0 = condicion_inicial[0], condicion_inicial[1]
    t_end = intervalo[1]
    
    return f"""📝 INSTRUCCIONES DETALLADAS PARA LA HOJA - EJERCICIO 5

═══════════════════════════════════════════════════════════════════════════════

🎯 PASO 1: IDENTIFICAR EL PROBLEMA

📋 Escribir en la hoja:
   EDO: y' = {funcion}
   Condición inicial: y({t0}) = {y0}
   Intervalo: t ∈ [{t0}, {t_end}]
   Paso: h = {paso}
   
   Resolver numéricamente usando métodos de Euler y Runge-Kutta 4.

═══════════════════════════════════════════════════════════════════════════════

📐 PASO 2: MÉTODO DE EULER

📋 Escribir en la hoja:

   Fórmula de Euler:
   y_{{n+1}} = y_n + h·f(t_n, y_n)
   
   donde f(t,y) = {funcion}
   
   Tabla de iteraciones:
   
   | n | t_n | y_n | f(t_n, y_n) = {funcion.replace('t', 't_n').replace('y', 'y_n')} | y_{{n+1}} = y_n + h·f(t_n, y_n) |
   |---|-----|-----|----------------------------------------------------------------|-----------------------------------|
   | 0 | {t0} | {y0} | f({t0}, {y0}) = {funcion.replace('t', str(t0)).replace('y', str(y0))} | {y0} + {paso}·[f({t0}, {y0})] = [resultado] |
   | 1 | {t0} + {paso} | [y_1] | f(t_1, y_1) = [calcular] | y_1 + {paso}·[f(t_1, y_1)] = [resultado] |
   | 2 | t_1 + {paso} | [y_2] | f(t_2, y_2) = [calcular] | y_2 + {paso}·[f(t_2, y_2)] = [resultado] |
   | ... | ... | ... | ... | ... |

═══════════════════════════════════════════════════════════════════════════════

🚀 PASO 3: MÉTODO DE RUNGE-KUTTA 4

📋 Escribir en la hoja:

   Fórmulas de Runge-Kutta 4:
   k1 = f(t_n, y_n)
   k2 = f(t_n + h/2, y_n + (h/2)·k1)
   k3 = f(t_n + h/2, y_n + (h/2)·k2)
   k4 = f(t_n + h, y_n + h·k3)
   y_{{n+1}} = y_n + (h/6)(k1 + 2k2 + 2k3 + k4)
   
   Tabla de pendientes (primeras iteraciones):
   
   | n | t_n | y_n | k1 | k2 | k3 | k4 | y_{{n+1}} |
   |---|-----|-----|----|----|----|----|-----------|
   | 0 | {t0} | {y0} | f({t0}, {y0}) = [calcular] | f({t0}+{paso}/2, {y0}+{paso}/2·k1) = [calcular] | f({t0}+{paso}/2, {y0}+{paso}/2·k2) = [calcular] | f({t0}+{paso}, {y0}+{paso}·k3) = [calcular] | {y0} + {paso}/6·(k1 + 2k2 + 2k3 + k4) = [resultado] |
   | 1 | t_1 | y_1 | f(t_1, y_1) = [calcular] | f(t_1+h/2, y_1+h/2·k1) = [calcular] | f(t_1+h/2, y_1+h/2·k2) = [calcular] | f(t_1+h, y_1+h·k3) = [calcular] | y_1 + h/6·(k1 + 2k2 + 2k3 + k4) = [resultado] |

═══════════════════════════════════════════════════════════════════════════════

📊 PASO 4: COMPARACIÓN CON SOLUCIÓN ANALÍTICA

📋 Escribir en la hoja:

   Solución analítica: y(t) = [resolver la EDO]
   
   Comparación de errores:
   
   | Método | t | y_numérico | y_exacto | Error absoluto | Error relativo |
   |--------|---|------------|----------|----------------|----------------|
   | Euler | {t0} | {y0} | [y_exacto] | 0 | 0% |
   | Euler | t_1 | [y_1] | [y_exacto] | |[y_1] - [y_exacto]| | |[y_1] - [y_exacto]|/|[y_exacto]| × 100% |
   | RK4 | t_1 | [y_1_RK4] | [y_exacto] | |[y_1_RK4] - [y_exacto]| | |[y_1_RK4] - [y_exacto]|/|[y_exacto]| × 100% |
   
   Observaciones:
   • RK4 tiene mayor precisión que Euler
   • El error de Euler es O(h), el de RK4 es O(h⁴)
   • Para el mismo paso h, RK4 converge más rápido

═══════════════════════════════════════════════════════════════════════════════"""

def _make_safe_func(expr: str) -> Callable[[float], float]:
    """Compila una expresión en una función segura f(x)."""
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    allowed_names.update({"abs": abs, "pow": pow})
    expr_ast = ast.parse(expr, mode='eval')
    for node in ast.walk(expr_ast):
        if isinstance(node, ast.Name):
            if node.id != 'x' and node.id not in allowed_names:
                raise ValueError(f"Nombre no permitido en expresión: {node.id}")
        elif isinstance(node, (ast.Call, ast.BinOp, ast.UnaryOp, ast.Expression,
                               ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div,
                               ast.Pow, ast.USub, ast.UAdd, ast.Mod, ast.Constant,
                               ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.Gt,
                               ast.LtE, ast.GtE, ast.And, ast.Or, ast.BoolOp)):
            continue
        else:
            raise ValueError(f"Nodo AST no permitido: {type(node).__name__}")
    code = compile(expr_ast, '<string>', 'eval')
    def f(x: float) -> float:
        return eval(code, {'__builtins__': {}}, {**allowed_names, 'x': x})
    return f

def numerical_derivative(f: Callable[[float], float], x: float, h: float = 1e-6) -> float:
    return (f(x + h) - f(x - h)) / (2 * h)

def parse_function_sympy(expr_str):
    """Parsea función usando sympy."""
    x = sp.Symbol('x')
    expr_str = expr_str.replace("^", "**")
    try:
        expr = sp.sympify(expr_str, {"x": x, "e": sp.E, "pi": sp.pi})
    except Exception as e:
        raise ValueError(f"Expresión inválida: {e}")
    return expr, x

def f_num_numpy(expr_str):
    """Convierte expresión sympy a función numpy."""
    expr, x = parse_function_sympy(expr_str)
    return sp.lambdify(x, expr, 'numpy')

def valor_entry(s):
    """Convierte string a float, admite pi y E."""
    s = s.replace("pi","np.pi").replace("π","np.pi").replace("E","np.e")
    return float(eval(s))

# ============================================================================
# MÉTODOS NUMÉRICOS - PUNTO 1
# ============================================================================

def metodo_biseccion(f: Callable[[float], float], a: float, b: float, tol: float = 1e-8, max_iter: int = 50):
    if a >= b:
        raise ValueError("Se requiere a < b en bisección")
    fa, fb = f(a), f(b)
    if fa == 0:
        return a, [(0, a, b, a, f(a), 0.0, 0.0)]
    if fb == 0:
        return b, [(0, a, b, b, f(b), 0.0, 0.0)]
    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos (teorema de Bolzano)")
    history = []
    x_prev = None
    for n in range(1, max_iter + 1):
        m = (a + b) / 2
        fm = f(m)
        if x_prev is None:
            abs_err = float('inf')
            rel_err = float('inf')
        else:
            abs_err = abs(m - x_prev)
            rel_err = abs_err / abs(m) if m != 0 else float('inf')
        history.append((n, a, b, m, fm, abs_err, rel_err))
        if abs(fm) < tol or abs_err < tol or (b - a) / 2 < tol:
            return m, history
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
        x_prev = m
    return None, history

def newton_raphson(f: Callable[[float], float], x0: float, df: Optional[Callable[[float], float]] = None,
                   tol: float = 1e-8, max_iter: int = 50):
    history = []
    x = x0
    for n in range(max_iter):
        fx = f(x)
        dfx = df(x) if df is not None else numerical_derivative(f, x)
        if abs(dfx) < 1e-14:
            raise RuntimeError("Derivada cerca de cero; Newton puede fallar")
        x_next = x - fx / dfx
        abs_err = abs(x_next - x)
        rel_err = abs_err / abs(x_next) if x_next != 0 else float('inf')
        history.append((n, x, fx, dfx, abs_err, rel_err))
        if abs_err < tol:
            history.append((n + 1, x_next, f(x_next),
                            df(x_next) if df else numerical_derivative(f, x_next), 0.0, 0.0))
            return x_next, history
        x = x_next
    return None, history

def punto_fijo_aitken(g: Callable[[float], float], x0: float, tol: float = 1e-8, max_iter: int = 50):
    history = []
    x = x0
    for n in range(max_iter):
        x1 = g(x)
        x2 = g(x1)
        denom = x2 - 2 * x1 + x
        x_acc = x2 - (x2 - x1) ** 2 / denom if denom != 0 else x2
        abs_err = abs(x_acc - x)
        rel_err = abs_err / abs(x_acc) if x_acc != 0 else float('inf')
        history.append((n, x, x_acc, abs_err, rel_err))
        if abs_err < tol:
            return x_acc, history
        x = x_acc
    return None, history

# ============================================================================
# MÉTODOS NUMÉRICOS - PUNTO 2 (LAGRANGE)
# ============================================================================

def build_lagrange_polynomial(expr, x, nodes):
    """Construye polinomio de Lagrange."""
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

# ============================================================================
# MÉTODOS NUMÉRICOS - PUNTO 3 (INTEGRACIÓN)
# ============================================================================

def regla_trapecio(f, a, b, n):
    h = (b-a)/n
    x = np.linspace(a, b, n+1)
    y = f(x)
    I = h * (0.5*y[0] + np.sum(y[1:-1]) + 0.5*y[-1])
    tabla = [(i, x[i], y[i], 1 if i==0 or i==n else 2) for i in range(n+1)]
    return I, tabla, x

def regla_simpson_1_3(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("n debe ser par para Simpson 1/3")
    h = (b-a)/n
    x = np.linspace(a, b, n+1)
    y = f(x)
    I = h/3 * (y[0] + y[-1] + 4*np.sum(y[1::2]) + 2*np.sum(y[2:-1:2]))
    tabla = [(i, x[i], y[i], 1 if i==0 or i==n else (4 if i%2==1 else 2)) for i in range(n+1)]
    return I, tabla, x

# ============================================================================
# MÉTODOS NUMÉRICOS - PUNTO 4 (MONTE CARLO)
# ============================================================================

def monte_carlo_integral_2d(func_str, a, b, c, d, N, seed=0):
    """Monte Carlo para integral doble."""
    np.random.seed(seed)
    x_vals = np.random.uniform(a, b, N)
    y_vals = np.random.uniform(c, d, N)
    
    # Evaluar función
    def f(x, y):
        # Reemplazar x, y en la expresión
        expr = func_str.replace('x', f'({x})').replace('y', f'({y})')
        return eval(expr, {'exp': np.exp, 'sin': np.sin, 'cos': np.cos, 'e': np.e, 'pi': np.pi})
    
    f_vals = []
    for i in range(N):
        try:
            val = eval(func_str, {'x': x_vals[i], 'y': y_vals[i], 'exp': np.exp, 'e': np.e})
            f_vals.append(val)
        except:
            f_vals.append(0)
    
    f_vals = np.array(f_vals)
    area = (b-a) * (d-c)
    integral = area * np.mean(f_vals)
    
    return integral, f_vals, x_vals, y_vals

# ============================================================================
# MÉTODOS NUMÉRICOS - PUNTO 5 (RUNGE-KUTTA)
# ============================================================================

def runge_kutta_methods(func_str, t0, y0, t_end, h, method="RK4"):
    """Implementa diferentes métodos de Runge-Kutta."""
    def f(t, y):
        return eval(func_str, {'t': t, 'y': y, 'sin': np.sin, 'cos': np.cos, 'exp': np.exp, 'e': np.e, 'pi': np.pi})
    
    t_vals = np.arange(t0, t_end + h, h)
    y_vals = np.zeros(len(t_vals))
    y_vals[0] = y0
    
    history = []
    
    for i in range(len(t_vals) - 1):
        t = t_vals[i]
        y = y_vals[i]
        
        if method == "Euler":
            k1 = h * f(t, y)
            y_next = y + k1
            history.append((i, t, y, k1, 0, 0, 0, y_next))
            
        elif method == "RK4":
            k1 = h * f(t, y)
            k2 = h * f(t + h/2, y + k1/2)
            k3 = h * f(t + h/2, y + k2/2)
            k4 = h * f(t + h, y + k3)
            y_next = y + (k1 + 2*k2 + 2*k3 + k4)/6
            history.append((i, t, y, k1, k2, k3, k4, y_next))
        
        y_vals[i+1] = y_next
    
    return t_vals, y_vals, history

# ============================================================================
# CLASE PRINCIPAL
# ============================================================================

class SimuladorParcialUnificado:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("Simulador Parcial Unificado - Métodos Numéricos UADE")
        master.geometry("1400x900")
        
        # Variables de estado
        self.current_results = {}
        
        self._build_ui()
    
    def _build_ui(self):
        # Panel de información del parcial
        info_frame = ttk.LabelFrame(self.master, text="📚 Datos del Parcial Actual")
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        info_text = """EJERCICIO 1: f(x) = e^x - 3x² en [0,1] | EJERCICIO 2: f(x) = ln(x+1) en nodos [0,1,2]
EJERCICIO 3: f(x) = √2 * e^(x²) en [0,1] | EJERCICIO 4: f(x,y) = e^(2x-y) en [0,1]×[1,2]
EJERCICIO 5: y' = y*sin(t), y(0)=1, t∈[0,π]"""
        
        ttk.Label(info_frame, text=info_text, font=("Arial", 9)).pack(pady=5)
        
        # Notebook principal
        main_notebook = ttk.Notebook(self.master)
        main_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Crear pestañas para cada ejercicio
        self.create_ejercicio_1(main_notebook)
        self.create_ejercicio_2(main_notebook)
        self.create_ejercicio_3(main_notebook)
        self.create_ejercicio_4(main_notebook)
        self.create_ejercicio_5(main_notebook)
    
    def create_ejercicio_1(self, notebook):
        """Ejercicio 1: Búsqueda de Raíces"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Ejercicio 1: Raíces")
        
        # Panel de carga rápida
        carga_frame = ttk.LabelFrame(frame, text="🚀 Carga Rápida")
        carga_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(carga_frame, text="Cargar Datos del Parcial Actual", 
                  command=lambda: self.cargar_datos_ejercicio(1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(carga_frame, text="Limpiar Campos", 
                  command=lambda: self.limpiar_campos_ejercicio(1)).pack(side=tk.LEFT, padx=5)
        
        # Panel de explicación paso a paso
        expl_frame = ttk.LabelFrame(frame, text="🎯 Cómo Resolver el Ejercicio 1 - Paso a Paso")
        expl_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Crear notebook para diferentes secciones
        expl_notebook = ttk.Notebook(expl_frame)
        expl_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña 1: Explicación General
        self.create_explicacion_general(expl_notebook)
        
        # Pestaña 2: Newton-Raphson
        self.create_explicacion_newton(expl_notebook)
        
        # Pestaña 3: Punto Fijo + Aitken
        self.create_explicacion_punto_fijo(expl_notebook)
        
        # Pestaña 4: Instrucciones para la Hoja
        self.create_instrucciones_hoja(expl_notebook)
        
        # Panel de entrada
        input_frame = ttk.LabelFrame(frame, text="Parámetros del Ejercicio 1")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="f(x):").grid(row=0, column=0, sticky='w')
        self.ej1_func = tk.StringVar(value="exp(x) - 3*x**2")
        self.ej1_func_entry = ttk.Entry(input_frame, textvariable=self.ej1_func, width=30)
        self.ej1_func_entry.grid(row=0, column=1, sticky='we')
        self.ej1_func.trace_add('write', lambda *args: self.actualizar_instrucciones_ejercicio_1())
        
        ttk.Label(input_frame, text="g(x) (punto fijo):").grid(row=1, column=0, sticky='w')
        self.ej1_g = tk.StringVar(value="sqrt(exp(x)/3)")
        self.ej1_g_entry = ttk.Entry(input_frame, textvariable=self.ej1_g, width=30)
        self.ej1_g_entry.grid(row=1, column=1, sticky='we')
        
        ttk.Button(input_frame, text="🔧 Generar g(x) automáticamente", 
                  command=self.generar_gx_automatico).grid(row=1, column=2, padx=5)
        
        ttk.Label(input_frame, text="x₀:").grid(row=2, column=0, sticky='w')
        self.ej1_x0 = tk.StringVar(value="0.5")
        self.ej1_x0_entry = ttk.Entry(input_frame, textvariable=self.ej1_x0, width=10)
        self.ej1_x0_entry.grid(row=2, column=1, sticky='w')
        self.ej1_x0.trace_add('write', lambda *args: self.actualizar_instrucciones_ejercicio_1())
        
        ttk.Button(input_frame, text="🚀 Resolver Ejercicio 1", 
                  command=self.resolver_ejercicio_1).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Panel de resultados
        result_frame = ttk.LabelFrame(frame, text="Resultados")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tabla de iteraciones
        self.ej1_tree = ttk.Treeview(result_frame, columns=("n", "x_n", "x_acc", "err_abs", "err_rel"), show='headings')
        for col in ("n", "x_n", "x_acc", "err_abs", "err_rel"):
            self.ej1_tree.heading(col, text=col)
            self.ej1_tree.column(col, width=100)
        self.ej1_tree.pack(fill=tk.BOTH, expand=True)
    
    def create_ejercicio_2(self, notebook):
        """Ejercicio 2: Interpolación de Lagrange"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Ejercicio 2: Lagrange")
        
        # Panel de carga rápida
        carga_frame = ttk.LabelFrame(frame, text="🚀 Carga Rápida")
        carga_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(carga_frame, text="Cargar Datos del Parcial Actual", 
                  command=lambda: self.cargar_datos_ejercicio(2)).pack(side=tk.LEFT, padx=5)
        ttk.Button(carga_frame, text="Limpiar Campos", 
                  command=lambda: self.limpiar_campos_ejercicio(2)).pack(side=tk.LEFT, padx=5)
        
        # Panel de instrucciones
        inst_frame = ttk.LabelFrame(frame, text="📋 Qué escribir en la hoja")
        inst_frame.pack(fill=tk.X, padx=5, pady=5)
        
        instructions = """PASO A PASO PARA LA HOJA:

1. TABLA DE VALORES:
   • f(x) = ln(x+1) con nodos x₀=0, x₁=1, x₂=2
   • y₀ = ln(1) = 0
   • y₁ = ln(2) ≈ 0.6931
   • y₂ = ln(3) ≈ 1.0986

2. BASES DE LAGRANGE:
   • L₀(x) = (x-1)(x-2)/((0-1)(0-2)) = (x-1)(x-2)/2
   • L₁(x) = (x-0)(x-2)/((1-0)(1-2)) = -x(x-2)
   • L₂(x) = (x-0)(x-1)/((2-0)(2-1)) = x(x-1)/2

3. POLINOMIO DE LAGRANGE:
   • P₂(x) = y₀L₀(x) + y₁L₁(x) + y₂L₂(x)
   • Expandir y simplificar

4. EVALUAR EN ξ = 0.5:
   • Calcular P₂(0.5) y f(0.5)
   • Error = |f(0.5) - P₂(0.5)|

5. DERIVADA EN x = 1:
   • P₂'(1) vs f'(1) = 1/2"""
        
        inst_text = tk.Text(inst_frame, height=12, wrap=tk.WORD)
        inst_text.insert(tk.END, instructions)
        inst_text.config(state=tk.DISABLED)
        inst_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel de entrada
        input_frame = ttk.LabelFrame(frame, text="Parámetros del Ejercicio 2")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="f(x):").grid(row=0, column=0, sticky='w')
        self.ej2_func = tk.StringVar(value="log(x+1)")
        ttk.Entry(input_frame, textvariable=self.ej2_func, width=30).grid(row=0, column=1, sticky='we')
        
        ttk.Label(input_frame, text="Nodos (separados por coma):").grid(row=1, column=0, sticky='w')
        self.ej2_nodes = tk.StringVar(value="0,1,2")
        ttk.Entry(input_frame, textvariable=self.ej2_nodes, width=30).grid(row=1, column=1, sticky='we')
        
        ttk.Label(input_frame, text="Punto ξ para evaluar:").grid(row=2, column=0, sticky='w')
        self.ej2_xi = tk.StringVar(value="0.5")
        ttk.Entry(input_frame, textvariable=self.ej2_xi, width=10).grid(row=2, column=1, sticky='w')
        
        ttk.Button(input_frame, text="🚀 Resolver Ejercicio 2", 
                  command=self.resolver_ejercicio_2).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Panel de resultados
        result_frame = ttk.LabelFrame(frame, text="Resultados")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.ej2_result = scrolledtext.ScrolledText(result_frame, height=15)
        self.ej2_result.pack(fill=tk.BOTH, expand=True)
    
    def create_ejercicio_3(self, notebook):
        """Ejercicio 3: Integración Numérica"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Ejercicio 3: Integración")
        
        # Panel de carga rápida
        carga_frame = ttk.LabelFrame(frame, text="🚀 Carga Rápida")
        carga_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(carga_frame, text="Cargar Datos del Parcial Actual", 
                  command=lambda: self.cargar_datos_ejercicio(3)).pack(side=tk.LEFT, padx=5)
        ttk.Button(carga_frame, text="Limpiar Campos", 
                  command=lambda: self.limpiar_campos_ejercicio(3)).pack(side=tk.LEFT, padx=5)
        
        # Panel de instrucciones
        inst_frame = ttk.LabelFrame(frame, text="📋 Qué escribir en la hoja")
        inst_frame.pack(fill=tk.X, padx=5, pady=5)
        
        instructions = """PASO A PASO PARA LA HOJA:

1. IDENTIFICAR LA INTEGRAL:
   • I = ∫₀¹ √2 · e^(x²) dx
   • Esta integral no tiene solución analítica elemental

2. REGLA DEL TRAPECIO (n=4):
   • h = (1-0)/4 = 0.25
   • x₀=0, x₁=0.25, x₂=0.5, x₃=0.75, x₄=1
   • Calcular f(xᵢ) para cada punto
   • T₄ = h[½f(x₀) + f(x₁) + f(x₂) + f(x₃) + ½f(x₄)]

3. REGLA DE SIMPSON 1/3 (n=4):
   • Mismos puntos que trapecio
   • S₄ = (h/3)[f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + f(x₄)]

4. COMPARAR RESULTADOS:
   • Mostrar tabla con xᵢ, f(xᵢ), coeficientes
   • Calcular T₄ y S₄
   • Error estimado entre métodos"""
        
        inst_text = tk.Text(inst_frame, height=10, wrap=tk.WORD)
        inst_text.insert(tk.END, instructions)
        inst_text.config(state=tk.DISABLED)
        inst_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel de entrada
        input_frame = ttk.LabelFrame(frame, text="Parámetros del Ejercicio 3")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="f(x):").grid(row=0, column=0, sticky='w')
        self.ej3_func = tk.StringVar(value="sqrt(2)*exp(x**2)")
        ttk.Entry(input_frame, textvariable=self.ej3_func, width=30).grid(row=0, column=1, sticky='we')
        
        ttk.Label(input_frame, text="a:").grid(row=1, column=0, sticky='w')
        self.ej3_a = tk.StringVar(value="0")
        ttk.Entry(input_frame, textvariable=self.ej3_a, width=10).grid(row=1, column=1, sticky='w')
        
        ttk.Label(input_frame, text="b:").grid(row=1, column=2, sticky='w')
        self.ej3_b = tk.StringVar(value="1")
        ttk.Entry(input_frame, textvariable=self.ej3_b, width=10).grid(row=1, column=3, sticky='w')
        
        ttk.Label(input_frame, text="n:").grid(row=2, column=0, sticky='w')
        self.ej3_n = tk.StringVar(value="4")
        ttk.Entry(input_frame, textvariable=self.ej3_n, width=10).grid(row=2, column=1, sticky='w')
        
        ttk.Button(input_frame, text="🚀 Resolver Ejercicio 3", 
                  command=self.resolver_ejercicio_3).grid(row=3, column=0, columnspan=4, pady=10)
        
        # Panel de resultados
        result_frame = ttk.LabelFrame(frame, text="Resultados")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tabla
        self.ej3_tree = ttk.Treeview(result_frame, columns=("i", "x_i", "f(x_i)", "coef_trap", "coef_simp"), show='headings')
        for col in ("i", "x_i", "f(x_i)", "coef_trap", "coef_simp"):
            self.ej3_tree.heading(col, text=col)
            self.ej3_tree.column(col, width=100)
        self.ej3_tree.pack(fill=tk.BOTH, expand=True)
        
        # Resultados finales
        self.ej3_final = tk.Text(result_frame, height=5)
        self.ej3_final.pack(fill=tk.X, pady=5)
    
    def create_ejercicio_4(self, notebook):
        """Ejercicio 4: Monte Carlo"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Ejercicio 4: Monte Carlo")
        
        # Panel de carga rápida
        carga_frame = ttk.LabelFrame(frame, text="🚀 Carga Rápida")
        carga_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(carga_frame, text="Cargar Datos del Parcial Actual", 
                  command=lambda: self.cargar_datos_ejercicio(4)).pack(side=tk.LEFT, padx=5)
        ttk.Button(carga_frame, text="Limpiar Campos", 
                  command=lambda: self.limpiar_campos_ejercicio(4)).pack(side=tk.LEFT, padx=5)
        
        # Panel de instrucciones
        inst_frame = ttk.LabelFrame(frame, text="📋 Qué escribir en la hoja")
        inst_frame.pack(fill=tk.X, padx=5, pady=5)
        
        instructions = """PASO A PASO PARA LA HOJA:

1. SOLUCIÓN ANALÍTICA:
   • I = ∫₀¹∫₁² e^(2x-y) dy dx
   • Integrar respecto a y: ∫₁² e^(2x-y) dy = e^(2x)[e^(-1) - e^(-2)]
   • Integrar respecto a x: I = (e^(-1) - e^(-2)) · (e² - 1)/2
   • Valor exacto ≈ 0.742869

2. MÉTODO MONTE CARLO:
   • Dominio: [0,1] × [1,2], área = 1
   • Generar N puntos aleatorios (xᵢ, yᵢ)
   • Calcular f(xᵢ, yᵢ) = e^(2xᵢ - yᵢ)
   • Estimación: Î = (1/N) Σf(xᵢ, yᵢ)

3. ANÁLISIS ESTADÍSTICO:
   • Media muestral
   • Desviación estándar
   • Intervalo de confianza 95%
   • Error relativo vs valor exacto"""
        
        inst_text = tk.Text(inst_frame, height=10, wrap=tk.WORD)
        inst_text.insert(tk.END, instructions)
        inst_text.config(state=tk.DISABLED)
        inst_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel de entrada
        input_frame = ttk.LabelFrame(frame, text="Parámetros del Ejercicio 4")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="f(x,y):").grid(row=0, column=0, sticky='w')
        self.ej4_func = tk.StringVar(value="exp(2*x - y)")
        ttk.Entry(input_frame, textvariable=self.ej4_func, width=30).grid(row=0, column=1, sticky='we')
        
        ttk.Label(input_frame, text="N (muestras):").grid(row=1, column=0, sticky='w')
        self.ej4_N = tk.StringVar(value="1000")
        ttk.Entry(input_frame, textvariable=self.ej4_N, width=10).grid(row=1, column=1, sticky='w')
        
        ttk.Label(input_frame, text="Semilla:").grid(row=1, column=2, sticky='w')
        self.ej4_seed = tk.StringVar(value="0")
        ttk.Entry(input_frame, textvariable=self.ej4_seed, width=10).grid(row=1, column=3, sticky='w')
        
        ttk.Button(input_frame, text="🚀 Resolver Ejercicio 4", 
                  command=self.resolver_ejercicio_4).grid(row=2, column=0, columnspan=4, pady=10)
        
        # Panel de resultados
        result_frame = ttk.LabelFrame(frame, text="Resultados")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.ej4_result = scrolledtext.ScrolledText(result_frame, height=15)
        self.ej4_result.pack(fill=tk.BOTH, expand=True)
    
    def create_ejercicio_5(self, notebook):
        """Ejercicio 5: Runge-Kutta"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Ejercicio 5: Runge-Kutta")
        
        # Panel de carga rápida
        carga_frame = ttk.LabelFrame(frame, text="🚀 Carga Rápida")
        carga_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(carga_frame, text="Cargar Datos del Parcial Actual", 
                  command=lambda: self.cargar_datos_ejercicio(5)).pack(side=tk.LEFT, padx=5)
        ttk.Button(carga_frame, text="Limpiar Campos", 
                  command=lambda: self.limpiar_campos_ejercicio(5)).pack(side=tk.LEFT, padx=5)
        
        # Panel de instrucciones
        inst_frame = ttk.LabelFrame(frame, text="📋 Qué escribir en la hoja")
        inst_frame.pack(fill=tk.X, padx=5, pady=5)
        
        instructions = """PASO A PASO PARA LA HOJA:

1. PROBLEMA INICIAL:
   • dy/dx = y·sin(x), y(0) = 1
   • Intervalo: [0, π], h = π/10

2. SOLUCIÓN ANALÍTICA:
   • Separar variables: dy/y = sin(x)dx
   • Integrar: ln|y| = -cos(x) + C
   • Con y(0) = 1: C = 1 + cos(0) = 2
   • Solución: y(x) = e^(2-cos(x))

3. MÉTODO DE EULER (inciso a):
   • Fórmula: yₙ₊₁ = yₙ + h·f(xₙ, yₙ)
   • Mostrar primeras 3 iteraciones paso a paso

4. MÉTODO RK4 (inciso b):
   • Fórmulas: k₁, k₂, k₃, k₄
   • yₙ₊₁ = yₙ + (k₁ + 2k₂ + 2k₃ + k₄)/6
   • Tabla completa con todas las pendientes"""
        
        inst_text = tk.Text(inst_frame, height=10, wrap=tk.WORD)
        inst_text.insert(tk.END, instructions)
        inst_text.config(state=tk.DISABLED)
        inst_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Panel de entrada
        input_frame = ttk.LabelFrame(frame, text="Parámetros del Ejercicio 5")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(input_frame, text="f(t,y):").grid(row=0, column=0, sticky='w')
        self.ej5_func = tk.StringVar(value="y*sin(t)")
        ttk.Entry(input_frame, textvariable=self.ej5_func, width=30).grid(row=0, column=1, sticky='we')
        
        ttk.Label(input_frame, text="t₀:").grid(row=1, column=0, sticky='w')
        self.ej5_t0 = tk.StringVar(value="0")
        ttk.Entry(input_frame, textvariable=self.ej5_t0, width=10).grid(row=1, column=1, sticky='w')
        
        ttk.Label(input_frame, text="y₀:").grid(row=1, column=2, sticky='w')
        self.ej5_y0 = tk.StringVar(value="1")
        ttk.Entry(input_frame, textvariable=self.ej5_y0, width=10).grid(row=1, column=3, sticky='w')
        
        ttk.Label(input_frame, text="t_end:").grid(row=2, column=0, sticky='w')
        self.ej5_tend = tk.StringVar(value="pi")
        ttk.Entry(input_frame, textvariable=self.ej5_tend, width=10).grid(row=2, column=1, sticky='w')
        
        ttk.Label(input_frame, text="h:").grid(row=2, column=2, sticky='w')
        self.ej5_h = tk.StringVar(value="pi/10")
        ttk.Entry(input_frame, textvariable=self.ej5_h, width=10).grid(row=2, column=3, sticky='w')
        
        method_frame = ttk.Frame(input_frame)
        method_frame.grid(row=3, column=0, columnspan=4, pady=5)
        
        ttk.Button(method_frame, text="🚀 Euler", 
                  command=lambda: self.resolver_ejercicio_5("Euler")).pack(side=tk.LEFT, padx=5)
        ttk.Button(method_frame, text="🚀 RK4", 
                  command=lambda: self.resolver_ejercicio_5("RK4")).pack(side=tk.LEFT, padx=5)
        
        # Panel de resultados
        result_frame = ttk.LabelFrame(frame, text="Resultados")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tabla
        self.ej5_tree = ttk.Treeview(result_frame, columns=("n", "t", "y", "k1", "k2", "k3", "k4", "y_next"), show='headings')
        for col in ("n", "t", "y", "k1", "k2", "k3", "k4", "y_next"):
            self.ej5_tree.heading(col, text=col)
            self.ej5_tree.column(col, width=80)
        self.ej5_tree.pack(fill=tk.BOTH, expand=True)
    
    # ========================================================================
    # MÉTODOS DE RESOLUCIÓN
    # ========================================================================
    
    def resolver_ejercicio_1(self):
        """Resolver búsqueda de raíces."""
        try:
            # Limpiar tabla
            for item in self.ej5_tree.get_children():
                self.ej1_tree.delete(item)
            
            g = _make_safe_func(self.ej1_g.get())
            x0 = float(self.ej1_x0.get())
            
            root, history = punto_fijo_aitken(g, x0, tol=1e-8, max_iter=20)
            
            # Llenar tabla
            for rec in history:
                vals = [f"{v:.6f}" if isinstance(v, float) else str(v) for v in rec]
                self.ej1_tree.insert('', 'end', values=vals)
            
            messagebox.showinfo("Resultado", f"Raíz encontrada: {root:.6f}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def resolver_ejercicio_2(self):
        """Resolver interpolación de Lagrange."""
        try:
            self.ej2_result.delete('1.0', tk.END)
            
            expr, x = parse_function_sympy(self.ej2_func.get())
            nodes = [float(n.strip()) for n in self.ej2_nodes.get().split(',')]
            xi = float(self.ej2_xi.get())
            
            # Construir polinomio
            P, y_vals, L_terms = build_lagrange_polynomial(expr, x, nodes)
            
            # Resultados
            result = f"EJERCICIO 2 - INTERPOLACIÓN DE LAGRANGE\n"
            result += "="*50 + "\n\n"
            
            result += "1. TABLA DE VALORES:\n"
            for i, (node, y_val) in enumerate(zip(nodes, y_vals)):
                result += f"   x_{i} = {node}, y_{i} = {y_val:.6f}\n"
            
            result += "\n2. BASES DE LAGRANGE:\n"
            for i, L_i in enumerate(L_terms):
                result += f"   L_{i}(x) = {L_i}\n"
            
            result += f"\n3. POLINOMIO DE LAGRANGE:\n"
            result += f"   P(x) = {P}\n"
            
            # Evaluar en xi
            P_xi = float(P.subs(x, xi))
            f_xi = float(expr.subs(x, xi))
            error = abs(f_xi - P_xi)
            
            result += f"\n4. EVALUACIÓN EN ξ = {xi}:\n"
            result += f"   P({xi}) = {P_xi:.6f}\n"
            result += f"   f({xi}) = {f_xi:.6f}\n"
            result += f"   Error = |f(ξ) - P(ξ)| = {error:.6f}\n"
            
            # Derivada
            P_prime = sp.diff(P, x)
            f_prime = sp.diff(expr, x)
            
            result += f"\n5. DERIVADAS EN x = 1:\n"
            result += f"   P'(1) = {float(P_prime.subs(x, 1)):.6f}\n"
            result += f"   f'(1) = {float(f_prime.subs(x, 1)):.6f}\n"
            
            self.ej2_result.insert('1.0', result)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def resolver_ejercicio_3(self):
        """Resolver integración numérica."""
        try:
            # Limpiar tabla
            for item in self.ej3_tree.get_children():
                self.ej3_tree.delete(item)
            
            self.ej3_final.delete('1.0', tk.END)
            
            f = f_num_numpy(self.ej3_func.get())
            a = valor_entry(self.ej3_a.get())
            b = valor_entry(self.ej3_b.get())
            n = int(self.ej3_n.get())
            
            # Trapecio
            I_trap, tabla_trap, x_vals = regla_trapecio(f, a, b, n)
            
            # Simpson
            try:
                I_simp, tabla_simp, _ = regla_simpson_1_3(f, a, b, n)
            except:
                I_simp = "N/A (n debe ser par)"
            
            # Llenar tabla
            for i, (x_i, f_xi, coef_t) in enumerate([(x, f(x), t[3]) for x, t in zip(x_vals, tabla_trap)]):
                if isinstance(I_simp, str):
                    coef_s = "N/A"
                else:
                    coef_s = tabla_simp[i][3]
                
                self.ej3_tree.insert('', 'end', values=(
                    i, f"{x_i:.3f}", f"{f_xi:.6f}", coef_t, coef_s
                ))
            
            # Resultados finales
            result = f"RESULTADOS:\n"
            result += f"Trapecio: I ≈ {I_trap:.6f}\n"
            result += f"Simpson:  I ≈ {I_simp if isinstance(I_simp, str) else f'{I_simp:.6f}'}\n"
            if not isinstance(I_simp, str):
                result += f"Diferencia: {abs(I_trap - I_simp):.6f}\n"
            
            self.ej3_final.insert('1.0', result)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def resolver_ejercicio_4(self):
        """Resolver Monte Carlo."""
        try:
            self.ej4_result.delete('1.0', tk.END)
            
            func_str = self.ej4_func.get()
            N = int(self.ej4_N.get())
            seed = int(self.ej4_seed.get())
            
            # Valor analítico
            valor_exacto = (np.e**(-1) - np.e**(-2)) * (np.e**2 - 1) / 2
            
            # Monte Carlo
            integral_mc, f_vals, x_vals, y_vals = monte_carlo_integral_2d(
                func_str, 0, 1, 1, 2, N, seed
            )
            
            # Estadísticas
            media = np.mean(f_vals)
            std = np.std(f_vals, ddof=1)
            error_std = std / np.sqrt(N)
            
            # Intervalo de confianza 95%
            alpha = 0.05
            t_val = stats.t.ppf(1 - alpha/2, N-1)
            ic_inf = integral_mc - t_val * error_std
            ic_sup = integral_mc + t_val * error_std
            
            error_relativo = abs(integral_mc - valor_exacto) / valor_exacto * 100
            
            result = f"EJERCICIO 4 - MONTE CARLO\n"
            result += "="*50 + "\n\n"
            
            result += f"1. VALOR ANALÍTICO:\n"
            result += f"   I_exacto = {valor_exacto:.6f}\n\n"
            
            result += f"2. MONTE CARLO (N = {N}):\n"
            result += f"   Estimación: {integral_mc:.6f}\n"
            result += f"   Media muestral: {media:.6f}\n"
            result += f"   Desv. estándar: {std:.6f}\n"
            result += f"   Error estándar: {error_std:.6f}\n\n"
            
            result += f"3. INTERVALO CONFIANZA 95%:\n"
            result += f"   [{ic_inf:.6f}, {ic_sup:.6f}]\n\n"
            
            result += f"4. ANÁLISIS DE ERROR:\n"
            result += f"   Error absoluto: {abs(integral_mc - valor_exacto):.6f}\n"
            result += f"   Error relativo: {error_relativo:.2f}%\n"
            
            self.ej4_result.insert('1.0', result)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def resolver_ejercicio_5(self, method):
        """Resolver Runge-Kutta."""
        try:
            # Limpiar tabla
            for item in self.ej5_tree.get_children():
                self.ej5_tree.delete(item)
            
            func_str = self.ej5_func.get()
            t0 = valor_entry(self.ej5_t0.get())
            y0 = float(self.ej5_y0.get())
            t_end = valor_entry(self.ej5_tend.get())
            h = valor_entry(self.ej5_h.get())
            
            t_vals, y_vals, history = runge_kutta_methods(func_str, t0, y0, t_end, h, method)
            
            # Llenar tabla
            for rec in history:
                vals = [f"{v:.6f}" if isinstance(v, float) else str(v) for v in rec]
                self.ej5_tree.insert('', 'end', values=vals)
            
            messagebox.showinfo("Resultado", f"Método {method} completado.\nValor final: y({t_end:.3f}) ≈ {y_vals[-1]:.6f}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def cargar_datos_ejercicio(self, ejercicio_num: int):
        """Carga los datos del parcial actual para el ejercicio especificado."""
        try:
            datos = cargar_datos_parcial(f"ejercicio_{ejercicio_num}")
            if not datos:
                messagebox.showwarning("Advertencia", f"No hay datos predefinidos para el ejercicio {ejercicio_num}")
                return
            
            if ejercicio_num == 1:
                # Cargar datos para ejercicio 1 (raíces)
                if hasattr(self, 'ej1_func_entry'):
                    self.ej1_func_entry.delete(0, tk.END)
                    self.ej1_func_entry.insert(0, datos['funcion'])
                if hasattr(self, 'ej1_a_entry'):
                    self.ej1_a_entry.delete(0, tk.END)
                    self.ej1_a_entry.insert(0, str(datos['intervalo'][0]))
                if hasattr(self, 'ej1_b_entry'):
                    self.ej1_b_entry.delete(0, tk.END)
                    self.ej1_b_entry.insert(0, str(datos['intervalo'][1]))
                if hasattr(self, 'ej1_semilla_entry'):
                    self.ej1_semilla_entry.delete(0, tk.END)
                    self.ej1_semilla_entry.insert(0, str(datos['semilla']))
                    
            elif ejercicio_num == 2:
                # Cargar datos para ejercicio 2 (interpolación)
                if hasattr(self, 'ej2_func_entry'):
                    self.ej2_func_entry.delete(0, tk.END)
                    self.ej2_func_entry.insert(0, datos['funcion'])
                if hasattr(self, 'ej2_nodos_entry'):
                    self.ej2_nodos_entry.delete(0, tk.END)
                    self.ej2_nodos_entry.insert(0, str(datos['nodos']))
                if hasattr(self, 'ej2_eval_entry'):
                    self.ej2_eval_entry.delete(0, tk.END)
                    self.ej2_eval_entry.insert(0, str(datos['punto_evaluacion']))
                    
            elif ejercicio_num == 3:
                # Cargar datos para ejercicio 3 (integración)
                if hasattr(self, 'ej3_func_entry'):
                    self.ej3_func_entry.delete(0, tk.END)
                    self.ej3_func_entry.insert(0, datos['funcion'])
                if hasattr(self, 'ej3_a_entry'):
                    self.ej3_a_entry.delete(0, tk.END)
                    self.ej3_a_entry.insert(0, str(datos['intervalo'][0]))
                if hasattr(self, 'ej3_b_entry'):
                    self.ej3_b_entry.delete(0, tk.END)
                    self.ej3_b_entry.insert(0, str(datos['intervalo'][1]))
                    
            elif ejercicio_num == 4:
                # Cargar datos para ejercicio 4 (integrales dobles)
                if hasattr(self, 'ej4_func_entry'):
                    self.ej4_func_entry.delete(0, tk.END)
                    self.ej4_func_entry.insert(0, datos['funcion'])
                if hasattr(self, 'ej4_xmin_entry'):
                    self.ej4_xmin_entry.delete(0, tk.END)
                    self.ej4_xmin_entry.insert(0, str(datos['dominio_x'][0]))
                if hasattr(self, 'ej4_xmax_entry'):
                    self.ej4_xmax_entry.delete(0, tk.END)
                    self.ej4_xmax_entry.insert(0, str(datos['dominio_x'][1]))
                if hasattr(self, 'ej4_ymin_entry'):
                    self.ej4_ymin_entry.delete(0, tk.END)
                    self.ej4_ymin_entry.insert(0, str(datos['dominio_y'][0]))
                if hasattr(self, 'ej4_ymax_entry'):
                    self.ej4_ymax_entry.delete(0, tk.END)
                    self.ej4_ymax_entry.insert(0, str(datos['dominio_y'][1]))
                    
            elif ejercicio_num == 5:
                # Cargar datos para ejercicio 5 (EDO)
                if hasattr(self, 'ej5_func_entry'):
                    self.ej5_func_entry.delete(0, tk.END)
                    self.ej5_func_entry.insert(0, datos['funcion'])
                if hasattr(self, 'ej5_t0_entry'):
                    self.ej5_t0_entry.delete(0, tk.END)
                    self.ej5_t0_entry.insert(0, str(datos['condicion_inicial'][0]))
                if hasattr(self, 'ej5_y0_entry'):
                    self.ej5_y0_entry.delete(0, tk.END)
                    self.ej5_y0_entry.insert(0, str(datos['condicion_inicial'][1]))
                if hasattr(self, 'ej5_tend_entry'):
                    self.ej5_tend_entry.delete(0, tk.END)
                    self.ej5_tend_entry.insert(0, str(datos['intervalo'][1]))
                if hasattr(self, 'ej5_h_entry'):
                    self.ej5_h_entry.delete(0, tk.END)
                    self.ej5_h_entry.insert(0, str(datos['paso']))
            
            # Actualizar instrucciones después de cargar datos
            if ejercicio_num == 1:
                self.actualizar_instrucciones_ejercicio_1()
            
            messagebox.showinfo("Éxito", f"Datos del parcial actual cargados para el ejercicio {ejercicio_num}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def limpiar_campos_ejercicio(self, ejercicio_num: int):
        """Limpia todos los campos del ejercicio especificado."""
        try:
            if ejercicio_num == 1:
                if hasattr(self, 'ej1_func_entry'):
                    self.ej1_func_entry.delete(0, tk.END)
                if hasattr(self, 'ej1_a_entry'):
                    self.ej1_a_entry.delete(0, tk.END)
                if hasattr(self, 'ej1_b_entry'):
                    self.ej1_b_entry.delete(0, tk.END)
                if hasattr(self, 'ej1_semilla_entry'):
                    self.ej1_semilla_entry.delete(0, tk.END)
                    
            elif ejercicio_num == 2:
                if hasattr(self, 'ej2_func_entry'):
                    self.ej2_func_entry.delete(0, tk.END)
                if hasattr(self, 'ej2_nodos_entry'):
                    self.ej2_nodos_entry.delete(0, tk.END)
                if hasattr(self, 'ej2_eval_entry'):
                    self.ej2_eval_entry.delete(0, tk.END)
                    
            elif ejercicio_num == 3:
                if hasattr(self, 'ej3_func_entry'):
                    self.ej3_func_entry.delete(0, tk.END)
                if hasattr(self, 'ej3_a_entry'):
                    self.ej3_a_entry.delete(0, tk.END)
                if hasattr(self, 'ej3_b_entry'):
                    self.ej3_b_entry.delete(0, tk.END)
                    
            elif ejercicio_num == 4:
                if hasattr(self, 'ej4_func_entry'):
                    self.ej4_func_entry.delete(0, tk.END)
                if hasattr(self, 'ej4_xmin_entry'):
                    self.ej4_xmin_entry.delete(0, tk.END)
                if hasattr(self, 'ej4_xmax_entry'):
                    self.ej4_xmax_entry.delete(0, tk.END)
                if hasattr(self, 'ej4_ymin_entry'):
                    self.ej4_ymin_entry.delete(0, tk.END)
                if hasattr(self, 'ej4_ymax_entry'):
                    self.ej4_ymax_entry.delete(0, tk.END)
                    
            elif ejercicio_num == 5:
                if hasattr(self, 'ej5_func_entry'):
                    self.ej5_func_entry.delete(0, tk.END)
                if hasattr(self, 'ej5_t0_entry'):
                    self.ej5_t0_entry.delete(0, tk.END)
                if hasattr(self, 'ej5_y0_entry'):
                    self.ej5_y0_entry.delete(0, tk.END)
                if hasattr(self, 'ej5_tend_entry'):
                    self.ej5_tend_entry.delete(0, tk.END)
                if hasattr(self, 'ej5_h_entry'):
                    self.ej5_h_entry.delete(0, tk.END)
            
            messagebox.showinfo("Éxito", f"Campos limpiados para el ejercicio {ejercicio_num}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al limpiar campos: {str(e)}")
    
    def generar_gx_automatico(self):
        """Genera automáticamente la función g(x) para punto fijo."""
        try:
            funcion = self.ej1_func.get()
            if not funcion.strip():
                messagebox.showwarning("Advertencia", "Ingrese primero la función f(x)")
                return
            
            g_func = generar_funcion_punto_fijo(funcion)
            self.ej1_g.set(g_func)
            messagebox.showinfo("Éxito", f"g(x) generada automáticamente:\n{g_func}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar g(x): {str(e)}")
    
    def actualizar_instrucciones_ejercicio_1(self):
        """Actualiza las instrucciones del ejercicio 1 con los datos actuales."""
        try:
            funcion = self.ej1_func.get() or "exp(x) - 3*x**2"
            x0 = float(self.ej1_x0.get() or "0.5")
            
            # Usar intervalo por defecto [0,1] o intentar extraer de la función
            intervalo = [0, 1]
            
            instrucciones = generar_instrucciones_ejercicio_1(funcion, intervalo, x0)
            
            self.ej1_inst_text.config(state=tk.NORMAL)
            self.ej1_inst_text.delete(1.0, tk.END)
            self.ej1_inst_text.insert(1.0, instrucciones)
            self.ej1_inst_text.config(state=tk.DISABLED)
            
        except Exception as e:
            # Si hay error, mantener instrucciones por defecto
            pass
    
    def create_explicacion_general(self, notebook):
        """Crea la pestaña de explicación general del ejercicio 1."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📚 Explicación General")
        
        # Texto explicativo
        texto = """🎯 ¿QUÉ VAMOS A HACER?

En este ejercicio necesitamos encontrar la raíz de una función f(x) = 0.

🔍 PASO 1: VERIFICAR QUE EXISTE UNA RAÍZ
• Usamos el Teorema de Bolzano
• Evaluamos f(x) en los extremos del intervalo
• Si hay cambio de signo, existe una raíz

🚀 PASO 2: MÉTODO DE NEWTON-RAPHSON (PARTE A)
• Usa la derivada de la función
• Converge muy rápido (orden 2)
• Fórmula: x_{n+1} = x_n - f(x_n)/f'(x_n)

🔧 PASO 3: MÉTODO DE PUNTO FIJO + AITKEN (PARTE B)
• Despejamos x de la ecuación f(x) = 0
• Usamos aceleración de Aitken para converger más rápido
• Más estable que Newton-Raphson

📊 PASO 4: COMPARAR AMBOS MÉTODOS
• Ver cuál converge más rápido
• Verificar que ambos dan el mismo resultado
• Analizar la precisión de cada método

✅ RESULTADO FINAL
• La raíz aproximada con 6 decimales
• Verificación: f(raíz) ≈ 0"""
        
        text_widget = tk.Text(frame, height=20, wrap=tk.WORD, font=("Arial", 11))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, texto)
        text_widget.config(state=tk.DISABLED)
    
    def create_explicacion_newton(self, notebook):
        """Crea la pestaña de explicación del método de Newton-Raphson."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🚀 Newton-Raphson")
        
        # Texto explicativo
        texto = """🚀 MÉTODO DE NEWTON-RAPHSON

¿QUÉ ES?
Es un método iterativo que usa la derivada para encontrar raíces.

¿CÓMO FUNCIONA?
1. Empezamos con un valor inicial x₀
2. En cada paso, usamos la fórmula:
   x_{n+1} = x_n - f(x_n)/f'(x_n)
3. Repetimos hasta que converja

¿POR QUÉ FUNCIONA?
• La derivada f'(x) nos da la pendiente de la tangente
• Movemos x en la dirección donde f(x) se acerca a 0
• Es como "seguir la pendiente hacia abajo"

EJEMPLO CON f(x) = e^x - 3x²:
• f(x) = e^x - 3x²
• f'(x) = e^x - 6x
• x₀ = 0.5

PASO 1:
• f(0.5) = e^0.5 - 3(0.5)² = 1.6487 - 0.75 = 0.8987
• f'(0.5) = e^0.5 - 6(0.5) = 1.6487 - 3 = -1.3513
• x₁ = 0.5 - 0.8987/(-1.3513) = 0.5 + 0.6651 = 1.1651

PASO 2:
• f(1.1651) = e^1.1651 - 3(1.1651)² = 3.2064 - 4.0723 = -0.8659
• f'(1.1651) = e^1.1651 - 6(1.1651) = 3.2064 - 6.9906 = -3.7842
• x₂ = 1.1651 - (-0.8659)/(-3.7842) = 1.1651 - 0.2288 = 0.9363

Y así sucesivamente...

VENTAJAS:
✅ Converge muy rápido (orden 2)
✅ Muy preciso
✅ Fácil de implementar

DESVENTAJAS:
❌ Necesita la derivada
❌ Puede divergir si x₀ está mal elegido
❌ Sensible a la condición inicial"""
        
        text_widget = tk.Text(frame, height=20, wrap=tk.WORD, font=("Arial", 11))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, texto)
        text_widget.config(state=tk.DISABLED)
    
    def create_explicacion_punto_fijo(self, notebook):
        """Crea la pestaña de explicación del método de Punto Fijo + Aitken."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🔧 Punto Fijo + Aitken")
        
        # Texto explicativo
        texto = """🔧 MÉTODO DE PUNTO FIJO + ACELERACIÓN DE AITKEN

¿QUÉ ES?
Transformamos f(x) = 0 en x = g(x) y usamos Aitken para acelerar la convergencia.

¿CÓMO FUNCIONA?
1. Despejamos x de f(x) = 0 → x = g(x)
2. Iteramos: x_{n+1} = g(x_n)
3. Usamos Aitken para acelerar: x̂_n = x_n - (x_{n+1} - x_n)²/(x_{n+2} - 2x_{n+1} + x_n)

EJEMPLO CON f(x) = e^x - 3x²:
• f(x) = e^x - 3x² = 0
• Despejando: e^x = 3x² → x = √(e^x/3)
• g(x) = √(e^x/3)
• x₀ = 0.5

PASO 1:
• x₁ = g(0.5) = √(e^0.5/3) = √(1.6487/3) = √0.5496 = 0.7413

PASO 2:
• x₂ = g(0.7413) = √(e^0.7413/3) = √(2.0996/3) = √0.6999 = 0.8366

PASO 3:
• x₃ = g(0.8366) = √(e^0.8366/3) = √(2.3089/3) = √0.7696 = 0.8773

ACELERACIÓN DE AITKEN:
• x̂₀ = x₀ - (x₁ - x₀)²/(x₂ - 2x₁ + x₀)
• x̂₀ = 0.5 - (0.7413 - 0.5)²/(0.8366 - 2(0.7413) + 0.5)
• x̂₀ = 0.5 - (0.2413)²/(0.8366 - 1.4826 + 0.5)
• x̂₀ = 0.5 - 0.0582/(-0.1460) = 0.5 + 0.3986 = 0.8986

VENTAJAS:
✅ No necesita derivada
✅ Más estable que Newton-Raphson
✅ Aitken acelera la convergencia
✅ Funciona bien con funciones complicadas

DESVENTAJAS:
❌ Converge más lento que Newton-Raphson
❌ Necesita encontrar una buena g(x)
❌ Puede no converger si g'(x) > 1

¿POR QUÉ AITKEN?
• El método de punto fijo simple puede ser lento
• Aitken "predice" hacia dónde va a converger
• Acelera la convergencia sin cambiar el método base"""
        
        text_widget = tk.Text(frame, height=20, wrap=tk.WORD, font=("Arial", 11))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, texto)
        text_widget.config(state=tk.DISABLED)
    
    def create_instrucciones_hoja(self, notebook):
        """Crea la pestaña con las instrucciones detalladas para la hoja."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📋 Instrucciones para la Hoja")
        
        self.ej1_inst_text = tk.Text(frame, height=20, wrap=tk.WORD, font=("Courier", 10))
        self.ej1_inst_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Actualizar instrucciones iniciales
        self.actualizar_instrucciones_ejercicio_1()

# ============================================================================
# MAIN
# ============================================================================

def main():
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use('clam')
    except Exception:
        pass
    
    app = SimuladorParcialUnificado(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# raiz cuadrada de e a la x dividido en 3: sqrt(exp(x)/3)