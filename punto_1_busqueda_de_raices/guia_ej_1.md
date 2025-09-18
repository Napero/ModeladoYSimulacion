# Punto 1 — Encontrar la raíz de $f(x)=e^{x}-3x^{2}$ en $(0,1)$

Guía corta, clara y replicable para parciales. Lista para pegar en Notion o cualquier editor con KaTeX.

---

## Paso 0 — Qué tengo que hacer
1) Ver si **hay** una raíz en el intervalo.  
2) **Aproximarla** con un método (te doy dos: **Punto Fijo** y **Newton**).  
3) **Validar** que el resultado tenga sentido.

---

## Paso 1 — ¿Existe una raíz? (test rápido)
1. Calculá los extremos:  
   $f(0)=e^{0}-0=1$ → **positivo**  
   $f(1)=e-3\approx -0.28$ → **negativo**
2. Si hay **signos opuestos**, por Bolzano **hay** una raíz adentro de $(0,1)$.

---

## Opción A — Punto Fijo (con Aitken) → simple y estable
**Idea:** escribir $e^{x}-3x^{2}=0$ como  
$x=\sqrt{\dfrac{e^{x}}{3}} \;\Rightarrow\; g(x)=\sqrt{\dfrac{e^{x}}{3}}$.

**Cómo hacerlo**
1. Semilla: $x_0=0.5$.  
2. Iterá:  
   $x_1=g(x_0),\; x_2=g(x_1)$  
   **Aitken:** $\hat x = x_0 - \dfrac{(x_1-x_0)^2}{\,x_2-2x_1+x_0\,}$
3. Repetí usando $\hat x$ como nuevo $x_0$.  
4. **Cortá** cuando $|x_{\text{nuevo}}-x_{\text{viejo}}|<10^{-8}$.

**Mini-ejemplo (valores reales)**  
$0.5 \to 0.898210\dots \to 0.909994\dots \to 0.910007572\dots$ ✅

**Resultado:** $x^{*} \approx 0.9100075725$

---

## Opción B — Newton–Raphson → el más rápido
**Fórmula:** $x_{k+1}=x_k-\dfrac{f(x_k)}{f'(x_k)}$ con  
$f(x)=e^{x}-3x^{2}$, $f'(x)=e^{x}-6x$.

**Cómo hacerlo**
1. Semilla $x_0=0.5$.  
2. Iterá hasta $|x_{k+1}-x_k|<10^{-8}$.

**Mini-ejemplo (valores reales)**  
$0.5 \to 1.16509 \to 0.93623 \to 0.910397 \to 0.91000766 \to 0.9100075725$ ✅

**Resultado:** $x^{*} \approx 0.9100075725$

---

## Paso 3 — Validación rápida
- **Residuo:** $|f(x^{*})|=|e^{x^{*}}-3(x^{*})^{2}|$ debe ser **muy chico** (≈0).  
  Con $x^{*}=0.9100075725$ da $\sim 10^{-16}$. ✔

---

## Copiar y pegar (Python opcional)

**Punto Fijo + Aitken**
```python
import math
g = lambda x: math.sqrt(math.exp(x)/3)

def aitken_step(x):
    x1 = g(x); x2 = g(x1)
    den = x2 - 2*x1 + x
    return x2 if den == 0 else x - (x1 - x)**2/den

x = 0.5
while True:
    x_new = aitken_step(x)
    if abs(x_new - x) < 1e-8: break
    x = x_new
print(x)  # ~0.9100075725
```

**Newton**
```python
import math
f  = lambda x: math.exp(x) - 3*x*x
df = lambda x: math.exp(x) - 6*x

x = 0.5
while True:
    x_new = x - f(x)/df(x)
    if abs(x_new - x) < 1e-8: break
    x = x_new
print(x)  # ~0.9100075725
```

---

### Nota KaTeX
- Usá `$...$` o `$$...$$` para fórmulas.  
- Evitá escribir `\*` dentro de las fórmulas. Si necesitás un “asterisco” en superíndice, usá `$x^{*}$`.
