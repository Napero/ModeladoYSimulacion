### b) Justificación teórica y verificación empírica de la ley 1/√n

**Objetivo:** Mostrar que el error (medido como error estándar del estimador Monte Carlo) decrece como 1/√n y que para reducirlo a la mitad necesitamos cuadruplicar el tamaño de muestra.

---

#### 1. Modelo probabilístico

Sea \( (X_i,Y_i) \) ~ Uniforme independiente en el rectángulo y \(F_i = f(X_i,Y_i)\).
El estimador Monte Carlo de la integral (área = 1) es:
\[
\hat I_n = \frac{1}{n}\sum_{i=1}^{n} F_i
\]

Con:
\[
\mathbb{E}[\hat I_n] = \mathbb{E}[F_i] = I,\qquad
\mathrm{Var}(\hat I_n)=\frac{\mathrm{Var}(F_i)}{n}=\frac{\sigma^{2}}{n}
\]

El **error estándar** (desviación típica del estimador):
\[
\mathrm{SE}(\hat I_n)=\frac{\sigma}{\sqrt{n}}
\]

Esto prueba la relación inversa con \(\sqrt{n}\).

---

#### 2. ¿Cómo reducir el error a la mitad?

Queremos:
\[
\frac{\sigma}{\sqrt{n'}} = \frac{1}{2}\frac{\sigma}{\sqrt{n}}
\;\Longrightarrow\;
\sqrt{n'} = 2\sqrt{n}
\;\Longrightarrow\;
n' = 4n
\]

Conclusión: **Para dividir el error estándar por 2, se debe cuadruplicar el tamaño de la muestra.**

---

#### 3. Verificación numérica (ejemplo reproducible)

````python
import numpy as np

def mc_integral(n, seed=0):
    rng = np.random.default_rng(seed)
    xs = rng.uniform(0, 1, n)
    ys = rng.uniform(1, 2, n)
    vals = np.exp(2*xs - ys)
    mean = vals.mean()
    std  = vals.std(ddof=1)
    se   = std / n**0.5
    return mean, std, se

N1 = 10_000
N2 = 4 * N1  # 40_000

m1, std1, se1 = mc_integral(N1, seed=0)
m2, std2, se2 = mc_integral(N2, seed=1)  # semilla distinta para independencia

print(f"N1={N1}  SE1={se1:.6f}")
print(f"N2={N2}  SE2={se2:.6f}")
print(f"Razón SE1/SE2 = {se1/se2:.3f}  (≈ 2 esperado)")