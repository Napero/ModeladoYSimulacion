# 📈 Ejercicio 2: Interpolación de Lagrange - Guía Completa

## 🎯 Objetivo del Ejercicio

Encontrar el polinomio de Lagrange que interpola una función $f(x)$ en puntos dados, evaluarlo en un punto específico y calcular su derivada.

## 📋 Estructura del Ejercicio

El ejercicio 2 se divide en **3 pasos** que debes resolver en orden:

1. **📊 Calcular Polinomio de Lagrange**
2. **🎯 Evaluar en Punto Específico**
3. **📐 Calcular Derivada del Polinomio**

---

## 📊 PASO 1: Calcular Polinomio de Lagrange

### 📝 ¿Qué escribir en la hoja?

**1.1 Datos del problema:**

```
Datos:
- Función: f(x) = [tu función]
- Nodos: x₀ = [valor], x₁ = [valor], x₂ = [valor], ...
- Puntos: (x₀, f(x₀)), (x₁, f(x₁)), (x₂, f(x₂)), ...
```

**1.2 Fórmula general de Lagrange:**

$$P_n(x) = \sum_{i=0}^{n} f(x_i) \cdot L_i(x)$$

donde:

$$L_i(x) = \prod_{\substack{j=0 \\ j \neq i}}^{n} \frac{x - x_j}{x_i - x_j}$$

**1.3 Calcular polinomios base $L_i(x)$:**

Para cada $i$, calcular $L_i(x)$:

$$L_0(x) = \frac{(x - x_1)(x - x_2)\cdots(x - x_n)}{(x_0 - x_1)(x_0 - x_2)\cdots(x_0 - x_n)}$$

$$L_1(x) = \frac{(x - x_0)(x - x_2)\cdots(x - x_n)}{(x_1 - x_0)(x_1 - x_2)\cdots(x_1 - x_n)}$$

$$L_2(x) = \frac{(x - x_0)(x - x_1)\cdots(x - x_n)}{(x_2 - x_0)(x_2 - x_1)\cdots(x_2 - x_n)}$$

**1.4 Construir el polinomio final:**

$$P_n(x) = f(x_0) \cdot L_0(x) + f(x_1) \cdot L_1(x) + f(x_2) \cdot L_2(x) + \cdots$$

### 📝 Ejemplo con $f(x) = \ln(x+1)$, nodos $[0, 1, 2]$:

```
Datos:
- Función: f(x) = ln(x+1)
- Nodos: x₀ = 0, x₁ = 1, x₂ = 2
- Puntos: (0, ln(1)), (1, ln(2)), (2, ln(3))

Evaluar en los nodos:
f(0) = ln(0+1) = ln(1) = 0.000000
f(1) = ln(1+1) = ln(2) = 0.693147
f(2) = ln(2+1) = ln(3) = 1.098612

Polinomio de Lagrange de grado 2:
P₂(x) = f(x₀)·L₀(x) + f(x₁)·L₁(x) + f(x₂)·L₂(x)
```

**Calcular polinomios base $L_i(x)$:**

$$L_0(x) = \frac{(x - x_1)(x - x_2)}{(x_0 - x_1)(x_0 - x_2)} = \frac{(x - 1)(x - 2)}{(0 - 1)(0 - 2)} = \frac{(x - 1)(x - 2)}{2}$$

$$L_0(x) = \frac{x^2 - 3x + 2}{2}$$

$$L_1(x) = \frac{(x - x_0)(x - x_2)}{(x_1 - x_0)(x_1 - x_2)} = \frac{x(x - 2)}{(1)(-1)} = -x(x - 2)$$

$$L_1(x) = -x^2 + 2x$$

$$L_2(x) = \frac{(x - x_0)(x - x_1)}{(x_2 - x_0)(x_2 - x_1)} = \frac{x(x - 1)}{(2)(1)} = \frac{x(x - 1)}{2}$$

$$L_2(x) = \frac{x^2 - x}{2}$$

**Construir el polinomio final:**

$$P_2(x) = f(0) \cdot L_0(x) + f(1) \cdot L_1(x) + f(2) \cdot L_2(x)$$

$$P_2(x) = 0.000000 \cdot L_0(x) + 0.693147 \cdot L_1(x) + 1.098612 \cdot L_2(x)$$

$$P_2(x) = 0.693147 \cdot (-x^2 + 2x) + 1.098612 \cdot \frac{x^2 - x}{2}$$

$$P_2(x) = -0.693147x^2 + 1.386294x + 0.549306x^2 - 0.549306x$$

$$P_2(x) = (-0.693147 + 0.549306)x^2 + (1.386294 - 0.549306)x$$

$$P_2(x) = -0.143841x^2 + 0.836988x$$

---

## 🎯 PASO 2: Evaluar en Punto Específico

### 📝 ¿Qué escribir en la hoja?

**2.1 Datos para evaluación:**

```
Evaluar el polinomio P_n(x) en x = [punto]
```

**2.2 Sustitución directa:**

```
P_n([punto]) = [sustituir en el polinomio]
P_n([punto]) = [desarrollar cálculo]
P_n([punto]) = [resultado final]
```

**2.3 Verificación con función original:**

```
Verificación:
f([punto]) = [sustituir en función original]
f([punto]) = [resultado]

Error de interpolación: |P_n([punto]) - f([punto])| = [diferencia]
```

### 📝 Ejemplo con $P_2(x) = -0.143841x^2 + 0.836988x$, evaluar en $x = 0.45$:

```
Evaluar el polinomio P₂(x) en x = 0.45

P₂(0.45) = -0.143841(0.45)² + 0.836988(0.45)
P₂(0.45) = -0.143841(0.2025) + 0.836988(0.45)
P₂(0.45) = -0.029128 + 0.376645
P₂(0.45) = 0.347517

Verificación:
f(0.45) = ln(0.45 + 1) = ln(1.45) = 0.371564

Error de interpolación: |P₂(0.45) - f(0.45)| = |0.347517 - 0.371564| = 0.024047
```

---

## 📐 PASO 3: Calcular Derivada del Polinomio

### 📝 ¿Qué escribir en la hoja?

**3.1 Derivada del polinomio:**

```
Derivada del polinomio P_n(x):
P'_n(x) = d/dx[P_n(x)]
P'_n(x) = [derivar término por término]
```

**3.2 Evaluar derivada en punto:**

```
Evaluar P'_n(x) en x = [punto]:
P'_n([punto]) = [sustituir en derivada]
P'_n([punto]) = [resultado]
```

**3.3 Verificación con derivada original:**

```
Verificación con derivada de f(x):
f'(x) = [derivada de función original]
f'([punto]) = [sustituir en derivada original]
f'([punto]) = [resultado]

Error de derivada: |P'_n([punto]) - f'([punto])| = [diferencia]
```

### 📝 Ejemplo con $P_2(x) = -0.143841x^2 + 0.836988x$:

**Derivada del polinomio:**

$$P'_2(x) = \frac{d}{dx}[-0.143841x^2 + 0.836988x]$$

$$P'_2(x) = -0.143841(2x) + 0.836988(1)$$

$$P'_2(x) = -0.287682x + 0.836988$$

**Evaluar $P'_2(x)$ en $x = 1.5$:**

$$P'_2(1.5) = -0.287682(1.5) + 0.836988$$

$$P'_2(1.5) = -0.431523 + 0.836988$$

$$P'_2(1.5) = 0.405465$$

**Verificación con derivada de $f(x)$:**

$$f'(x) = \frac{d}{dx}[\ln(x+1)] = \frac{1}{x+1}$$

$$f'(1.5) = \frac{1}{1.5 + 1} = \frac{1}{2.5} = 0.400000$$

**Error de derivada:**

$$|P'_2(1.5) - f'(1.5)| = |0.405465 - 0.400000| = 0.005465$$

---

## 🎯 Cómo Adaptar para Cualquier Función

### 📝 Pasos para Adaptar:

1. **Cambiar la función**: Reemplaza $f(x) = \ln(x+1)$ por tu función
2. **Cambiar los nodos**: Usa los nodos que te den
3. **Calcular $f(x_i)$**: Evalúa tu función en cada nodo
4. **Usar el mismo formato**: Mantén la estructura de las fórmulas
5. **Aplicar las mismas reglas**: Los polinomios base se calculan igual

### 📝 Ejemplos de Otras Funciones:

**$f(x) = x^2$, nodos $[0, 1, 2]$:**

- $f(0) = 0$, $f(1) = 1$, $f(2) = 4$
- $L_0(x) = \frac{(x-1)(x-2)}{2}$, $L_1(x) = -x(x-2)$, $L_2(x) = \frac{x(x-1)}{2}$
- $P_2(x) = 0 \cdot L_0(x) + 1 \cdot L_1(x) + 4 \cdot L_2(x) = -x^2 + 2x + 2x^2 - 2x = x^2$

**$f(x) = e^x$, nodos $[0, 1, 2]$:**

- $f(0) = 1$, $f(1) = e$, $f(2) = e^2$
- $P_2(x) = 1 \cdot L_0(x) + e \cdot L_1(x) + e^2 \cdot L_2(x)$

**$f(x) = \sin(x)$, nodos $[0, \frac{\pi}{2}, \pi]$:**

- $f(0) = 0$, $f(\frac{\pi}{2}) = 1$, $f(\pi) = 0$
- $P_2(x) = 0 \cdot L_0(x) + 1 \cdot L_1(x) + 0 \cdot L_2(x) = L_1(x)$

### 📝 Fórmulas Universales:

**Para $n+1$ nodos $x_0, x_1, \ldots, x_n$:**

$$L_i(x) = \prod_{\substack{j=0 \\ j \neq i}}^{n} \frac{x - x_j}{x_i - x_j}$$

$$P_n(x) = \sum_{i=0}^{n} f(x_i) \cdot L_i(x)$$

$$P'_n(x) = \sum_{i=0}^{n} f(x_i) \cdot L'_i(x)$$

**Propiedades importantes:**

- $L_i(x_j) = 1$ si $i = j$, $0$ si $i \neq j$
- $P_n(x_i) = f(x_i)$ para todos los nodos
- El polinomio es único para los nodos dados

---

## 📊 Tabla de Resumen

### 📝 Formato para la hoja:

```
RESUMEN DEL EJERCICIO 2:

Datos:
- Función: f(x) = [tu función]
- Nodos: [lista de nodos]
- Punto de evaluación: x = [valor]
- Punto de derivada: x = [valor]

Resultados:
- Polinomio de Lagrange: P_n(x) = [polinomio final]
- Evaluación: P_n([punto]) = [resultado]
- Derivada: P'_n(x) = [derivada]
- Derivada evaluada: P'_n([punto]) = [resultado]

Errores:
- Error de interpolación: [valor]
- Error de derivada: [valor]
```

---

## 🚀 Usar el Simulador

Para resolver automáticamente con cualquier función:

```bash
python ejercicio_1_raices.py
```

**Pasos:**

1. Ve a la pestaña "📈 Ejercicio 2: Lagrange"
2. Cambia la función $f(x)$ en el campo correspondiente
3. Ajusta los nodos si es necesario
4. Haz clic en los botones numerados para resolver cada paso
5. Copia las explicaciones que aparecen con estilo

---

## ✅ Checklist para el Examen

- [ ] **Paso 1**: Calcular polinomios base $L_i(x)$
- [ ] **Paso 1**: Construir polinomio final $P_n(x)$
- [ ] **Paso 2**: Evaluar $P_n(x)$ en punto específico
- [ ] **Paso 2**: Verificar con función original
- [ ] **Paso 3**: Calcular derivada $P'_n(x)$
- [ ] **Paso 3**: Evaluar derivada en punto
- [ ] **Fórmulas**: Todas las fórmulas de Lagrange escritas
- [ ] **Cálculos**: Valores numéricos calculados
- [ ] **Errores**: Errores de interpolación y derivada

---

## 🎯 Consejos Importantes

### ✅ **Para el Examen:**

1. **Verifica siempre**: $P_n(x_i) = f(x_i)$ en todos los nodos
2. **Calcula paso a paso**: No saltes pasos en los polinomios base
3. **Simplifica el polinomio**: Combina términos semejantes
4. **Verifica la derivada**: Usa la regla de la cadena correctamente
5. **Calcula errores**: Siempre compara con la función original

### ⚠️ **Errores Comunes:**

- **Olvidar el signo**: En los denominadores de $L_i(x)$
- **No simplificar**: Dejar el polinomio sin combinar términos
- **Derivada incorrecta**: No aplicar la regla de la cadena
- **No verificar**: No comprobar que $P_n(x_i) = f(x_i)$

---

**¡Con esta guía puedes resolver el ejercicio 2 con cualquier función y nodos que te den!** 🎓✨
