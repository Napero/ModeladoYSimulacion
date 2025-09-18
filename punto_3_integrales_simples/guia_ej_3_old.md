# Punto 3 — Integración numérica de $I = \int_0^1 \sqrt{2}\,e^{x^2}\,dx$

**Integrando correcto:** $f(x)=\sqrt{2}\,e^{x^2}$ en $[0,1]$.

---

## 1) Observación clave y valor exacto (función especial)
La primitiva de $e^{x^2}$ **no** es elemental. El valor exacto puede expresarse con la función especial `erfi`:
$$
I = \sqrt{\tfrac{\pi}{2}}\,\mathrm{erfi}(1),\qquad \mathrm{erfi}(x)=\frac{2}{\sqrt{\pi}}\int_0^x e^{t^2}\,dt.
$$
Numéricamente,
$$
I = \sqrt{\tfrac{\pi}{2}}\,\mathrm{erfi}(1) \;\approx\; 2.068501936091.
$$

---

## 2) Trapecio (compuesto)
- Con $n=4$: $T_4 = 2.108138263357$  \\
  Error $|T_4 - I| = 0.039636327267$
- Con $n=10$: $T_{10} = 2.074898348842$  \\
  Error $|T_{10} - I| = 0.006396412751$

> Orden global: $O(h^2)$.

---

## 3) Simpson 1/3 (compuesto)
- Con $n=4$ (par): $S_4 = 2.069999608814$  \\
  Error $|S_4 - I| = 0.001497672723$

> Orden global: $O(h^4)$.

---

## 4) Código de ejemplo (con tus funciones actuales)
Usando el archivo `parcial1_resuelto.py` (define `trapezoidal` y `simpson13`):

```python
import math
from parcial1_resuelto import trapezoidal, simpson13

f = lambda x: math.sqrt(2.0) * math.exp(x*x)
a, b = 0.0, 1.0

print('Trapecio n=4 :',  trapezoidal(f, a, b, 4))
print('Trapecio n=10:', trapezoidal(f, a, b, 10))
print('Simpson n=4  :',  simpson13(f, a, b, 4))  # n debe ser par
```

> Si querés la forma cerrada en Python, y tenés `mpmath`: `I = math.sqrt(math.pi/2) * mp.erfi(1)`.

---

## 5) Qué escribir en el examen (resumen)
- La primitiva no es elemental; dar resultado numérico por **Trapecio**/**Simpson**.  
- Mostrar $n$, $h$, y el valor aproximado.  
- (Opcional) Mencionar $I=\sqrt{\pi/2}\,\mathrm{erfi}(1)$.
