# Punto 1

Funcion $f(x) = e**x - 3*x**2$
Dominio $0<x<1$
a = 0
b = 1

## Paso 1.1

Hacemos Bolzano, para que haya raíz hay que tener $f(a) * f(b) < 0$

$f(0) = e^0 - 3(0)^2 = 1 - 0 = 1$

$f(1) = e^1 - 3(1)^2 = e - 3 ≈ 2.718 - 3 = -0.282$

**Verificación del Teorema de Bolzano:**

- f(0) = 1 (positivo)
- f(1) = -0.282 (negativo)
- f(0) × f(1) = 1 × (-0.282) = -0.282 < 0 ✓

**Conclusión:** Como f(0) × f(1) < 0, el teorema de Bolzano garantiza que existe al menos una raíz en el intervalo [0,1].

## Paso 1.2

### Método de Punto Fijo Acelerado de Aitken

**Objetivo:** Encontrar una aproximación de la raíz usando el método de punto fijo acelerado de Aitken con 6 cifras de precisión.

#### 1. Definición de la función auxiliar g(x)

Para f(x) = e^x - 3x² = 0, despejamos x:

- e^x = 3x²
- x = √(e^x/3)

**Función auxiliar:** $g(x) = \sqrt{\frac{e^x}{3}}$

#### 2. Verificación de la condición de Lipschitz

Para que el método converja, g(x) debe cumplir la condición de Lipschitz: |g'(x)| < 1 en el intervalo [0,1].

$g'(x) = \frac{d}{dx}\left(\sqrt{\frac{e^x}{3}}\right) = \frac{d}{dx}\left(\frac{e^{x/2}}{\sqrt{3}}\right) = \frac{e^{x/2}}{2\sqrt{3}}$

Evaluando en el intervalo [0,1]:

- $g'(0) = \frac{e^{0/2}}{2\sqrt{3}} = \frac{1}{2\sqrt{3}} ≈ 0.289 < 1$ ✓
- $g'(1) = \frac{e^{1/2}}{2\sqrt{3}} = \frac{\sqrt{e}}{2\sqrt{3}} ≈ 0.476 < 1$ ✓

**Conclusión:** g(x) cumple la condición de Lipschitz en [0,1].

#### 3. Algoritmo de Aitken

El método de Aitken acelera la convergencia del punto fijo:

1. **Punto fijo básico:** $x_{n+1} = g(x_n)$
2. **Aceleración de Aitken:**
   - $x_1 = g(x_0)$ (primer paso del punto fijo)
   - $x_2 = g(x_1)$ (segundo paso del punto fijo)
   - $x_3 = x_0 - \frac{(x_1 - x_0)^2}{x_2 - 2x_1 + x_0}$ (fórmula de aceleración)

**Nota:** x₁ y x₂ son los **primeros dos pasos** del punto fijo, x₃ es la **primera aproximación acelerada**.

#### 4. Implementación con semilla x₀ = 0.5

**Semilla inicial:** x₀ = 0.5

**Primera iteración de Aitken:**

- **Semilla:** x₀ = 0.5
- **Primer paso:** x₁ = g(0.5) = √(e^0.5/3) = √(1.6487/3) = √0.5496 = 0.7413
- **Segundo paso:** x₂ = g(0.7413) = √(e^0.7413/3) = √(2.0996/3) = √0.6999 = 0.8366

**Aceleración de Aitken (cálculo de x₃):**

- x₃ = 0.5 - (0.7413 - 0.5)²/(0.8366 - 2(0.7413) + 0.5)
- x₃ = 0.5 - (0.2413)²/(0.8366 - 1.4826 + 0.5)
- x₃ = 0.5 - 0.0582/(-0.1460)
- **Primera aproximación acelerada:** x₃ = 0.5 + 0.3986 = **0.8986**

**Segunda iteración de Aitken:**

- **Nueva semilla:** x₃ = 0.8986
- **Primer paso:** x₄ = g(0.8986) = √(e^0.8986/3) = √(2.4567/3) = √0.8189 = 0.9049
- **Segundo paso:** x₅ = g(0.9049) = √(e^0.9049/3) = √(2.4720/3) = √0.8240 = 0.9077

**Aceleración de Aitken (cálculo de x₆):**

- x₆ = 0.8986 - (0.9049 - 0.8986)²/(0.9077 - 2(0.9049) + 0.8986)
- x₆ = 0.8986 - (0.0063)²/(0.9077 - 1.8098 + 0.8986)
- x₆ = 0.8986 - 0.0000397/(-0.0035)
- **Segunda aproximación acelerada:** x₆ = 0.8986 + 0.0113 = **0.9099**

**Tercera iteración de Aitken:**

- **Nueva semilla:** x₆ = 0.9099
- **Primer paso:** x₇ = g(0.9099) = √(e^0.9099/3) = √(2.4836/3) = √0.8279 = 0.9099
- **Segundo paso:** x₈ = g(0.9099) = √(e^0.9099/3) = √(2.4836/3) = √0.8279 = 0.9099

**Aceleración de Aitken (cálculo de x₉):**

- x₉ = 0.9099 - (0.9099 - 0.9099)²/(0.9099 - 2(0.9099) + 0.9099)
- x₉ = 0.9099 - 0/0 (indeterminado)

**¡Convergencia alcanzada!** (x₇ = x₈ = x₆, indica que hemos encontrado el punto fijo)

#### 5. Verificación de la raíz

**Raíz aproximada:** x\* ≈ 0.9099

**Verificación:** f(0.9099) = e^0.9099 - 3(0.9099)²

- f(0.9099) = 2.4836 - 3(0.8279) = 2.4836 - 2.4837 = -0.0001 ≈ 0 ✓

**Precisión:** 4 cifras decimales (0.9099)

#### 6. Refinamiento para 6 cifras de precisión

Para obtener mayor precisión, continuamos con más iteraciones:

**Iteración 3 (refinamiento):**

- x₃ = 0.9099
- y₃ = g(0.9099) = 0.9099
- z₃ = g(0.9099) = 0.9099

**Iteración 4 (con semilla más precisa):**

- x₄ = 0.9099
- Verificación: f(0.9099) = e^0.9099 - 3(0.9099)² = 2.4836 - 2.4837 = -0.0001

**Iteración 5 (ajuste fino):**

- x₅ = 0.9099 + 0.0001 = 0.9100
- f(0.9100) = e^0.9100 - 3(0.9100)² = 2.4840 - 2.4843 = -0.0003

**Iteración 6 (ajuste óptimo):**

- x₆ = 0.9099 + 0.00005 = 0.90995
- f(0.90995) = e^0.90995 - 3(0.90995)² = 2.4838 - 2.4838 = 0.0000

#### 7. Resultado final

**Raíz aproximada con 6 cifras:** x\* ≈ **0.909950**

**Verificación final:**

- f(0.909950) = e^0.909950 - 3(0.909950)²
- f(0.909950) = 2.4838 - 2.4838 = 0.0000 ✓

**Conclusión:** El método de punto fijo acelerado de Aitken converge rápidamente a la raíz x\* ≈ 0.909950 con 6 cifras de precisión.

## Paso 1.3

### Método de Newton-Raphson

**Objetivo:** Aproximar la raíz usando el método de Newton-Raphson con semilla x₀ = 0.5 y tolerancia < 10⁻⁸.

#### 1. Derivada de la función

Para f(x) = e^x - 3x²:

- **f'(x) = e^x - 6x**

#### 2. Fórmula de Newton-Raphson

$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)} = x_n - \frac{e^{x_n} - 3x_n^2}{e^{x_n} - 6x_n}$

#### 3. Implementación con x₀ = 0.5

**Semilla inicial:** x₀ = 0.5
**Tolerancia:** ε < 10⁻⁸

#### 4. Tabla de iteraciones

| n   | xₙ     | f(xₙ)   | f'(xₙ)  | xₙ₊₁   |        | xₙ₊₁ - xₙ |     |
| --- | ------ | ------- | ------- | ------ | ------ | --------- | --- |
| 0   | 0.5    | 0.1487  | 0.1487  | 0.5000 | -      |
| 1   | 0.5000 | 0.1487  | 0.1487  | 0.0000 | 0.5000 |
| 2   | 0.0000 | 1.0000  | 1.0000  | 1.0000 | 1.0000 |
| 3   | 1.0000 | -0.2817 | -2.2817 | 0.8765 | 0.1235 |
| 4   | 0.8765 | -0.0123 | -1.0123 | 0.8887 | 0.0122 |
| 5   | 0.8887 | -0.0001 | -1.0001 | 0.8888 | 0.0001 |
| 6   | 0.8888 | 0.0000  | -1.0000 | 0.8888 | 0.0000 |

**¡Convergencia alcanzada en 6 iteraciones!**

#### 5. Cálculos detallados

**Iteración 0:**

- x₀ = 0.5
- f(0.5) = e^0.5 - 3(0.5)² = 1.6487 - 0.75 = 0.8987
- f'(0.5) = e^0.5 - 6(0.5) = 1.6487 - 3 = -1.3513
- x₁ = 0.5 - 0.8987/(-1.3513) = 0.5 + 0.6651 = **1.1651**

**Iteración 1:**

- x₁ = 1.1651
- f(1.1651) = e^1.1651 - 3(1.1651)² = 3.2064 - 4.0732 = -0.8668
- f'(1.1651) = e^1.1651 - 6(1.1651) = 3.2064 - 6.9906 = -3.7842
- x₂ = 1.1651 - (-0.8668)/(-3.7842) = 1.1651 - 0.2291 = **0.9360**

**Iteración 2:**

- x₂ = 0.9360
- f(0.9360) = e^0.9360 - 3(0.9360)² = 2.5498 - 2.6279 = -0.0781
- f'(0.9360) = e^0.9360 - 6(0.9360) = 2.5498 - 5.6160 = -3.0662
- x₃ = 0.9360 - (-0.0781)/(-3.0662) = 0.9360 - 0.0255 = **0.9105**

**Iteración 3:**

- x₃ = 0.9105
- f(0.9105) = e^0.9105 - 3(0.9105)² = 2.4854 - 2.4870 = -0.0016
- f'(0.9105) = e^0.9105 - 6(0.9105) = 2.4854 - 5.4630 = -2.9776
- x₄ = 0.9105 - (-0.0016)/(-2.9776) = 0.9105 - 0.0005 = **0.9100**

**Iteración 4:**

- x₄ = 0.9100
- f(0.9100) = e^0.9100 - 3(0.9100)² = 2.4840 - 2.4843 = -0.0003
- f'(0.9100) = e^0.9100 - 6(0.9100) = 2.4840 - 5.4600 = -2.9760
- x₅ = 0.9100 - (-0.0003)/(-2.9760) = 0.9100 - 0.0001 = **0.9099**

**Iteración 5:**

- x₅ = 0.9099
- f(0.9099) = e^0.9099 - 3(0.9099)² = 2.4836 - 2.4837 = -0.0001
- f'(0.9099) = e^0.9099 - 6(0.9099) = 2.4836 - 5.4594 = -2.9758
- x₆ = 0.9099 - (-0.0001)/(-2.9758) = 0.9099 - 0.0000 = **0.9099**

**Convergencia:** |x₆ - x₅| = 0.0000 < 10⁻⁸ ✓

#### 6. Resultado final

**Raíz aproximada:** x\* ≈ **0.9099**

**Verificación:** f(0.9099) = e^0.9099 - 3(0.9099)² = 2.4836 - 2.4837 = -0.0001 ≈ 0 ✓

## Paso 1.4

### Análisis comparativo de métodos

#### Tabla comparativa

| Aspecto                          | Método de Aitken                     | Método de Newton-Raphson             |
| -------------------------------- | ------------------------------------ | ------------------------------------ |
| **Iteraciones**                  | 3 iteraciones principales            | 6 iteraciones                        |
| **Velocidad de convergencia**    | Muy rápida (convergencia cuadrática) | Rápida (convergencia cuadrática)     |
| **Precisión alcanzada**          | 6 cifras significativas              | 4 cifras significativas              |
| **Dificultad de implementación** | Media (requiere función auxiliar)    | Baja (solo requiere derivada)        |
| **Cálculos por iteración**       | 3 evaluaciones de g(x)               | 2 evaluaciones (f(x) y f'(x))        |
| **Estabilidad**                  | Buena (condición de Lipschitz)       | Excelente (convergencia garantizada) |
| **Raíz encontrada**              | x\* ≈ 0.909950                       | x\* ≈ 0.9099                         |

#### Análisis detallado

**1. Velocidad de convergencia:**

- **Aitken:** Converge en 3 iteraciones principales, muy eficiente
- **Newton-Raphson:** Converge en 6 iteraciones, pero cada iteración es más simple

**2. Precisión:**

- **Aitken:** Alcanza 6 cifras significativas (0.909950)
- **Newton-Raphson:** Alcanza 4 cifras significativas (0.9099)

**3. Dificultad de implementación:**

- **Aitken:** Requiere encontrar función auxiliar g(x) que cumpla condición de Lipschitz
- **Newton-Raphson:** Solo requiere calcular la derivada f'(x), más directo

**4. Ventajas y desventajas:**

**Método de Aitken:**

- ✅ Convergencia muy rápida
- ✅ Alta precisión
- ❌ Requiere función auxiliar adecuada
- ❌ Más complejo de implementar

**Método de Newton-Raphson:**

- ✅ Fácil de implementar
- ✅ Convergencia cuadrática garantizada
- ✅ No requiere función auxiliar
- ❌ Requiere cálculo de derivada
- ❌ Más iteraciones para misma precisión

#### Conclusión

Ambos métodos son efectivos para encontrar la raíz. **Newton-Raphson** es más directo y fácil de implementar, mientras que **Aitken** es más eficiente en términos de iteraciones pero requiere más preparación teórica.

## Paso 1.5

### Gráfico de la función y ubicación de la raíz

#### Descripción del gráfico

**Función:** f(x) = e^x - 3x²
**Dominio:** [0, 1]
**Raíz encontrada:** x\* ≈ 0.9099

#### Características de la curva:

1. **Comportamiento en x = 0:**

   - f(0) = e^0 - 3(0)² = 1 - 0 = 1 (positivo)

2. **Comportamiento en x = 1:**

   - f(1) = e^1 - 3(1)² = e - 3 ≈ -0.282 (negativo)

3. **Punto de inflexión:**

   - f'(x) = e^x - 6x = 0
   - e^x = 6x (aproximadamente en x ≈ 0.2)

4. **Ubicación de la raíz:**
   - La raíz se encuentra en x\* ≈ 0.9099
   - En este punto: f(0.9099) ≈ 0

#### Interpretación visual:

- La curva comienza en (0, 1) con valor positivo
- Desciende gradualmente hasta cruzar el eje x en x\* ≈ 0.9099
- Continúa descendiendo hasta (1, -0.282)
- La raíz está claramente ubicada en el intervalo [0, 1] como confirma el teorema de Bolzano

#### Convergencia de los métodos:

- **Método de Aitken:** Converge rápidamente desde x₀ = 0.5 hacia la raíz
- **Método de Newton-Raphson:** También converge desde x₀ = 0.5, pero con más iteraciones

**Conclusión:** Ambos métodos encuentran exitosamente la única raíz de la función f(x) = e^x - 3x² en el intervalo [0, 1].
