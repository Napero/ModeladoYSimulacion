# Ejercicio 4 — Integral doble por Monte Carlo y verificación estadística

Integral a estimar:
\[
I=\int_{0}^{1}\int_{1}^{2} e^{\,2x-y}\;dy\,dx
\]

## a) Solución analítica (pasos)
1. Integrar respecto de y:
\[
\int_{1}^{2} e^{2x-y} dy = e^{2x}\int_{1}^{2} e^{-y}dy = e^{2x}\big[-e^{-y}\big]_{1}^{2}=e^{2x}(e^{-1}-e^{-2})
\]
2. Integrar respecto de x:
\[
I=(e^{-1}-e^{-2})\int_{0}^{1} e^{2x}dx=(e^{-1}-e^{-2})\left[\frac{e^{2x}}{2}\right]_0^{1}=(e^{-1}-e^{-2})\frac{e^{2}-1}{2}
\]
3. Valor numérico:
\[
I \approx 0.742868647\; (\text{redondeado})
\]

## b) Monte Carlo (método del promedio)
Dominio rectangular: x ∈ [0,1], y ∈ [1,2]; área = 1.  
Generar N puntos (x_i,y_i) ~ Uniformes independientes y estimar:
\[
\hat I_N = \frac{1}{N}\sum_{i=1}^N f(x_i,y_i),\quad f(x,y)=e^{2x-y}
\]

Parámetros usados:
- Semilla: np.random.seed(0)
- N = 10000

Ejemplo (lo podés correr aparte o en un script mínimo):
````python
import numpy as np, math
np.random.seed(0)
N = 10000
xs = np.random.uniform(0,1,N)
ys = np.random.uniform(1,2,N)
vals = np.exp(2*xs - ys)
I_mc = vals.mean()  # área=1, así que solo el promedio
var_muestral = vals.var(ddof=1)
std = var_muestral**0.5
stderr = std / N**0.5
z95 = 1.96
ci95 = (I_mc - z95*stderr, I_mc + z95*stderr)
print(I_mc, var_muestral, std, stderr, ci95)