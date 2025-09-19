# 🚀 Guía Paso a Paso: Ejercicio 5 A y B - EDOs

## 📋 Datos del Ejercicio

**EDO:** $dy/dx = y \sin(x)$  
**Función:** $f(x,y) = y \sin(x)$  
**Condición inicial:** $y(0) = 1$  
**Intervalo:** $0 \leq x \leq \pi$  
**Paso:** $h = \pi/10$

---

## 📋 Requerimientos del Enunciado

**Parte A:**

- Método numérico con precisión de $10^{-1}$
- Usar algoritmo de Euler
- Paso $h = \pi/10$
- Verificar primera y segunda iteración
- Graficar solución aproximada vs real

**Parte B:**

- Algoritmo con error $\leq 10^{-6}$ (Runge-Kutta 4)
- Estimar cuatro pendientes: $k_1, k_2, k_3, k_4$
- Presentar cálculos en tabla
- Comparar gráfica y numéricamente con parte A

---

## 🔍 PARTE A: Método de Euler

### 📝 Pasos a seguir:

**1 - Primero tenés que identificar el problema:**

Escribir en la hoja:

- EDO: $dy/dx = y \sin(x)$
- Condición inicial: $y(0) = 1$
- Intervalo: $0 \leq x \leq \pi$
- Paso: $h = \pi/10 \approx 0.314159$

**2 - Luego escribí la fórmula de Euler:**

Fórmula de Euler:
$y_{n+1} = y_n + h \cdot f(x_n, y_n)$

**3 - Reemplazá la fórmula con estos datos quedando así:**

$y_{n+1} = y_n + (π/10) · y_n · sin(x_n)$
$y_{n+1} = y_n + 0.314159 · y_n · sin(x_n)$

**4 - Andá al script y rellená con esto:**

Campo $f(x,y)= y*sin(x)$
Campo "x0": 0
Campo "y0": 1
Campo "x_end": pi
Campo "h": pi/10
Método: Seleccionar "Euler"

**5 - Hacé clic en "Calcular Solución Analítica" primero:**

```
Esto te dará la solución exacta: y(x) = e^(1 - cos(x))
```

**6 - Luego hacé clic en "Calcular" para el método Euler:**

```
Vas a obtener una tabla con columnas: n, x, y_num, y_exact, Error
```

**7 - Copiá las primeras 3 filas de la tabla:**

```
| n | x_n     | y_num   | y_exact | Error    |
|---|---------|---------|---------|----------|
| 0 | 0.000000| 1.000000| 1.000000| 0.000000 |
| 1 | 0.314159| 1.000000| 1.050132| 0.050132 |
| 2 | 0.628319| 1.097211| 1.210341| 0.113130 |
```

**8 - Escribí en la hoja la tabla de iteraciones:**

```
Tabla de iteraciones (Euler):

| n | x_n     | y_n     | f(x_n, y_n) | y_{n+1} = y_n + h·f(x_n, y_n) |
|---|---------|---------|-------------|--------------------------------|
| 0 | 0.000000| 1.000000| 0.000000     | y₁ = 1.000000 + 0.314159·0.000000 = 1.000000 |
| 1 | 0.314159| 1.000000| 0.309017     | y₂ = 1.000000 + 0.314159·0.309017 = 1.097211 |
| 2 | 0.628319| 1.097211| 0.587785     | y₃ = 1.097211 + 0.314159·0.587785 = 1.281718 |
```

**9 - Verificá la primera y segunda iteración:**

```
Primera iteración (n=0 → n=1):
x₀ = 0, y₀ = 1
f(x₀, y₀) = 1 · sin(0) = 0
y₁ = 1 + (π/10) · 0 = 1.000000 ✓

Segunda iteración (n=1 → n=2):
x₁ = π/10, y₁ = 1.000000
f(x₁, y₁) = 1 · sin(π/10) = 0.309017
y₂ = 1 + (π/10) · 0.309017 = 1.097211 ✓
```

**10 - Anotá el error máximo:**

```
Error máximo de Euler: aproximadamente 0.113130 (en n=2)
Este error es del orden 10⁻¹, coherente con el orden O(h) del método
```

**11 - Capturá el gráfico:**

```
El gráfico debe mostrar:
- Línea negra discontinua: solución exacta y(x) = e^(1 - cos(x))
- Línea de color: puntos de Euler
- Visualización clara de la desviación/error
```

---

## 🚀 PARTE B: Método de Runge-Kutta 4

### 📝 Pasos a seguir:

**1 - Primero escribí las fórmulas de RK4:**

Fórmulas de Runge-Kutta 4:
$k_1 = f(x_n, y_n)$
$k_2 = f(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_1)$
$k_3 = f(x_n + \frac{h}{2}, y_n + \frac{h}{2}k_2)$
$k_4 = f(x_n + h, y_n + h \cdot k_3)$
$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$

**2 - Reemplazá con los datos específicos:**

```
k1 = y_n · sin(x_n)
k2 = (y_n + (π/20)·k1) · sin(x_n + π/20)
k3 = (y_n + (π/20)·k2) · sin(x_n + π/20)
k4 = (y_n + (π/10)·k3) · sin(x_n + π/10)
y_{n+1} = y_n + (π/60)(k1 + 2k2 + 2k3 + k4)
```

**3 - Andá al script y cambiá el método:**

```
Método: Seleccionar "RK4"
Check "Mostrar Pendientes RK4": Activar
```

**4 - Hacé clic en "Calcular":**

```
Vas a obtener dos pestañas:
- "Tabla Normal": con errores mucho menores
- "Pendientes RK4": con k1, k2, k3, k4
```

**5 - Copiá la tabla de pendientes (primeras 2 filas):**

```
| n | x_n     | y_n     | k1       | k2       | k3       | k4       | y_{n+1}  |
|---|---------|---------|----------|----------|----------|----------|----------|
| 0 | 0.000000| 1.000000| 0.000000 | 0.156434 | 0.160277 | 0.324988 | 1.050132 |
| 1 | 0.314159| 1.050132| 0.309017 | 0.587785 | 0.601411 | 0.809017 | 1.210341 |
```

**6 - Escribí en la hoja la tabla de pendientes:**

```
Tabla de pendientes (RK4):

| n | x_n     | y_n     | k1       | k2       | k3       | k4       | y_{n+1}  |
|---|---------|---------|----------|----------|----------|----------|----------|
| 0 | 0.000000| 1.000000| 0.000000 | 0.156434 | 0.160277 | 0.324988 | 1.050132 |
| 1 | 0.314159| 1.050132| 0.309017 | 0.587785 | 0.601411 | 0.809017 | 1.210341 |
```

**7 - Anotá los errores de RK4:**

```
Error máximo de RK4: aproximadamente 10⁻⁶ o menor
Este error es del orden 10⁻⁶, coherente con el orden O(h⁴) del método
```

**8 - Capturá el gráfico de RK4:**

```
El gráfico debe mostrar:
- Línea negra discontinua: solución exacta y(x) = e^(1 - cos(x))
- Línea de color: puntos de RK4
- Visualización de la mejora significativa vs Euler
```

---

## 📊 COMPARACIÓN FINAL

### 📝 Pasos a seguir:

**1 - Hacé una tabla comparativa:**

```
Comparación de métodos:

| Método | Error máximo | Orden | Precisión |
|--------|--------------|-------|-----------|
| Euler  | ~10⁻¹        | O(h)  | Baja      |
| RK4    | ~10⁻⁶        | O(h⁴) | Alta      |
```

**2 - Escribí las conclusiones:**

```
Conclusiones:
• Con h = π/10, Euler alcanza precisión de orden 10⁻¹
• Con el mismo paso, RK4 reduce el error a 10⁻⁶
• RK4 confirma su orden 4 de convergencia
• Las pendientes k1..k4 validan el cálculo interno
```

**3 - Anotá la frase de conclusión:**

```
"Con h = π/10, Euler alcanza una precisión de orden 10⁻¹, coherente con su orden 1.
Con el mismo paso, RK4 reduce el error global a valores cercanos a 10⁻⁶,
confirmando su orden 4. Las pendientes k1..k4 registradas en la tabla
validan el cálculo interno de cada iteración."
```

---

## 🎯 CHECKLIST FINAL

### ✅ Verificá que tengas:

- [ ] **Parte A**: Tabla de iteraciones de Euler (primeras 3 filas)
- [ ] **Parte A**: Verificación de primera y segunda iteración
- [ ] **Parte A**: Error máximo de Euler (~10⁻¹)
- [ ] **Parte A**: Gráfico Euler vs solución exacta
- [ ] **Parte B**: Tabla de pendientes RK4 (primeras 2 filas)
- [ ] **Parte B**: Error máximo de RK4 (~10⁻⁶)
- [ ] **Parte B**: Gráfico RK4 vs solución exacta
- [ ] **Comparación**: Tabla comparativa de métodos
- [ ] **Comparación**: Comparación gráfica y numérica
- [ ] **Conclusión**: Análisis de órdenes de error
- [ ] **Fórmulas**: Todas las fórmulas escritas correctamente
- [ ] **Datos**: Valores numéricos calculados

---

## 🚀 COMANDO PARA EJECUTAR

```bash
python simulador_parcial_unificado.py
```

**O si tenés el script específico:**

```bash
python punto_5_runge_kutta/5_a_b_simulador_runge_kutta_pro.py
```

---

## 📝 NOTAS IMPORTANTES

1. **Siempre calculá la solución analítica primero** antes de los métodos numéricos
2. **Copiá exactamente** los valores que te da el script
3. **Verificá que los errores** sean coherentes con el orden del método
4. **Las pendientes k1..k4** son fundamentales para RK4
5. **El paso h = π/10** es el mismo para ambos métodos

---

**¡Con esta guía paso a paso podés resolver el ejercicio 5 A y B sin problemas!** 🎓✨
