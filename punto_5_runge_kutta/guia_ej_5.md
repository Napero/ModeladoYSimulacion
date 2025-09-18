# Cómo usar tu script (simulador_runge_kutta_pro.py) para resolver el Ejercicio 5

Variable del script: usa t en lugar de x. Simplemente identifica x ≡ t.

---

## 1. Preparar el problema

Campos (fila superior):

| Campo GUI | Qué poner para este ejercicio |
|-----------|-------------------------------|
| f(t,y)=   | y*sin(t) |
| t0        | 0 |
| y0        | 1 |
| t_end     | pi |
| h         | pi/10 |
| Método    | (primero Euler, luego RK4) |
| Check "Mostrar Pendientes RK4" | Actívalo SOLO para RK4 (inciso b) |

Escribe pi (sin comillas). Sympy lo reconoce.

---

## 2. Obtener la solución analítica (antes de cálculos numéricos)

1. Rellená los campos como arriba (cualquier método seleccionado da igual).
2. Botón: Calcular Solución Analítica.  
   Aparecerá en el panel “Solución Analítica (LaTeX)” algo como:  
   y(t) = C₁*exp(cos(t)) → con la condición inicial se simplifica a y(t)=exp(1 - cos(t)).
3. Ahora la tabla numérica mostrará también la columna y_exact y Error cuando hagas Calcular.

---

## 3. Inciso (a) — Método Euler (precisión ~1e-1)

1. En “Método” seleccioná Euler.
2. Verificá h = pi/10 (≈ 0.314159…).
3. Botón: Calcular.
4. Mirá la pestaña “Tabla Normal” (Notebook):
   - Columnas: n, t, y_num, y_exact, Error.
   - Filas que te interesan para justificar:
     - n=0: t=0.000, y_num=1.000000, y_exact=1.000000, Error=0
     - n=1: t≈0.314, y_num≈1.000000 (porque sin(0)=0 en el primer paso), y_exact≈1.050132, Error≈5.01e-02
     - n=2: t≈0.628, y_num≈1.097211, y_exact≈1.210341, Error≈1.13e-01
5. El gráfico muestra la curva exacta (línea negra discontinua) y los puntos de Euler (línea de color).
6. Guarda (anotá) el error máximo (columna Error). Compara con la tolerancia 10^-1 pedida: está acorde al orden O(h).

Fórmula usada internamente (verificación manual):  
y_{n+1} = y_n + h * y_n * sin(t_n)

---

## 4. Inciso (b) — Método RK4 (error ~1e-6 o menor)

1. Cambiá “Método” a RK4.
2. Activá el check “Mostrar Pendientes RK4”.
3. Botón: Calcular.
4. Pestañas a revisar:
   - “Tabla Normal”: ahora y_num casi coincide con y_exact (errores muy pequeños).
   - “Pendientes RK4”: columnas n, t_n, y_n, k1, k2, k3, k4, y_{n+1}.  
     Primer paso esperado (aprox):
     - k1 = 0
     - k2 ≈ 0.156434
     - k3 ≈ 0.160277
     - k4 ≈ 0.324988
     - y_1 ≈ 1.050132 (coincide con exacta a muchas cifras)
5. Segundo paso (n=1) mostrará otra serie de k1..k4; copiá esos valores si el enunciado te pide la tabla de pendientes.
6. Observá el error final en t=pi (fila n=10). Esperá algo cercano a cero (≈1e-6 o mejor).

Fórmulas que justifica la tabla:
k1 = f(t_n, y_n)  
k2 = f(t_n + h/2, y_n + (h/2)k1)  
k3 = f(t_n + h/2, y_n + (h/2)k2)  
k4 = f(t_n + h,   y_n + h k3)  
y_{n+1} = y_n + (h/6)(k1 + 2k2 + 2k3 + k4)

---

## 5. Comparar métodos en una sola vista

1. (Opcional) Botón: Comparar Métodos → grafica todas las trayectorias para el mismo h.
2. Botón: Tabla Comparativa → pestaña “Tabla Comparativa” se llena con columnas para cada método y su error en cada nodo (si la solución exacta ya fue calculada).

---

## 6. Datos clave que debés extraer para el informe

Para (a) Euler:
- Paso h = pi/10
- Primeras dos iteraciones (n=0→1 y n=1→2) con y_num, y_exact, error.
- Error máximo (por ejemplo en n=2 ya se ve ~1.13e-01).
- Gráfico Euler vs exacta (captura).

Para (b) RK4:
- Tabla de pendientes (primeras 1–2 filas) k1..k4.
- Errores (mucho menores, típicamente <1e-6).
- Gráfico RK4 vs exacta.
- Comparación final: error Euler ~1e-1 vs RK4 ~1e-6 (misma h → mejor orden).

---

## 7. Checklist rápido para no olvidar

| Paso | Acción |
|------|--------|
| 1 | Ingresar f(t,y)= y*sin(t) |
| 2 | t0=0, y0=1, t_end=pi, h=pi/10 |
| 3 | Calcular Solución Analítica |
| 4 | Método=Euler → Calcular → Guardar primeras 2 filas y error |
| 5 | Método=RK4 + check pendientes → Calcular |
| 6 | Revisar pestaña Pendientes RK4 (k1..k4) |
| 7 | Tabla Comparativa (opcional) |
| 8 | Graficar / Capturar gráficos |
| 9 | Redactar conclusiones (error orden O(h) vs O(h^4)) |

---

## 8. Frase de conclusión reutilizable

Con h = pi/10, Euler alcanza una precisión de orden 10^-1, coherente con su orden 1. Con el mismo paso, RK4 reduce el error global a valores cercanos a 10^-6, confirmando su orden 4. Las pendientes k1..k4 registradas en la tabla validan el cálculo interno de cada iteración.

Listo: con estos pasos reunís todo lo que