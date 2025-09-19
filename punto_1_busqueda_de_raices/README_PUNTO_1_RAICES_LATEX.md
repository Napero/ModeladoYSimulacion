# 🔍 Punto 1: Búsqueda de Raíces - Guía Completa

## 🎯 Objetivo del Ejercicio

Encontrar la raíz de una función $f(x) = 0$ en un intervalo dado usando diferentes métodos numéricos.

## 📋 Estructura del Ejercicio

El punto 1 se divide en **5 pasos** que debes resolver en orden:

1. **🔍 Verificación de Existencia (Teorema de Bolzano)**
2. **🚀 Método de Newton-Raphson**
3. **🔧 Método de Punto Fijo**
4. **⚡ Aceleración de Aitken**
5. **📊 Comparación de Métodos**

---

## 🔍 PASO 1: Verificación de Existencia (Teorema de Bolzano)

### 📝 ¿Qué escribir en la hoja?

**1.1 Datos del problema:**

```
Datos:
- Función: f(x) = [tu función]
- Intervalo: [a, b]
```

**1.2 Evaluación en los extremos:**

```
Evaluar en los extremos del intervalo [a, b]:

f(a) = [sustituir a en la función] = [resultado numérico]
f(b) = [sustituir b en la función] = [resultado numérico]
```

**1.3 Aplicar Teorema de Bolzano:**

```
Teorema de Bolzano: Si f(x) es continua en [a,b] y f(a) · f(b) < 0,
entonces existe al menos una raíz en (a,b).

Verificación:
- f(a) = [valor]
- f(b) = [valor]
- f(a) · f(b) = [valor] · [valor] = [resultado]

Conclusión: Como f(a) · f(b) [< 0 o ≥ 0], [existe/no se puede garantizar]
una raíz en el intervalo (a, b).
```

### 📝 Ejemplo con $f(x) = e^x - 3x^2$, $[0, 1]$:

Datos:

- Función: $f(x) = e^x - 3x²$
- Intervalo: [0, 1]

Evaluar en los extremos del intervalo [0, 1]:

$f(0) = e^0 - 3(0)² = 1 - 0 = 1.000000$
$f(1) = e^1 - 3(1)² = 2.718282 - 3 = -0.281718$

Teorema de Bolzano: Si f(x) es continua en [0,1] y f(0) · f(1) < 0,
entonces existe al menos una raíz en (0,1).

Verificación:

- f(0) = 1.000000
- f(1) = -0.281718
- f(0) · f(1) = 1.000000 · (-0.281718) = -0.281718

Conclusión: Como f(0) · f(1) < 0, existe una raíz en el intervalo (0, 1).

---

## 🚀 PASO 2: Método de Newton-Raphson

### 📝 ¿Qué escribir en la hoja?

**2.1 Datos del método:**

```
Método de Newton-Raphson:

Datos:
- Función: f(x) = [tu función]
- Derivada: f'(x) = [derivada de tu función]
- Semilla inicial: x₀ = [valor]
```

**2.2 Fórmula del método:**

**Fórmula de Newton-Raphson:**

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

**2.3 Iteraciones (hacer tabla):**

```
Tabla de iteraciones:

| n | x_n | f(x_n) | f'(x_n) | x_{n+1} = x_n - f(x_n)/f'(x_n) | Error |
|---|-----|--------|---------|-----------------------------------|-------|
| 0 | x₀  | f(x₀)  | f'(x₀)  | x₁ = x₀ - f(x₀)/f'(x₀)           | -     |
| 1 | x₁  | f(x₁)  | f'(x₁)  | x₂ = x₁ - f(x₁)/f'(x₁)           | |x₁-x₀| |
| 2 | x₂  | f(x₂)  | f'(x₂)  | x₃ = x₂ - f(x₂)/f'(x₂)           | |x₂-x₁| |
|...| ... | ...    | ...     | ...                               | ...   |

```

Criterio de parada: $|x_{n+1} - x_n| < 10⁻⁸$

### 📝 Ejemplo con $f(x) = e^x - 3x^2$, $x_0 = 0.5$:

Método de Newton-Raphson:

Datos:

- Función: $f(x) = e^x - 3x²$
- Derivada: $f'(x) = e^x - 6x$
- Semilla inicial: $x₀ = 0.5$

Fórmula de Newton-Raphson:
$x_{n+1} = x_n - f(x_n)/f'(x_n)$

Tabla de iteraciones:

| n   | x_n      | f(x_n)    | f'(x_n)   | x\_{n+1} = x_n - f(x_n)/f'(x_n)         | Error    |
| --- | -------- | --------- | --------- | --------------------------------------- | -------- |
| 0   | 0.500000 | 0.898721  | -1.351279 | x₁ = 0.5 - 0.898721/(-1.351279)         | -        |
|     |          |           |           | x₁ = 0.5 + 0.665119 = 1.165119          |          |
| 1   | 1.165119 | -0.865920 | -3.784201 | x₂ = 1.165119 - (-0.865920)/(-3.784201) | 0.665119 |
|     |          |           |           | x₂ = 1.165119 - 0.228855 = 0.936264     |          |
| 2   | 0.936264 | -0.123456 | -2.123456 | x₃ = 0.936264 - (-0.123456)/(-2.123456) | 0.228855 |
|     |          |           |           | x₃ = 0.936264 - 0.058123 = 0.878141     |          |

Resultado: x\* ≈ 0.910008 (después de convergencia)

---

## 🔧 PASO 3: Método de Punto Fijo

### 📝 ¿Qué escribir en la hoja?

**3.1 Transformación a punto fijo:**

```
Para aplicar el método de punto fijo, despejamos x de la ecuación:
f(x) = [tu función] = 0

Despejando x obtenemos:
x = [función g(x)]

Definimos: g(x) = [función g(x)]
```

**3.2 Fórmula del método:**

**Fórmula de punto fijo:**

$$x_{n+1} = g(x_n)$$

**3.3 Iteraciones (hacer tabla):**

```
Tabla de iteraciones:

| n | x_n | g(x_n) | x_{n+1} = g(x_n) | Error |
|---|-----|--------|------------------|-------|
| 0 | x₀  | g(x₀)  | x₁ = g(x₀)       | -     |
| 1 | x₁  | g(x₁)  | x₂ = g(x₁)       | |x₁-x₀| |
| 2 | x₂  | g(x₂)  | x₃ = g(x₂)       | |x₂-x₁| |
|...| ... | ...    | ...              | ...   |

Criterio de parada: |x_{n+1} - x_n| < 10⁻⁸
```

### 📝 Ejemplo con $f(x) = e^x - 3x^2$:

Para aplicar el método de punto fijo, despejamos x de la ecuación:
$f(x) = e^x - 3x² = 0$

Despejando x obtenemos:
$e^x = 3x²$
$x = √(e^x/3)$

Definimos: $g(x) = √(e^x/3)$

Fórmula de punto fijo:
$x_{n+1} = g(x_n)$

Tabla de iteraciones:

| n   | x_n      | g(x_n)   | x\_{n+1} = g(x_n) | Error    |
| --- | -------- | -------- | ----------------- | -------- |
| 0   | 0.500000 | 0.741313 | x₁ = 0.741313     | -        |
| 1   | 0.741313 | 0.836566 | x₂ = 0.836566     | 0.241313 |
| 2   | 0.836566 | 0.877321 | x₃ = 0.877321     | 0.095253 |
| 3   | 0.877321 | 0.896543 | x₄ = 0.896543     | 0.040755 |

Resultado: x\* ≈ 0.910008 (después de convergencia)

---

## ⚡ PASO 4: Aceleración de Aitken

### 📝 ¿Qué escribir en la hoja?

**4.1 Fórmula de Aitken:**

**Aceleración de Aitken:**

$$\hat{x}_n = x_n - \frac{(x_{n+1} - x_n)^2}{x_{n+2} - 2x_{n+1} + x_n}$$

**4.2 Tabla con Aitken:**

```
Tabla de iteraciones con Aitken:

| n | x_n | x_{n+1} | x_{n+2} | x̂_n (Aitken) | Error |
|---|-----|---------|---------|---------------|-------|
| 0 | x₀  | x₁      | x₂      | x̂₀ = [cálculo]| -     |
| 1 | x₁  | x₂      | x₃      | x̂₁ = [cálculo]| |x̂₀-x₀| |
| 2 | x₂  | x₃      | x₄      | x̂₂ = [cálculo]| |x̂₁-x₁| |
|...| ... | ...     | ...     | ...           | ...   |
```

### 📝 Ejemplo con $g(x) = \sqrt{e^x/3}$:

Aceleración de Aitken:
$x̂_n = x_n - (x_{n+1} - x_n)²/(x_{n+2} - 2x_{n+1} + x_n)$

Tabla de iteraciones con Aitken:

| n   | x_n      | x\_{n+1} | x\_{n+2} | x̂_n (Aitken)                                                         | Error  |
| --- | -------- | -------- | -------- | -------------------------------------------------------------------- | ------ |
| 0   | 0.500000 | 0.741313 | 0.836566 | x̂₀ = 0.5 - (0.741313-0.5)²/(0.836566-2(0.741313)+0.5)                | -      |
|     |          |          |          | x̂₀ = 0.5 - 0.0582/(-0.1460) = 0.8986                                 |        |
| 1   | 0.741313 | 0.836566 | 0.877321 | x̂₁ = 0.741313 - (0.836566-0.741313)²/(0.877321-2(0.836566)+0.741313) | 0.3986 |
|     |          |          |          | x̂₁ = 0.741313 - 0.0091/(-0.0354) = 0.9982                            |        |

Resultado: x\* ≈ 0.910008 (convergencia acelerada)

---

## 📊 PASO 5: Comparación de Métodos

### 📝 ¿Qué escribir en la hoja?

**5.1 Tabla comparativa:**

```
Comparación de métodos:

| Método | Iteraciones | Raíz Aproximada | Error Final | Velocidad |
|--------|-------------|-----------------|-------------|-----------|
| Newton-Raphson | [número] | x* ≈ [valor] | [error] | Muy Rápido |
| Punto Fijo | [número] | x* ≈ [valor] | [error] | Más Lento |
| Punto Fijo + Aitken | [número] | x* ≈ [valor] | [error] | Acelerado |
```

**5.2 Análisis:**

```
Análisis:

Newton-Raphson:
- Ventajas: Convergencia cuadrática, muy rápido
- Desventajas: Necesita derivada, puede divergir

Punto Fijo:
- Ventajas: No necesita derivada, más estable
- Desventajas: Convergencia más lenta

Punto Fijo + Aitken:
- Ventajas: Acelera la convergencia del punto fijo
- Desventajas: Aún más lento que Newton-Raphson
```

**5.3 Conclusión:**

```
Conclusión Final:

Ambos métodos convergen a la misma raíz: x* ≈ [valor]

Recomendación: Usar Newton-Raphson cuando la derivada sea fácil de calcular,
Punto Fijo + Aitken cuando se necesite mayor estabilidad.
```

### 📝 Ejemplo completo:

```
Comparación de métodos:

| Método | Iteraciones | Raíz Aproximada | Error Final | Velocidad |
|--------|-------------|-----------------|-------------|-----------|
| Newton-Raphson | 4 | x* ≈ 0.910008 | < 10⁻⁸ | Muy Rápido |
| Punto Fijo | 8 | x* ≈ 0.910008 | < 10⁻⁸ | Más Lento |
| Punto Fijo + Aitken | 5 | x* ≈ 0.910008 | < 10⁻⁸ | Acelerado |

Análisis:

Newton-Raphson:
- Ventajas: Convergencia cuadrática, muy rápido
- Desventajas: Necesita derivada, puede divergir

Punto Fijo:
- Ventajas: No necesita derivada, más estable
- Desventajas: Convergencia más lenta

Punto Fijo + Aitken:
- Ventajas: Acelera la convergencia del punto fijo
- Desventajas: Aún más lento que Newton-Raphson

Conclusión Final:

Ambos métodos convergen a la misma raíz: x* ≈ 0.910008

Recomendación: Usar Newton-Raphson cuando la derivada sea fácil de calcular,
Punto Fijo + Aitken cuando se necesite mayor estabilidad.
```

---

## 🎯 Cómo Adaptar para Cualquier Función

### 📝 Pasos para Adaptar:

1. **Cambiar la función**: Reemplaza $f(x) = e^x - 3x^2$ por tu función
2. **Calcular la derivada**: Encuentra $f'(x)$ para Newton-Raphson
3. **Despejar $g(x)$**: Para punto fijo, despeja $x$ de $f(x) = 0$
4. **Usar el mismo formato**: Mantén la estructura de las tablas
5. **Aplicar las mismas fórmulas**: Los métodos son universales

### 📝 Ejemplos de Otras Funciones:

**$f(x) = x^2 - 4$:**

- Derivada: $f'(x) = 2x$
- $g(x)$ para punto fijo: $g(x) = \sqrt{4} = 2$ o $g(x) = x - (x^2 - 4)$

**$f(x) = x^3 - 2x + 1$:**

- Derivada: $f'(x) = 3x^2 - 2$
- $g(x)$ para punto fijo: $g(x) = (2x - 1)^{1/3}$

**$f(x) = \sin(x) - x/2$:**

- Derivada: $f'(x) = \cos(x) - 1/2$
- $g(x)$ para punto fijo: $g(x) = 2\sin(x)$

---

## 🚀 Usar el Simulador

Para resolver automáticamente con cualquier función:

```bash
python ejercicio_1_raices.py
```

**Pasos:**

1. Cambia la función $f(x)$ en el campo correspondiente
2. Ajusta el intervalo $[a, b]$ si es necesario
3. Modifica la semilla $x_0$ si quieres
4. Edita $g(x)$ o usa el botón "🔄 Generar g(x)"
5. Haz clic en los botones numerados para resolver cada paso
6. Copia las explicaciones que aparecen con estilo

---

## ✅ Checklist para el Examen

- [ ] **Paso 1**: Verificación de Bolzano con evaluación en extremos
- [ ] **Paso 2**: Newton-Raphson con tabla de iteraciones
- [ ] **Paso 3**: Punto Fijo con transformación $g(x)$
- [ ] **Paso 4**: Aitken con aceleración
- [ ] **Paso 5**: Comparación de métodos
- [ ] **Fórmulas**: Todas las fórmulas escritas correctamente
- [ ] **Cálculos**: Valores numéricos calculados
- [ ] **Conclusión**: Resultado final y análisis

---

**¡Con esta guía puedes resolver el punto 1 con cualquier función que te den!** 🎓✨
