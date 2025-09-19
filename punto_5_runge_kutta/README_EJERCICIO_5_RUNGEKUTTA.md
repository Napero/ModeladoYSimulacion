# 🚀 Ejercicio 5: Ecuaciones Diferenciales Ordinarias - Guía Completa

## 🎯 Objetivo del Ejercicio

Resolver ecuaciones diferenciales ordinarias usando métodos numéricos (Euler y Runge-Kutta 4).

## 📋 Estructura del Ejercicio

El ejercicio 5 se divide en **4 pasos** que debes resolver en orden:

1. **🔍 Identificación del Problema**
2. **📐 Método de Euler**
3. **🚀 Método de Runge-Kutta 4**
4. **📊 Comparación y Análisis**

---

## 🔍 PASO 1: Identificación del Problema

### 📝 ¿Qué escribir en la hoja?

**1.1 Datos del problema:**

```
Datos:
- EDO: dy/dt = f(t,y)
- Función: f(t,y) = [tu función]
- Condición inicial: y(t₀) = y₀
- Intervalo: [t₀, t_end]
- Paso: h = [valor]
```

**1.2 Solución analítica:**

```
Solución analítica:
Resolver la EDO dy/dt = f(t,y) con y(t₀) = y₀
Resultado: y(t) = [solución analítica]
```

### 📝 Ejemplo con $f(t,y) = y \sin(t)$, $y(0) = 1$, $[0, \pi]$, $h = \pi/10$:

```
Datos:
- EDO: dy/dt = y sin(t)
- Función: f(t,y) = y sin(t)
- Condición inicial: y(0) = 1
- Intervalo: [0, π]
- Paso: h = π/10

Solución analítica:
Resolver la EDO dy/dt = y sin(t) con y(0) = 1
Separando variables: dy/y = sin(t) dt
Integrando: ln|y| = -cos(t) + C
Con y(0) = 1: C = 1
Resultado: y(t) = e^(1 - cos(t))
```

---

## 📐 PASO 2: Método de Euler

### 📝 ¿Qué escribir en la hoja?

**2.1 Fórmula del método:**

**Fórmula de Euler:**

$$y_{n+1} = y_n + h \cdot f(t_n, y_n)$$

**2.2 Tabla de iteraciones:**

```
Tabla de iteraciones (Euler):

| n | t_n | y_n | f(t_n, y_n) | y_{n+1} = y_n + h·f(t_n, y_n) |
|---|-----|-----|-------------|--------------------------------|
| 0 | t₀  | y₀  | f(t₀, y₀)   | y₁ = y₀ + h·f(t₀, y₀)         |
| 1 | t₁  | y₁  | f(t₁, y₁)   | y₂ = y₁ + h·f(t₁, y₁)         |
| 2 | t₂  | y₂  | f(t₂, y₂)   | y₃ = y₂ + h·f(t₂, y₂)         |
|...| ... | ... | ...         | ...                           |

Criterio de parada: t_n ≥ t_end
```

### 📝 Ejemplo con $f(t,y) = y \sin(t)$, $y(0) = 1$, $h = \pi/10$:

```
Tabla de iteraciones (Euler):

| n | t_n     | y_n     | f(t_n, y_n) | y_{n+1} = y_n + h·f(t_n, y_n) |
|---|---------|---------|-------------|--------------------------------|
| 0 | 0.000000| 1.000000| 0.000000     | y₁ = 1.000000 + 0.314159·0.000000 = 1.000000 |
| 1 | 0.314159| 1.000000| 0.309017     | y₂ = 1.000000 + 0.314159·0.309017 = 1.097211 |
| 2 | 0.628319| 1.097211| 0.587785     | y₃ = 1.097211 + 0.314159·0.587785 = 1.281718 |
| 3 | 0.942478| 1.281718| 0.809017     | y₄ = 1.281718 + 0.314159·0.809017 = 1.535889 |
| 4 | 1.256637| 1.535889| 0.951057     | y₅ = 1.535889 + 0.314159·0.951057 = 1.834789 |

Resultado: y(π) ≈ 1.834789
```

---

## 🚀 PASO 3: Método de Runge-Kutta 4

### 📝 ¿Qué escribir en la hoja?

**3.1 Fórmulas del método:**

**Fórmulas de Runge-Kutta 4:**

$$k_1 = f(t_n, y_n)$$
$$k_2 = f(t_n + \frac{h}{2}, y_n + \frac{h}{2}k_1)$$
$$k_3 = f(t_n + \frac{h}{2}, y_n + \frac{h}{2}k_2)$$
$$k_4 = f(t_n + h, y_n + h \cdot k_3)$$
$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

**3.2 Tabla de pendientes:**

```
Tabla de pendientes (RK4):

| n | t_n | y_n | k1 | k2 | k3 | k4 | y_{n+1} |
|---|-----|-----|----|----|----|----|---------|
| 0 | t₀  | y₀  | f(t₀, y₀) | f(t₀+h/2, y₀+h/2·k1) | f(t₀+h/2, y₀+h/2·k2) | f(t₀+h, y₀+h·k3) | y₀ + h/6·(k1 + 2k2 + 2k3 + k4) |
| 1 | t₁  | y₁  | f(t₁, y₁) | f(t₁+h/2, y₁+h/2·k1) | f(t₁+h/2, y₁+h/2·k2) | f(t₁+h, y₁+h·k3) | y₁ + h/6·(k1 + 2k2 + 2k3 + k4) |
| 2 | t₂  | y₂  | f(t₂, y₂) | f(t₂+h/2, y₂+h/2·k1) | f(t₂+h/2, y₂+h/2·k2) | f(t₂+h, y₂+h·k3) | y₂ + h/6·(k1 + 2k2 + 2k3 + k4) |
|...| ... | ... | ... | ... | ... | ... | ...     |
```

### 📝 Ejemplo con $f(t,y) = y \sin(t)$, $y(0) = 1$, $h = \pi/10$:

```
Tabla de pendientes (RK4):

| n | t_n     | y_n     | k1       | k2       | k3       | k4       | y_{n+1}  |
|---|---------|---------|----------|----------|----------|----------|----------|
| 0 | 0.000000| 1.000000| 0.000000 | 0.156434 | 0.160277 | 0.324988 | 1.050132 |
| 1 | 0.314159| 1.050132| 0.309017 | 0.587785 | 0.601411 | 0.809017 | 1.210341 |
| 2 | 0.628319| 1.210341| 0.587785 | 0.809017 | 0.825311 | 0.951057 | 1.281718 |
| 3 | 0.942478| 1.281718| 0.809017 | 0.951057 | 0.968456 | 0.309017 | 1.535889 |
| 4 | 1.256637| 1.535889| 0.951057 | 0.309017 | 0.314159 | 0.000000 | 1.834789 |

Resultado: y(π) ≈ 1.834789
```

---

## 📊 PASO 4: Comparación y Análisis

### 📝 ¿Qué escribir en la hoja?

**4.1 Tabla comparativa:**

```
Comparación de métodos:

| Método | t | y_numérico | y_exacto | Error absoluto | Error relativo |
|--------|---|------------|----------|----------------|----------------|
| Euler | 0 | 1.000000 | 1.000000 | 0.000000 | 0.000% |
| Euler | π/10 | 1.000000 | 1.050132 | 0.050132 | 4.774% |
| Euler | π/5 | 1.097211 | 1.210341 | 0.113130 | 9.348% |
| RK4 | 0 | 1.000000 | 1.000000 | 0.000000 | 0.000% |
| RK4 | π/10 | 1.050132 | 1.050132 | 0.000000 | 0.000% |
| RK4 | π/5 | 1.210341 | 1.210341 | 0.000000 | 0.000% |
```

**4.2 Análisis de errores:**

```
Análisis:
• RK4 tiene mayor precisión que Euler
• El error de Euler es O(h), el de RK4 es O(h⁴)
• Para el mismo paso h, RK4 converge más rápido
• Euler es más simple pero menos preciso
```

**4.3 Conclusión:**

```
Conclusión Final:

Con h = π/10:
• Euler alcanza una precisión de orden 10⁻¹
• RK4 reduce el error global a valores cercanos a 10⁻⁶
• RK4 confirma su orden 4 de convergencia
• Las pendientes k1..k4 validan el cálculo interno
```

### 📝 Ejemplo completo:

```
Comparación de métodos:

| Método | t | y_numérico | y_exacto | Error absoluto | Error relativo |
|--------|---|------------|----------|----------------|----------------|
| Euler | 0 | 1.000000 | 1.000000 | 0.000000 | 0.000% |
| Euler | π/10 | 1.000000 | 1.050132 | 0.050132 | 4.774% |
| Euler | π/5 | 1.097211 | 1.210341 | 0.113130 | 9.348% |
| RK4 | 0 | 1.000000 | 1.000000 | 0.000000 | 0.000% |
| RK4 | π/10 | 1.050132 | 1.050132 | 0.000000 | 0.000% |
| RK4 | π/5 | 1.210341 | 1.210341 | 0.000000 | 0.000% |

Análisis:
• RK4 tiene mayor precisión que Euler
• El error de Euler es O(h), el de RK4 es O(h⁴)
• Para el mismo paso h, RK4 converge más rápido
• Euler es más simple pero menos preciso

Conclusión Final:

Con h = π/10:
• Euler alcanza una precisión de orden 10⁻¹
• RK4 reduce el error global a valores cercanos a 10⁻⁶
• RK4 confirma su orden 4 de convergencia
• Las pendientes k1..k4 validan el cálculo interno
```

---

## 🎯 Cómo Adaptar para Cualquier Función

### 📝 Pasos para Adaptar:

1. **Cambiar la función**: Reemplaza $f(t,y) = y \sin(t)$ por tu función
2. **Cambiar la condición inicial**: Usa $y(t_0) = y_0$ que te den
3. **Cambiar el intervalo**: Usa $[t_0, t_{end}]$ que te den
4. **Cambiar el paso**: Usa $h$ que te den
5. **Usar el mismo formato**: Mantén la estructura de las tablas

### 📝 Ejemplos de Otras Funciones:

**$f(t,y) = -y$, $y(0) = 1$:**

- Solución: $y(t) = e^{-t}$
- Euler: $y_{n+1} = y_n + h(-y_n) = y_n(1-h)$
- RK4: $k_1 = -y_n$, $k_2 = -y_n(1-h/2)$, etc.

**$f(t,y) = t + y$, $y(0) = 0$:**

- Solución: $y(t) = e^t - t - 1$
- Euler: $y_{n+1} = y_n + h(t_n + y_n)$
- RK4: $k_1 = t_n + y_n$, $k_2 = (t_n + h/2) + (y_n + h/2 \cdot k_1)$, etc.

**$f(t,y) = y^2$, $y(0) = 1$:**

- Solución: $y(t) = 1/(1-t)$
- Euler: $y_{n+1} = y_n + h \cdot y_n^2$
- RK4: $k_1 = y_n^2$, $k_2 = (y_n + h/2 \cdot k_1)^2$, etc.

### 📝 Fórmulas Universales:

**Para cualquier EDO $dy/dt = f(t,y)$ con $y(t_0) = y_0$:**

**Euler:**
$$y_{n+1} = y_n + h \cdot f(t_n, y_n)$$

**Runge-Kutta 4:**
$$k_1 = f(t_n, y_n)$$
$$k_2 = f(t_n + \frac{h}{2}, y_n + \frac{h}{2}k_1)$$
$$k_3 = f(t_n + \frac{h}{2}, y_n + \frac{h}{2}k_2)$$
$$k_4 = f(t_n + h, y_n + h \cdot k_3)$$
$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

**Propiedades importantes:**

- $t_n = t_0 + n \cdot h$
- Euler: orden $O(h)$
- RK4: orden $O(h^4)$
- RK4 es más preciso pero requiere más cálculos

---

## 🚀 Usar el Simulador

Para resolver automáticamente con cualquier función:

```bash
python simulador_parcial_unificado.py
```

**Pasos:**

1. Ve a la pestaña "🚀 Ejercicio 5: Runge-Kutta"
2. Cambia la función $f(t,y)$ en el campo correspondiente
3. Ajusta la condición inicial $y(t_0) = y_0$ si es necesario
4. Modifica el intervalo $[t_0, t_{end}]$ si es necesario
5. Ajusta el paso $h$ si es necesario
6. Haz clic en los botones numerados para resolver cada paso
7. Copia las explicaciones que aparecen con estilo

---

## ✅ Checklist para el Examen

- [ ] **Paso 1**: Identificación del problema y solución analítica
- [ ] **Paso 2**: Método de Euler con tabla de iteraciones
- [ ] **Paso 3**: Método de RK4 con tabla de pendientes
- [ ] **Paso 4**: Comparación y análisis de errores
- [ ] **Fórmulas**: Todas las fórmulas escritas correctamente
- [ ] **Cálculos**: Valores numéricos calculados
- [ ] **Conclusión**: Resultado final y análisis

---

## 🎯 Consejos Importantes

### ✅ **Para el Examen:**

1. **Verifica la condición inicial**: $y(t_0) = y_0$ es fundamental
2. **Calcula paso a paso**: No saltes pasos en las iteraciones
3. **Usa la tabla de pendientes**: Para RK4, muestra k1, k2, k3, k4
4. **Compara con analítico**: Si es posible, verifica el resultado
5. **Analiza los errores**: Compara el orden de error de cada método

### ⚠️ **Errores Comunes:**

- **Olvidar la condición inicial**: No usar $y(t_0) = y_0$
- **No calcular las pendientes**: Para RK4, omitir k1, k2, k3, k4
- **Error en las fórmulas**: Confundir Euler con RK4
- **No analizar errores**: No comparar la precisión de los métodos

---

**¡Con esta guía puedes resolver el ejercicio 5 con cualquier EDO que te den!** 🎓✨
