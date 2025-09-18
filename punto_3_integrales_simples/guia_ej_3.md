# Punto 3 — Integración numérica de $I=\int_0^1 \sqrt{2}\,e^{x^2}\,dx$

**Integrando:** $f(x)=\sqrt{2}\,e^{x^2}$ en $[0,1]$  
**Objetivo:** aproximar $I$ con Trapecio y Simpson (y, si querés, comparar con un valor de referencia).

---

## 1) Identificación rápida
- $f$ es **continua** en $[0,1]$ ⇒ métodos numéricos aplican.  
- La primitiva de $e^{x^2}$ **no** es elemental. Puede escribirse con la función especial **erfi**:
$$
I = \sqrt{\tfrac{\pi}{2}}\,\mathrm{erfi}(1),\qquad
\mathrm{erfi}(x)=\frac{2}{\sqrt{\pi}}\int_0^x e^{t^2}\,dt.
$$

---

## 2) Métodos y fórmulas (lo justo y necesario)
**Trapecio (compuesto)**, paso $h=\tfrac{b-a}{n}$:
$$
T_n=h\Big[\tfrac12 f(a)+\sum_{i=1}^{n-1} f(a+ih)+\tfrac12 f(b)\Big],\quad \text{orden }O(h^2).
$$

**Simpson 1/3 (compuesto)**, $n$ **par**:
$$
S_n=\frac{h}{3}\Big[f(a)+f(b)+4\sum_{i\,\text{impar}} f(a+ih)+2\sum_{i\,\text{par}} f(a+ih)\Big],\quad \text{orden }O(h^4).
$$

---

## 3) Cálculo (valores numéricos)
- Trapecio $n=4$: $T_4=2.108138263357$  
- Trapecio $n=10$: $T_{10}=2.074898348842$  
- Simpson $n=4$ (par): $S_4=2.069999608814$

**Referencia “exacta” (con erfi):** $I\approx 2.068501936091$

**Errores absolutos (vs. referencia):**
- $|T_4-I|=0.039636327266$  
- $|T_{10}-I|=0.006396412751$  
- $|S_4-I|=0.001497672723$

> Se observa que al disminuir $h$ mejora Trapecio (orden $O(h^2)$) y que Simpson es más preciso a igual $n$ (orden $O(h^4)$).

---

## 4) Conclusión (cómo cerrarlo en el examen)
Con **Simpson 1/3** y $n=4$:
$$
\boxed{I\approx 2.069999608814}
$$
(preciso a $\sim 0.001497672723$ del valor de referencia).  
Válido por continuidad de $f$ y el orden de error del método.

---

## 5) ¿Qué es $\mathrm{erfi}$? (muy breve)
- Se llama **función error imaginaria**. Se define por
$$
\mathrm{erfi}(x)=\frac{2}{\sqrt{\pi}}\int_0^x e^{t^2}\,dt
$$
  y está relacionada con la función error usual por $\mathrm{erfi}(x)=-i\,\mathrm{erf}(ix)$.
- Sirve para escribir integrales de $e^{t^2}$ (que no tienen primitiva elemental).  
- Derivada: $\dfrac{d}{dx}\,\mathrm{erfi}(x)=\tfrac{2}{\sqrt{\pi}}e^{x^2}$.

---

## 6) Código de ejemplo (usa **tus** funciones `trapezoidal` y `simpson13`)
```python
import math
from parcial1_resuelto import trapezoidal, simpson13

f = lambda x: math.sqrt(2.0) * math.exp(x*x)
a, b = 0.0, 1.0

print('Trapecio n=4 :',  trapezoidal(f, a, b, 4))
print('Trapecio n=10:', trapezoidal(f, a, b, 10))
print('Simpson n=4  :',  simpson13(f, a, b, 4))  # n debe ser par
```
