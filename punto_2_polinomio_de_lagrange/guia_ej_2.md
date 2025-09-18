# Punto 2 — Interpolación (grado 2) y derivada

**Función:** $f(x)=\ln(x+1)$  
**Nodos:** $x_0=0,\; x_1=1,\; x_2=2$

---

## 1) Armá la tabla de valores
Calculá $y_i=f(x_i)$:
- $y_0=\ln(1)=0$
- $y_1=\ln(2)\approx 0.6931471806$
- $y_2=\ln(3)\approx 1.0986122887$

> Con estos tres puntos ya podés construir el polinomio de grado 2.

---

## 2) Polinomio de Lagrange $P_2(x)$
Bases de Lagrange:
\[
\begin{aligned}
L_0(x)&=\frac{(x-1)(x-2)}{(0-1)(0-2)}=\frac{(x-1)(x-2)}{2},\\[4pt]
L_1(x)&=\frac{(x-0)(x-2)}{(1-0)(1-2)}=-\,x(x-2),\\[4pt]
L_2(x)&=\frac{(x-0)(x-1)}{(2-0)(2-1)}=\frac{x(x-1)}{2}.
\end{aligned}
\]
Entonces:
\[
P_2(x)=y_0\,L_0(x)+y_1\,L_1(x)+y_2\,L_2(x).
\]

---

## 3) Evaluá en $x=0.45$
- $P_2(0.45)\approx 0.3475168877$
- $f(0.45)=\ln(1.45)\approx 0.3715635564$
- **Error local:** $|f(0.45)-P_2(0.45)|\approx 0.0240466687$

### (Opcional) Cota de error teórica
Para grado 2:
\[
|R_2(x)|\le \frac{\max|f^{(3)}(\xi)|}{3!}\,\big| (x-0)(x-1)(x-2) \big|.
\]
Como $f^{(3)}(x)=\dfrac{2}{(x+1)^3}$, en $[0,2]$ el máximo es $2$.  
En $x=0.45$: $|R_2(0.45)|\le \dfrac{2}{6}\cdot|0.45\,(0.45-1)\,(0.45-2)|\approx 0.127875$.

---

## 4) Derivada en $x=1.5$ por diferencia central (usando $P_2$)
Usá $h=0.5$:
\[
P_2'(1.5)\approx \frac{P_2(1.5+h)-P_2(1.5-h)}{2h}
=\frac{P_2(2)-P_2(1)}{1}=\ln 3-\ln 2\approx 0.4054651081.
\]
Compará con la derivada real: $f'(x)=\dfrac{1}{x+1}\Rightarrow f'(1.5)=0.4$ (bastante cerca).

---

## Snippet de verificación (Python opcional)
```python
import math
y0, y1, y2 = 0.0, math.log(2.0), math.log(3.0)

def P2(x):
    L0 = ((x-1)*(x-2))/2.0
    L1 = -x*(x-2)
    L2 = (x*(x-1))/2.0
    return y0*L0 + y1*L1 + y2*L2

x = 0.45
print(P2(x))           # ~0.3475168877
print(math.log(1+x))   # ~0.3715635564

# Derivada central en 1.5 con h=0.5 usando P2
deriv = (P2(2.0) - P2(1.0)) / 1.0
print(deriv)           # ~0.4054651081
```

---

## Cómo repetir con cualquier función/nodos (checklist rápido)
1. Elegí nodos $x_0,\dots,x_n$ y calculá $y_i=f(x_i)$.  
2. Armá $L_i(x)=\prod_{j\ne i}\dfrac{x-x_j}{x_i-x_j}$.  
3. Construí $P_n(x)=\sum_i y_i L_i(x)$.  
4. Evaluá $P_n$ donde pidan.  
5. Si piden derivada: diferencia central con $P_n$ (elegí $h$ razonable).  
6. Cerrá con error (real o cota).
