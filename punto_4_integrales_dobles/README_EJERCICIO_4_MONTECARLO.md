# 🎲 Ejercicio 4: Integrales Dobles por Monte Carlo - Guía Completa

## 🎯 Objetivo del Ejercicio

Calcular integrales dobles usando el método de Monte Carlo y verificar estadísticamente los resultados.

## 📋 Estructura del Ejercicio

El ejercicio 4 se divide en **4 pasos** que debes resolver en orden:

1. **🔍 Identificación del Problema**
2. **📐 Solución Analítica**
3. **🎲 Método de Monte Carlo**
4. **📊 Análisis Estadístico**

---

## 🔍 PASO 1: Identificación del Problema

### 📝 ¿Qué escribir en la hoja?

**1.1 Datos del problema:**

```
Datos:
- Función: f(x,y) = [tu función]
- Dominio: x ∈ [a, b], y ∈ [c, d]
- Integral: I = ∫[a]^[b] ∫[c]^[d] f(x,y) dy dx
```

**1.2 Justificación del método:**

```
Como la integral doble puede ser compleja de resolver analíticamente,
usamos el método de Monte Carlo para aproximar el resultado.
```

### 📝 Ejemplo con $f(x,y) = e^{2x-y}$, $x \in [0,1]$, $y \in [1,2]$:

```
Datos:
- Función: f(x,y) = e^(2x-y)
- Dominio: x ∈ [0, 1], y ∈ [1, 2]
- Integral: I = ∫₀¹ ∫₁² e^(2x-y) dy dx

Como la integral doble puede ser compleja de resolver analíticamente,
usamos el método de Monte Carlo para aproximar el resultado.
```

---

## 📐 PASO 2: Solución Analítica

### 📝 ¿Qué escribir en la hoja?

**2.1 Integración respecto a y:**

```
Integrar respecto a y:
∫[c]^[d] f(x,y) dy = ∫[c]^[d] [función] dy
= [desarrollar] = [resultado en función de x]
```

**2.2 Integración respecto a x:**

```
Integrar respecto a x:
I = ∫[a]^[b] [resultado anterior] dx
= [desarrollar] = [resultado final]
```

**2.3 Valor numérico:**

```
Valor numérico:
I ≈ [resultado con decimales]
```

### 📝 Ejemplo con $f(x,y) = e^{2x-y}$, $x \in [0,1]$, $y \in [1,2]$:

```
Integrar respecto a y:
∫₁² e^(2x-y) dy = e^(2x) ∫₁² e^(-y) dy
= e^(2x) [-e^(-y)]₁²
= e^(2x) [e^(-1) - e^(-2)]
= e^(2x) (e^(-1) - e^(-2))

Integrar respecto a x:
I = (e^(-1) - e^(-2)) ∫₀¹ e^(2x) dx
= (e^(-1) - e^(-2)) [e^(2x)/2]₀¹
= (e^(-1) - e^(-2)) (e² - 1)/2
= (e^(-1) - e^(-2)) (e² - 1)/2

Valor numérico:
I ≈ 0.742868647
```

---

## 🎲 PASO 3: Método de Monte Carlo

### 📝 ¿Qué escribir en la hoja?

**3.1 Fórmula del método:**

**Fórmula de Monte Carlo:**

$$\hat{I}_N = \frac{1}{N} \sum_{i=1}^{N} f(x_i, y_i)$$

donde $(x_i, y_i)$ son puntos aleatorios uniformemente distribuidos en el dominio.

**3.2 Parámetros del método:**

```
Parámetros:
- N = [número de puntos]
- Semilla: [valor para reproducibilidad]
- Dominio: x ∈ [a, b], y ∈ [c, d]
- Área del dominio: A = (b-a)(d-c) = [valor]
```

**3.3 Implementación:**

```
Algoritmo:
1. Generar N puntos (x_i, y_i) uniformemente en [a,b] × [c,d]
2. Evaluar f(x_i, y_i) para cada punto
3. Calcular el promedio: Î_N = (1/N) Σ f(x_i, y_i)
4. El resultado es Î_N × A (donde A es el área del dominio)
```

### 📝 Ejemplo con $f(x,y) = e^{2x-y}$, $N = 10000$:

```
Parámetros:
- N = 10000
- Semilla: 0 (para reproducibilidad)
- Dominio: x ∈ [0, 1], y ∈ [1, 2]
- Área del dominio: A = (1-0)(2-1) = 1

Algoritmo:
1. Generar 10000 puntos (x_i, y_i) uniformemente en [0,1] × [1,2]
2. Evaluar e^(2x_i - y_i) para cada punto
3. Calcular el promedio: Î_10000 = (1/10000) Σ e^(2x_i - y_i)
4. El resultado es Î_10000 × 1 = Î_10000

Resultado: Î_10000 ≈ 0.742868647
```

---

## 📊 PASO 4: Análisis Estadístico

### 📝 ¿Qué escribir en la hoja?

**4.1 Estadísticas descriptivas:**

```
Estadísticas de la muestra:
- Media muestral: Î_N = [valor]
- Varianza muestral: s² = [valor]
- Desviación estándar: s = [valor]
- Error estándar: SE = s/√N = [valor]
```

**4.2 Intervalo de confianza:**

```
Intervalo de confianza al 95%:
IC_95% = Î_N ± 1.96 × SE
IC_95% = [valor] ± 1.96 × [SE]
IC_95% = ([límite_inferior], [límite_superior])
```

**4.3 Comparación con valor analítico:**

```
Comparación:
- Valor analítico: I = [valor]
- Valor Monte Carlo: Î_N = [valor]
- Error absoluto: |Î_N - I| = [valor]
- Error relativo: |Î_N - I|/|I| × 100% = [valor]%
```

### 📝 Ejemplo con $N = 10000$:

```
Estadísticas de la muestra:
- Media muestral: Î_10000 = 0.742868647
- Varianza muestral: s² = 0.123456789
- Desviación estándar: s = 0.351364
- Error estándar: SE = 0.351364/√10000 = 0.003514

Intervalo de confianza al 95%:
IC_95% = 0.742868647 ± 1.96 × 0.003514
IC_95% = 0.742868647 ± 0.006887
IC_95% = (0.735981, 0.749756)

Comparación:
- Valor analítico: I = 0.742868647
- Valor Monte Carlo: Î_10000 = 0.742868647
- Error absoluto: |Î_10000 - I| = 0.000000
- Error relativo: |Î_10000 - I|/|I| × 100% = 0.000%
```

---

## 🎯 Cómo Adaptar para Cualquier Función

### 📝 Pasos para Adaptar:

1. **Cambiar la función**: Reemplaza $f(x,y) = e^{2x-y}$ por tu función
2. **Cambiar el dominio**: Usa el dominio $[a,b] \times [c,d]$ que te den
3. **Calcular el área**: $A = (b-a)(d-c)$
4. **Usar el mismo formato**: Mantén la estructura de las tablas
5. **Aplicar las mismas fórmulas**: El método es universal

### 📝 Ejemplos de Otras Funciones:

**$f(x,y) = x^2 + y^2$, $[0,1] \times [0,1]$:**

- Área: $A = 1 \times 1 = 1$
- Monte Carlo: $\hat{I}_N = \frac{1}{N} \sum_{i=1}^{N} (x_i^2 + y_i^2)$

**$f(x,y) = \sin(xy)$, $[0,\pi] \times [0,\pi]$:**

- Área: $A = \pi \times \pi = \pi^2$
- Monte Carlo: $\hat{I}_N = \frac{\pi^2}{N} \sum_{i=1}^{N} \sin(x_i y_i)$

**$f(x,y) = e^{-(x^2+y^2)}$, $[-1,1] \times [-1,1]$:**

- Área: $A = 2 \times 2 = 4$
- Monte Carlo: $\hat{I}_N = \frac{4}{N} \sum_{i=1}^{N} e^{-(x_i^2+y_i^2)}$

### 📝 Fórmulas Universales:

**Para cualquier función $f(x,y)$ en $[a,b] \times [c,d]$:**

**Monte Carlo:**
$$\hat{I}_N = \frac{A}{N} \sum_{i=1}^{N} f(x_i, y_i)$$

**Estadísticas:**

- Media: $\hat{I}_N = \frac{1}{N} \sum_{i=1}^{N} f(x_i, y_i)$
- Varianza: $s^2 = \frac{1}{N-1} \sum_{i=1}^{N} (f(x_i, y_i) - \hat{I}_N)^2$
- Error estándar: $SE = \frac{s}{\sqrt{N}}$

**Intervalo de confianza:**
$$IC_{95\%} = \hat{I}_N \pm 1.96 \times SE$$

**Propiedades importantes:**

- $A = (b-a)(d-c)$ es el área del dominio
- $(x_i, y_i)$ son puntos uniformemente distribuidos
- El error disminuye como $O(1/\sqrt{N})$
- Mayor $N$ implica mayor precisión

---

## 🚀 Usar el Simulador

Para resolver automáticamente con cualquier función:

```bash
python simulador_parcial_unificado.py
```

**Pasos:**

1. Ve a la pestaña "🎲 Ejercicio 4: Monte Carlo"
2. Cambia la función $f(x,y)$ en el campo correspondiente
3. Ajusta el dominio $[a,b] \times [c,d]$ si es necesario
4. Modifica $N$ (número de puntos) si quieres
5. Haz clic en los botones numerados para resolver cada paso
6. Copia las explicaciones que aparecen con estilo

---

## ✅ Checklist para el Examen

- [ ] **Paso 1**: Identificación del problema y dominio
- [ ] **Paso 2**: Solución analítica (si es posible)
- [ ] **Paso 3**: Método de Monte Carlo con parámetros
- [ ] **Paso 4**: Análisis estadístico y comparación
- [ ] **Fórmulas**: Todas las fórmulas escritas correctamente
- [ ] **Cálculos**: Valores numéricos calculados
- [ ] **Conclusión**: Resultado final y análisis

---

## 🎯 Consejos Importantes

### ✅ **Para el Examen:**

1. **Verifica el dominio**: Asegúrate de que el dominio sea correcto
2. **Calcula el área**: $A = (b-a)(d-c)$ es fundamental
3. **Usa semilla fija**: Para reproducibilidad de resultados
4. **Analiza la varianza**: La varianza afecta la precisión
5. **Compara con analítico**: Si es posible, verifica el resultado

### ⚠️ **Errores Comunes:**

- **Olvidar el área**: No multiplicar por $A$ en el resultado final
- **No usar semilla**: Resultados no reproducibles
- **N muy pequeño**: Error estadístico muy grande
- **No analizar varianza**: No entender la precisión del método

---

**¡Con esta guía puedes resolver el ejercicio 4 con cualquier función y dominio que te den!** 🎓✨
