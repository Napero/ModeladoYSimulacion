# Punto 2 - Polinomio de Lagrange

## Enunciado del ejercicio

**2. Dada la siguiente función f(x) = Ln(x + 1), y los nodos: x₀ = 0, x₁ = 1, x₂ = 2,**

**a) Construya un polinomio interpolante de Lagrange que le permita aproximar la función; grafique tanto la curva como el polinomio interpolante resaltando donde son próximos. Calcule el error local para ξ = 0.45, y la cota de error global.**

**b) Dada la tabla que se construye con los datos discretos que proporciona la función reconstruida, es decir tomando en cuenta sus nodos interpole el valor de la derivada f'(1.5) usando diferencias finitas centrales.**

## Datos del problema

- **Función:** f(x) = ln(x + 1)
- **Nodos:** x₀ = 0, x₁ = 1, x₂ = 2
- **Valores de la función:**
  - f(0) = ln(0 + 1) = ln(1) = 0
  - f(1) = ln(1 + 1) = ln(2) ≈ 0.6931
  - f(2) = ln(2 + 1) = ln(3) ≈ 1.0986

## Parte a) - Polinomio Interpolante de Lagrange

### 1. Construcción del polinomio

Para n = 2 (3 nodos), el polinomio de Lagrange es:

$P_2(x) = \sum_{i=0}^{2} f(x_i) \cdot L_i(x)$

Donde los polinomios base de Lagrange son:

$L_0(x) = \frac{(x-x_1)(x-x_2)}{(x_0-x_1)(x_0-x_2)} = \frac{(x-1)(x-2)}{(0-1)(0-2)} = \frac{(x-1)(x-2)}{2}$

$L_1(x) = \frac{(x-x_0)(x-x_2)}{(x_1-x_0)(x_1-x_2)} = \frac{(x-0)(x-2)}{(1-0)(1-2)} = \frac{x(x-2)}{-1} = -x(x-2)$

$L_2(x) = \frac{(x-x_0)(x-x_1)}{(x_2-x_0)(x_2-x_1)} = \frac{(x-0)(x-1)}{(2-0)(2-1)} = \frac{x(x-1)}{2}$

### 2. Desarrollo del polinomio

$P_2(x) = f(0) \cdot L_0(x) + f(1) \cdot L_1(x) + f(2) \cdot L_2(x)$

$P_2(x) = 0 \cdot \frac{(x-1)(x-2)}{2} + 0.6931 \cdot (-x(x-2)) + 1.0986 \cdot \frac{x(x-1)}{2}$

$P_2(x) = -0.6931x(x-2) + 0.5493x(x-1)$

$P_2(x) = -0.6931x^2 + 1.3862x + 0.5493x^2 - 0.5493x$

$P_2(x) = -0.1438x^2 + 0.8369x$

### 3. Verificación en los nodos

- P₂(0) = -0.1438(0)² + 0.8369(0) = 0 ✓
- P₂(1) = -0.1438(1)² + 0.8369(1) = 0.6931 ✓
- P₂(2) = -0.1438(2)² + 0.8369(2) = 1.0986 ✓

### 4. Error local para ξ = 0.45

**Fórmula del error:**
$E(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!} \prod_{i=0}^{n} (x-x_i)$

Para n = 2:
$E(x) = \frac{f'''(ξ)}{3!} (x-0)(x-1)(x-2)$

**Cálculo de f'''(x):**

- f(x) = ln(x + 1)
- f'(x) = 1/(x + 1)
- f''(x) = -1/(x + 1)²
- f'''(x) = 2/(x + 1)³

**Error en ξ = 0.45:**
$E(0.45) = \frac{2/(0.45+1)^3}{6} \cdot (0.45-0)(0.45-1)(0.45-2)$

$E(0.45) = \frac{2/1.45^3}{6} \cdot (0.45)(-0.55)(-1.55)$

$E(0.45) = \frac{2/3.0486}{6} \cdot 0.3836$

$E(0.45) = \frac{0.6563}{6} \cdot 0.3836 = 0.0420$

### 5. Cota de error global

**Cota del error:**
$|E(x)| \leq \frac{M_{n+1}}{(n+1)!} \max_{x \in [0,2]} \left| \prod_{i=0}^{n} (x-x_i) \right|$

Donde $M_{n+1} = \max_{x \in [0,2]} |f'''(x)| = \max_{x \in [0,2]} \left| \frac{2}{(x+1)^3} \right|$

En [0,2]: $M_3 = \frac{2}{(0+1)^3} = 2$

$\max_{x \in [0,2]} |x(x-1)(x-2)| = \max_{x \in [0,2]} |x^3 - 3x^2 + 2x|$

Evaluando en los puntos críticos:

- En x = 0: |0| = 0
- En x = 1: |1 - 3 + 2| = 0
- En x = 2: |8 - 12 + 4| = 0
- En x = 1/3: |1/27 - 1/3 + 2/3| = |1/27 + 1/3| = 10/27 ≈ 0.3704

**Cota de error global:**
$|E(x)| \leq \frac{2}{6} \cdot 0.3704 = 0.1235$

## Parte b) - Diferencias Finitas Centrales

### 1. Tabla de diferencias finitas

| x   | f(x)   | Δf     | Δ²f    |
| --- | ------ | ------ | ------ |
| 0   | 0.0000 | 0.6931 | 0.4055 |
| 1   | 0.6931 | 1.0986 | -      |
| 2   | 1.0986 | -      | -      |

### 2. Cálculo de f'(1.5) usando diferencias finitas centrales

**Fórmula de diferencias finitas centrales:**
$f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$

Para h = 0.5 y x = 1.5:
$f'(1.5) \approx \frac{f(2) - f(1)}{2 \cdot 0.5} = \frac{f(2) - f(1)}{1}$

**Valores necesarios:**

- f(1) = ln(2) ≈ 0.6931
- f(2) = ln(3) ≈ 1.0986

**Cálculo:**
$f'(1.5) \approx \frac{1.0986 - 0.6931}{1} = 0.4055$

### 3. Verificación analítica

**Valor exacto:**
f'(x) = 1/(x + 1)
f'(1.5) = 1/(1.5 + 1) = 1/2.5 = 0.4

**Error de aproximación:**
|Error| = |0.4055 - 0.4| = 0.0055

## Conclusiones

1. **Polinomio de Lagrange:** P₂(x) = -0.1438x² + 0.8369x
2. **Error local en ξ = 0.45:** 0.0420
3. **Cota de error global:** 0.1235
4. **Aproximación de f'(1.5):** 0.4055 (error: 0.0055)
