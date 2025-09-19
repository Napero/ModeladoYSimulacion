# 📊 Ejercicio 3: Integración Numérica - Guía Completa

## 🎯 Objetivo del Ejercicio

Calcular integrales definidas usando métodos numéricos cuando la primitiva no es elemental.

## 📋 Estructura del Ejercicio

El ejercicio 3 se divide en **4 pasos** que debes resolver en orden:

1. **🔍 Identificación del Problema**
2. **📐 Método del Trapecio Compuesto**
3. **📊 Método de Simpson 1/3**
4. **📈 Comparación y Análisis**

---

## 🔍 PASO 1: Identificación del Problema

### 📝 ¿Qué escribir en la hoja?

**1.1 Datos del problema:**

```
Datos:
- Función: f(x) = [tu función]
- Intervalo: [a, b]
- Integral: I = ∫[a]^[b] f(x) dx
```

**1.2 Justificación del método numérico:**

```
Como la primitiva de f(x) = [tu función] no es elemental,
usamos métodos numéricos para aproximar la integral.
```

### 📝 Ejemplo con $f(x) = \sqrt{2} \cdot e^{x^2}$, $[0, 1]$:

```
Datos:
- Función: f(x) = √2 · e^(x²)
- Intervalo: [0, 1]
- Integral: I = ∫₀¹ √2 · e^(x²) dx

Como la primitiva de e^(x²) no es elemental,
usamos métodos numéricos para aproximar la integral.
```

---

## 📐 PASO 2: Método del Trapecio Compuesto

### 📝 ¿Qué escribir en la hoja?

**2.1 Fórmula del trapecio compuesto:**

**Fórmula del trapecio compuesto:**

$$T_n = h \left[ \frac{1}{2}f(a) + \sum_{i=1}^{n-1} f(a + ih) + \frac{1}{2}f(b) \right]$$

donde: $h = \frac{b-a}{n}$

**2.2 Cálculo con n = 4:**

```
Para n = 4:
h = (b-a)/4 = [valor]/4 = [resultado]

Puntos: x_i = a + i·h = [a] + i·[h]

| i | x_i | f(x_i) = [función] |
|---|-----|---------------------|
| 0 | [a] | f([a]) = [valor] |
| 1 | [a+h] | f([a+h]) = [valor] |
| 2 | [a+2h] | f([a+2h]) = [valor] |
| 3 | [a+3h] | f([a+3h]) = [valor] |
| 4 | [b] | f([b]) = [valor] |

T_4 = h/2 [f(a) + 2f(x₁) + 2f(x₂) + 2f(x₃) + f(b)]
T_4 = [h]/2 [f([a]) + 2f([a+h]) + 2f([a+2h]) + 2f([a+3h]) + f([b])]
T_4 = [calcular] = [resultado]
```

### 📝 Ejemplo con $f(x) = \sqrt{2} \cdot e^{x^2}$, $[0, 1]$:

```
Para n = 4:
h = (1-0)/4 = 1/4 = 0.25

Puntos: x_i = 0 + i·0.25

| i | x_i | f(x_i) = √2 · e^(x_i²) |
|---|-----|-------------------------|
| 0 | 0.00 | f(0.00) = √2 · e^0 = 1.414214 |
| 1 | 0.25 | f(0.25) = √2 · e^(0.0625) = 1.502631 |
| 2 | 0.50 | f(0.50) = √2 · e^(0.25) = 1.755055 |
| 3 | 0.75 | f(0.75) = √2 · e^(0.5625) = 2.319007 |
| 4 | 1.00 | f(1.00) = √2 · e^1 = 3.844231 |

T_4 = 0.25/2 [1.414214 + 2(1.502631) + 2(1.755055) + 2(2.319007) + 3.844231]
T_4 = 0.125 [1.414214 + 3.005262 + 3.510110 + 4.638014 + 3.844231]
T_4 = 0.125 [16.411831] = 2.051479
```

---

## 📊 PASO 3: Método de Simpson 1/3

### 📝 ¿Qué escribir en la hoja?

**3.1 Fórmula de Simpson 1/3:**

**Fórmula de Simpson 1/3:**

$$S_n = \frac{h}{3} \left[ f(a) + f(b) + 4\sum_{i \text{ impar}} f(a + ih) + 2\sum_{i \text{ par}} f(a + ih) \right]$$

donde: $h = \frac{b-a}{n}$ y $n$ debe ser **par**

**3.2 Cálculo con n = 4:**

```
Para n = 4 (par):
h = (b-a)/4 = [valor]/4 = [resultado]

S_4 = h/3 [f(a) + 4f(x₁) + 2f(x₂) + 4f(x₃) + f(b)]
S_4 = [h]/3 [f([a]) + 4f([a+h]) + 2f([a+2h]) + 4f([a+3h]) + f([b])]
S_4 = [calcular] = [resultado]
```

### 📝 Ejemplo con $f(x) = \sqrt{2} \cdot e^{x^2}$, $[0, 1]$:

```
Para n = 4 (par):
h = (1-0)/4 = 1/4 = 0.25

S_4 = 0.25/3 [f(0) + 4f(0.25) + 2f(0.50) + 4f(0.75) + f(1)]
S_4 = 0.25/3 [1.414214 + 4(1.502631) + 2(1.755055) + 4(2.319007) + 3.844231]
S_4 = 0.25/3 [1.414214 + 6.010524 + 3.510110 + 9.276028 + 3.844231]
S_4 = 0.25/3 [24.055107] = 2.004592
```

---

## 📈 PASO 4: Comparación y Análisis

### 📝 ¿Qué escribir en la hoja?

**4.1 Tabla comparativa:**

```
Comparación de métodos:

| Método | n | Resultado | Error estimado |
|--------|---|-----------|----------------|
| Trapecio | 4 | T_4 = [resultado] | O(h²) |
| Trapecio | 10 | T_10 = [resultado] | O(h²) |
| Simpson | 4 | S_4 = [resultado] | O(h⁴) |
```

**4.2 Análisis de errores:**

```
Análisis:
• Simpson es más preciso que Trapecio para el mismo n
• El error de Simpson es O(h⁴) vs O(h²) del Trapecio
• Al aumentar n, ambos métodos convergen al valor real
• Simpson requiere n par, Trapecio funciona con cualquier n
```

**4.3 Conclusión:**

```
Conclusión Final:

El método de Simpson 1/3 con n=4 proporciona la mejor aproximación:
I ≈ S_4 = [resultado]

Este resultado es válido por la continuidad de f(x) y el orden de error O(h⁴) del método.
```

### 📝 Ejemplo completo:

```
Comparación de métodos:

| Método | n | Resultado | Error estimado |
|--------|---|-----------|----------------|
| Trapecio | 4 | T_4 = 2.051479 | O(h²) |
| Trapecio | 10 | T_10 = 2.074898 | O(h²) |
| Simpson | 4 | S_4 = 2.004592 | O(h⁴) |

Análisis:
• Simpson es más preciso que Trapecio para el mismo n
• El error de Simpson es O(h⁴) vs O(h²) del Trapecio
• Al aumentar n, ambos métodos convergen al valor real
• Simpson requiere n par, Trapecio funciona con cualquier n

Conclusión Final:

El método de Simpson 1/3 con n=4 proporciona la mejor aproximación:
I ≈ S_4 = 2.004592

Este resultado es válido por la continuidad de f(x) y el orden de error O(h⁴) del método.
```

---

## 🎯 Cómo Adaptar para Cualquier Función

### 📝 Pasos para Adaptar:

1. **Cambiar la función**: Reemplaza $f(x) = \sqrt{2} \cdot e^{x^2}$ por tu función
2. **Cambiar el intervalo**: Usa el intervalo $[a, b]$ que te den
3. **Calcular los puntos**: Evalúa tu función en los puntos $x_i = a + ih$
4. **Usar el mismo formato**: Mantén la estructura de las tablas
5. **Aplicar las mismas fórmulas**: Los métodos son universales

### 📝 Ejemplos de Otras Funciones:

**$f(x) = x^2$, $[0, 2]$:**

- Trapecio: $T_4 = \frac{h}{2}[f(0) + 2f(0.5) + 2f(1) + 2f(1.5) + f(2)]$
- Simpson: $S_4 = \frac{h}{3}[f(0) + 4f(0.5) + 2f(1) + 4f(1.5) + f(2)]$

**$f(x) = \sin(x)$, $[0, \pi]$:**

- Trapecio: $T_4 = \frac{\pi}{8}[\sin(0) + 2\sin(\pi/4) + 2\sin(\pi/2) + 2\sin(3\pi/4) + \sin(\pi)]$
- Simpson: $S_4 = \frac{\pi}{12}[\sin(0) + 4\sin(\pi/4) + 2\sin(\pi/2) + 4\sin(3\pi/4) + \sin(\pi)]$

**$f(x) = e^{-x^2}$, $[0, 1]$:**

- Trapecio: $T_4 = \frac{1}{8}[e^0 + 2e^{-0.25} + 2e^{-1} + 2e^{-2.25} + e^{-1}]$
- Simpson: $S_4 = \frac{1}{12}[e^0 + 4e^{-0.25} + 2e^{-1} + 4e^{-2.25} + e^{-1}]$

### 📝 Fórmulas Universales:

**Para cualquier función $f(x)$ en $[a, b]$:**

**Trapecio compuesto:**
$$T_n = h \left[ \frac{1}{2}f(a) + \sum_{i=1}^{n-1} f(a + ih) + \frac{1}{2}f(b) \right]$$

**Simpson 1/3:**
$$S_n = \frac{h}{3} \left[ f(a) + f(b) + 4\sum_{i \text{ impar}} f(a + ih) + 2\sum_{i \text{ par}} f(a + ih) \right]$$

**Propiedades importantes:**

- $h = \frac{b-a}{n}$
- Trapecio: orden $O(h^2)$
- Simpson: orden $O(h^4)$, requiere $n$ par
- Ambos convergen al valor real cuando $n \to \infty$

---

## 🚀 Usar el Simulador

Para resolver automáticamente con cualquier función:

```bash
python simulador_parcial_unificado.py
```

**Pasos:**

1. Ve a la pestaña "📊 Ejercicio 3: Integrales"
2. Cambia la función $f(x)$ en el campo correspondiente
3. Ajusta el intervalo $[a, b]$ si es necesario
4. Haz clic en los botones numerados para resolver cada paso
5. Copia las explicaciones que aparecen con estilo

---

## ✅ Checklist para el Examen

- [ ] **Paso 1**: Identificación del problema y justificación
- [ ] **Paso 2**: Trapecio compuesto con tabla de valores
- [ ] **Paso 3**: Simpson 1/3 con tabla de valores
- [ ] **Paso 4**: Comparación y análisis de errores
- [ ] **Fórmulas**: Todas las fórmulas escritas correctamente
- [ ] **Cálculos**: Valores numéricos calculados
- [ ] **Conclusión**: Resultado final y análisis

---

## 🎯 Consejos Importantes

### ✅ **Para el Examen:**

1. **Verifica la continuidad**: Asegúrate de que $f(x)$ sea continua en $[a, b]$
2. **Calcula paso a paso**: No saltes pasos en las evaluaciones
3. **Usa n par para Simpson**: Simpson 1/3 requiere $n$ par
4. **Compara los errores**: Analiza el orden de error de cada método
5. **Justifica el método**: Explica por qué usas métodos numéricos

### ⚠️ **Errores Comunes:**

- **Olvidar el factor h**: En las fórmulas del trapecio y Simpson
- **No verificar n par**: Para Simpson 1/3
- **No calcular los puntos**: Evaluar $f(x_i)$ en cada punto
- **No analizar errores**: Comparar el orden de error de cada método

---

**¡Con esta guía puedes resolver el ejercicio 3 con cualquier función e intervalo que te den!** 🎓✨
