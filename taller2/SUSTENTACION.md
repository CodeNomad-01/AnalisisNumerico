# Sustentación del Taller 2 — Análisis Numérico

Este documento es un **guion de exposición** del notebook `Taller_2.ipynb`. Cada sección muestra el fragmento de código tal cual aparece en el cuaderno, y debajo el texto que se puede leer o parafrasear durante la sustentación.

---

## Cómo está organizado el taller

Antes de entrar en cada ejercicio, vale la pena ubicar el contexto general:

- **Ejercicio 1 — Platija:** longitud vs peso. Se interpola y se ajusta una ley de potencia.
- **Ejercicio 2 — Salto vertical:** se simula con Euler y RK4 y se compara con la altura exacta.
- **Ejercicio 3 — Cangrejo violinista:** crecimiento alométrico en dos fases (joven/maduro).
- **Ejercicio 4 — Lotka-Volterra:** dinámica de compradores y vendedores con cuatro juegos de parámetros.

Los archivos auxiliares (`modelos.py`, `Ceros.py`, `ecuaciones.py`, `sel.py`) contienen las **funciones de los métodos numéricos**: el notebook solo las llama con los datos del problema.

---

## Bloque inicial: imports

```python
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

import sel as s
import modelos as ml
import Ceros as c
import ecuaciones as ec
import SerieT as st
```

> "Lo primero es importar las herramientas. `numpy` para arreglos y matemáticas vectorizadas, `sympy` para trabajar con símbolos cuando necesitamos un polinomio en forma cerrada o derivadas exactas, y `matplotlib` para todas las gráficas. Después importamos nuestros propios módulos: `modelos` tiene los ajustes (Lagrange, mínimos cuadrados, R²), `Ceros` tiene los métodos para encontrar raíces (bisección), `ecuaciones` tiene los integradores de EDO (Euler y RK4), y `sel` tiene los métodos de sistemas lineales. Cada vez que veamos `ml.`, `c.` o `ec.` en el código, es porque estamos llamando a una función de esos módulos."

---

# Ejercicio 1 — Platija: longitud vs peso

**Idea general:** Tenemos 27 mediciones de longitud y peso de una platija americana. Queremos primero ver los datos, luego ajustar dos modelos distintos (uno que pase por todos los puntos y otro que capture la tendencia), y estimar el peso para una longitud de 60 cm.

---

## Datos iniciales

```python
L_data = np.array([23.5, 24.5, 25.5, 26.5, 27.5, 28.5, 29.5, 30.5, 31.5, 32.5,
                   33.5, 34.5, 35.5, 36.5, 37.5, 38.5, 39.5, 40.5, 41.5, 42.5,
                   43.5, 44.5, 45.5, 46.5, 47.5, 48.5, 49.5])

w_data = np.array([124, 146, 155, 174, 190, 213, 236, 259, 284, 308,
                   332, 363, 391, 419, 455, 500, 538, 574, 623, 674,
                   724, 808, 812, 909, 1039, 1124, 1163])
```

> "Cargamos los 27 puntos como dos arreglos de NumPy. `L_data` son las longitudes en centímetros, desde 23.5 hasta 49.5, y `w_data` son los pesos en gramos correspondientes a cada longitud. Esto es lo único que tenemos como información: a partir de aquí, todos los modelos van a salir de estos números."

---

## 1-a) Gráfico de los datos

```python
plt.figure(figsize=(8, 5))
plt.plot(L_data, w_data, 'or', label='Datos observados')
plt.title('Longitud vs peso de la Platija')
plt.xlabel('Longitud (cm)')
plt.ylabel('Peso (g)')
plt.grid(True)
plt.legend()
plt.show()
```

> "Antes de calcular nada graficamos. Esto sirve para confirmar dos cosas: que no hay errores tipográficos en los datos (algún punto fuera de orden), y que la relación entre longitud y peso no es una recta sino una curva creciente. Esa primera mirada visual nos orienta hacia qué tipo de modelo probar después."

---

## 1-b) Polinomio de Lagrange (pasa por todos los puntos)

```python
x_sym = sp.symbols('x')
P_lagrange = ml.lagrange(L_data, w_data)
P_func = sp.lambdify(x_sym, P_lagrange)

w_60_poli = float(P_func(60))
print(f"Aproximacion del peso para L = 60 cm: w(60) = {w_60_poli}")
```

**Salida:**

```
Aproximacion del peso para L = 60 cm: w(60) = -4215794534925375.0
```

> "Aquí construimos un polinomio que **pasa exactamente** por los 27 puntos. La función `ml.lagrange` arma el polinomio interpolante de Lagrange usando SymPy, devolviendo una expresión simbólica. Como esa expresión es simbólica, no se puede evaluar directamente como una función numérica: por eso `sp.lambdify` la convierte en una función Python que sí podemos llamar con un número.
>
> Después la evaluamos en `L = 60`, que es la longitud que pide el enunciado y que **está fuera** del rango medido. El resultado: `w(60) ≈ -4.22 × 10¹⁵ g`. Es decir, un peso **negativo y absurdamente grande**. Eso es el **fenómeno de Runge**: un polinomio de grado alto puede ajustar perfecto los datos pero se vuelve completamente inestable fuera del intervalo. Conclusión del ítem b: el polinomio de Lagrange **no es coherente** como modelo predictivo."

---

## 1-c) Modelo de ajuste (mínimos cuadrados, ley de potencia)

### Paso 1: explorar transformaciones con `escalas`

```python
ml.escalas(L_data, w_data)
```

> "La función `ml.escalas` dibuja una rejilla de 9 sub-gráficas con los datos transformados de distintas maneras: `y²`, `1/y`, `√y`, `log y`, `x²`, `x³`, `log x` y `log x` vs `log y`. La pregunta que estamos haciendo con esto es muy simple: **¿con qué transformación los puntos se ven como una recta?**, porque una recta es lo más fácil de ajustar con mínimos cuadrados. Al mirar las 9 gráficas, la única donde la nube queda visiblemente alineada es la de `log L` vs `log w`. Eso es la pista."

### Paso 2: confirmar la elección con R²

```python
R_lineal  = ml.coeficiente_determinacion(L_data, w_data)
R_x3      = ml.coeficiente_determinacion(L_data**3, w_data)
R_loglog  = ml.coeficiente_determinacion(np.log(L_data), np.log(w_data))

print(f"R^2 (L, w)              : {R_lineal}")
print(f"R^2 (L^3, w)            : {R_x3}")
print(f"R^2 (log(L), log(w))    : {R_loglog}")
```

**Salida:**

```
R^2 (L, w)              : 0.9362218067143112
R^2 (L^3, w)            : 0.9918775506182635
R^2 (log(L), log(w))    : 0.9961836639396179
```

> "Para no quedarnos con la pura impresión visual, calculamos el coeficiente de determinación R² para tres ideas: la recta directa, la cúbica directa (`L³` vs `w`) y el log–log. R² mide qué tan bien una recta explica los datos: cuanto más cerca de 1, mejor.
>
> El resultado nos da: 0.9362 para la recta directa, 0.9919 para `L³` directa y **0.9962 para log–log**, que es el más alto. Con esto confirmamos con un número que el ajuste log–log es el mejor."

### Paso 3: ajustar la recta en escala log–log

```python
b_coef, log_a = ml.minimos_cuadrados(np.log(L_data), np.log(w_data))
a_coef = np.exp(log_a)

w_modelo = lambda L: a_coef * L**b_coef

w_60_ajuste = w_modelo(60)
print(f"Modelo: w(L) = {a_coef:.6f} * L^{b_coef:.6f}")
print(f"Aproximacion para L = 60 cm: w(60) = {w_60_ajuste:.4f} g")
```

**Salida:**

```
Modelo: w(L) = 0.010737 * L^2.952605
Aproximacion para L = 60 cm: w(60) = 1910.0935 g
```

> "Ahora ajustamos el modelo de potencia `w = a · L^b`. Como ese modelo **no es lineal** en `a` ni en `b`, tomamos logaritmo a los dos lados, y queda `ln w = b · ln L + ln a`, que **sí** es una recta: pendiente `b`, intercepto `ln a`.
>
> Por eso pasamos los datos transformados con `np.log` a `ml.minimos_cuadrados`. La función devuelve la pendiente y el intercepto en ese orden, así que el primer valor lo guardamos como `b_coef` (porque la pendiente en log–log **es** el exponente `b`), y el segundo como `log_a` (porque el intercepto es `ln a`).
>
> Para recuperar `a` aplicamos la inversa del logaritmo, que es la exponencial: `a_coef = np.exp(log_a)`. El exponente `b` no necesita ningún ajuste extra; la pendiente ya es directamente `b`.
>
> Con `a` y `b` definimos `w_modelo` como una función rápida con `lambda`. Cuando la evaluamos en `L = 60`, obtenemos `1910.09 g`. Ese valor es **coherente** con los datos, a diferencia del polinomio de Lagrange que daba `-10¹⁵`. Esa es la moraleja: para extrapolar conviene un modelo de tendencia, no uno que pase por todos los puntos."

**Justificación rápida del exponente:** `b ≈ 2.95` es biológicamente plausible. Si el pez creciera **manteniendo la forma** (crecimiento isométrico), el volumen escalaría como `L³`, y como la densidad es casi constante, el peso también escalaría como `L³`. Que `b` no sea exactamente 3 indica un crecimiento ligeramente alométrico.

---

## 1-d) Tres gráficas comparativas

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].plot(L_data, w_data, 'or'); axes[0].set_title('Datos observados')
L_plot_b = np.linspace(L_data.min(), 60, 400)
y_plot_b = np.array([float(P_func(Li)) for Li in L_plot_b])
axes[1].plot(L_data, w_data, 'or')
axes[1].plot(L_plot_b, y_plot_b, 'g-'); axes[1].set_title('Lagrange (1-b)')
axes[1].axvline(60, color='k', linestyle='--')
L_plot_c = np.linspace(L_data.min(), 60, 400)
axes[2].plot(L_data, w_data, 'or')
axes[2].plot(L_plot_c, w_modelo(L_plot_c), 'b-'); axes[2].set_title('Modelo potencia (1-c)')
axes[2].axvline(60, color='k', linestyle='--')
plt.tight_layout()
plt.show()
```

> "Mostramos los tres gráficos uno al lado del otro: solo los datos, los datos con el polinomio de Lagrange extrapolado hasta 60 cm, y los datos con la curva de potencia hasta 60 cm. La línea vertical punteada marca dónde estamos extrapolando.
>
> Visualmente queda clarísimo: el polinomio se dispara y se sale del marco, mientras que la curva de potencia sigue la nube de puntos de forma suave hasta el final. Es la traducción gráfica de lo que ya dijeron los números."

---

# Ejercicio 2 — Salto vertical de la bailarina

**Idea general:** La bailarina sale del suelo, sube por inercia y la gravedad la frena hasta caer. La ecuación es la segunda ley de Newton aplicada a una caída libre. Queremos simularla con Euler y RK4, compararla con la altura exacta `H = g·T²/8`, y analizar el error al refinar el paso.

---

## 2-a) Solución numérica con Euler y RK4

```python
g  = 32.2
T  = 1 / 3
v0 = g * T / 2


def salto(t, u):
    y = u[0]
    v = u[1]
    f1 = v
    f2 = -g
    return np.array([f1, f2])

u0 = np.array([0.0, v0])
h  = T / 10

t_e, sol_e = ec.Euler(salto, 0, T, h, u0)
t_r, sol_r = ec.Rk4  (salto, 0, T, h, u0)

sol_e = np.array(sol_e)
sol_r = np.array(sol_r)
y_e, v_e = sol_e[:, 0], sol_e[:, 1]
y_r, v_r = sol_r[:, 0], sol_r[:, 1]

print(f"Altura maxima Euler = {y_e.max():.6f}")
print(f"Altura maxima Rk4   = {y_r.max():.6f}")
```

**Salida:**

```
Altura maxima Euler = 0.536667
Altura maxima Rk4   = 0.504864
```

> "Definimos las constantes físicas: `g = 32.2 ft/s²` (gravedad en unidades inglesas, porque el enunciado da las medidas en pulgadas), `T = 1/3 s` (la duración total del salto) y la velocidad inicial `v0 = g·T/2`, que sale de las ecuaciones de tiro vertical: para que el salto dure exactamente `T`, hay que despegar con esa velocidad.
>
> La función `salto` es el sistema de EDOs. Como los métodos del curso solo trabajan con sistemas de primer orden, convertimos la ecuación de Newton en dos ecuaciones: definimos un vector de estado `u = [y, v]`, donde `y` es la altura y `v` la velocidad. Las derivadas son: la derivada de `y` es `v` (por definición), y la derivada de `v` es `-g` (la gravedad). Por eso devolvemos `[v, -g]`.
>
> Después fijamos la condición inicial `u0 = [0, v0]` (sale del suelo con velocidad `v0`) y un paso de tiempo `h = T/10`, que divide el intervalo en 10 pasos.
>
> Llamamos a `ec.Euler` y `ec.Rk4` con los mismos argumentos: la función, el tiempo inicial, el final, el paso y la condición inicial. Cada uno devuelve el arreglo de tiempos y la solución como lista de vectores de estado.
>
> Convertimos la solución a un arreglo de NumPy de dos columnas, y separamos: la primera columna son las alturas (`y_e`, `y_r`) y la segunda las velocidades (`v_e`, `v_r`).
>
> Finalmente imprimimos la altura máxima usando `.max()` sobre el arreglo de alturas: Euler da 0.5367 ft y RK4 da 0.5049 ft."

---

## 2-b) Comparación con la altura máxima exacta

```python
H_exacto = (g * T**2) * 1/8
H_e = y_e.max()
H_r = y_r.max()

print(f"H exacto = {H_exacto:.6f} ({H_exacto*12:.4f} pulgadas)")
print(f"H Euler  = {H_e:.6f}   error = {abs(H_e - H_exacto):.4e}")
print(f"H Rk4    = {H_r:.6f}   error = {abs(H_r - H_exacto):.4e}")
```

**Salida:**

```
H exacto = 0.447222 (5.3667 pulgadas)
H Euler  = 0.536667   error = 8.9444e-02
H Rk4    = 0.504864   error = 5.7642e-02
```

> "La fórmula `H = g·T²/8` no es magia: viene de la cinemática. La velocidad se hace cero en `t = T/2` (por simetría), y al sustituir eso en `y(t) = v0·t − (1/2)g t²` con `v0 = g·T/2`, queda `H = g·T²/8`. Con `g = 32.2` y `T = 1/3`, eso da 0.4472 ft, que en pulgadas (multiplicando por 12) son 5.37 pulgadas, coincidiendo con el `5.4 pulgadas` del enunciado.
>
> Calculamos el error como el valor absoluto de la diferencia entre cada altura numérica y la exacta. El `abs` es para que solo nos interese la magnitud del error, sin importar el signo.
>
> Los resultados: Euler queda con error 0.0894 y RK4 con error 0.0576. RK4 es más preciso que Euler con el mismo paso, lo cual confirma que es un método de orden superior. Además, ambos métodos **sobreestiman** la altura: el numérico va por encima del exacto."

---

## 2-c) Error con distintos pasos h

```python
print(f"{'n':>5} | {'h':>10} | {'Err Euler':>14} | {'Err Rk4':>14}")
print("-" * 55)

pasos = [5, 10, 20, 50, 100, 200]

for n in pasos:
    h_i = T / n
    _, se = ec.Euler(salto, 0, T, h_i, u0)
    _, sr = ec.Rk4  (salto, 0, T, h_i, u0)
    err_e = abs(np.array(se)[:, 0].max() - H_exacto)
    err_r = abs(np.array(sr)[:, 0].max() - H_exacto)
    print(f"{n:>5} | {h_i:>10.6f} | {err_e:>14.4e} | {err_r:>14.4e}")
```

**Salida:**

```
    n |          h |      Err Euler |        Err Rk4
-------------------------------------------------------
    5 |   0.066667 |     1.9678e-01 |     1.1568e-01
   10 |   0.033333 |     8.9444e-02 |     5.7642e-02
   20 |   0.016667 |     4.4722e-02 |     2.9318e-02
   50 |   0.006667 |     1.7889e-02 |     1.1846e-02
  100 |   0.003333 |     8.9444e-03 |     5.9431e-03
  200 |   0.001667 |     4.4722e-03 |     2.9765e-03
```

> "Las dos primeras líneas son la cabecera de la tabla; el formato `>14` significa 'alinea a la derecha en ancho 14'. Eso hace que la tabla quede bien alineada en consola.
>
> Definimos una lista con seis valores de `n` (5, 10, 20, 50, 100, 200), que son los números de pasos en que vamos a dividir el intervalo. Elegimos varios que se duplican entre sí (5→10, 10→20, 50→100, 100→200) para verificar la regla teórica: si Euler es `O(h)`, al duplicar `n` el error debería caer aproximadamente a la mitad.
>
> Dentro del bucle, para cada `n` calculamos el paso `h_i = T/n`, simulamos con Euler y con RK4, sacamos la altura máxima de cada uno (`np.array(se)[:, 0].max()` selecciona la primera columna —las alturas— y toma el máximo), y calculamos el error contra la altura exacta. Usamos `_` para descartar el arreglo de tiempos, ya que no lo usamos aquí.
>
> **Lo importante de la tabla:** mirando la columna de Euler, cada vez que `n` se duplica, el error se reduce aproximadamente a la mitad: 0.197 → 0.0894 → 0.0447 → ... Eso confirma que Euler es un método de orden 1: el error es proporcional a `h`. RK4 también baja, pero parte de errores ya más pequeños desde el principio, lo que confirma que es un método de orden superior."

---

## 2-d) Gráficas tiempo vs altura y tiempo vs velocidad

```python
t_dense = np.linspace(0, T, 400)
y_exacto = v0*t_dense - 0.5*g*t_dense**2
v_exacto = v0 - g*t_dense

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(t_dense, y_exacto, 'k-', label='Exacta')
axes[0].plot(t_e, y_e, 'ob', label='Euler')
axes[0].plot(t_r, y_r, 'sr', label='RK4')
axes[0].set_title('Altura vs tiempo')
axes[0].grid(True); axes[0].legend()

axes[1].plot(t_dense, v_exacto, 'k-', label='Exacta')
axes[1].plot(t_e, v_e, 'ob', label='Euler')
axes[1].plot(t_r, v_r, 'sr', label='RK4')
axes[1].set_title('Velocidad vs tiempo')
axes[1].grid(True); axes[1].legend()
plt.tight_layout()
plt.show()
```

> "Para visualizar la calidad de los métodos, dibujamos dos paneles: altura vs tiempo y velocidad vs tiempo. La curva negra es la solución exacta evaluada en una malla fina, y los puntos son los valores que dieron Euler (azul) y RK4 (rojo) en sus tiempos discretos.
>
> En el panel de altura se ve la parábola del salto: sube, alcanza el pico, baja. En el de velocidad se ve cómo arranca positiva, llega a cero en el pico y se vuelve negativa al caer. Si los puntos numéricos están encima de la curva exacta, la simulación es buena. Esa es la verificación visual del análisis numérico que ya hicimos en 2-b y 2-c."

---

# Ejercicio 3 — Cangrejo violinista: cuerpo vs tenaza

**Idea general:** Tenemos 25 mediciones del peso del cuerpo y de la tenaza de cangrejos violinistas. La biología sugiere que el crecimiento de la tenaza **cambia de ritmo** al llegar a la madurez sexual, definida cuando cuerpo + tenaza superan 1100 mg. Queremos encontrar ese umbral, ajustar dos modelos (uno por fase) y predecir pesos para nuevos valores.

---

## Datos iniciales

```python
x_data = np.array([57.6, 80.3, 109.2, 156.1, 199.7, 283.3, 270.0, 300.2, 355.2, 420.1,
                   470.1, 535.7, 617.9, 680.6, 743.3, 872.4, 983.1, 1079.9, 1165.5,
                   1211.7, 1291.3, 1363.2, 1449.1, 1807.9, 2235.0])
y_data = np.array([5.3, 9.0, 13.7, 25.1, 38.3, 52.5, 59.0, 78.1, 104.5, 135.0,
                   164.9, 195.6, 243.0, 271.6, 319.2, 417.6, 460.8, 537.0, 593.8,
                   616.8, 670.0, 699.3, 777.8, 1009.1, 1380.0])

T_data = x_data + y_data
```

> "Cargamos los datos: `x_data` es el peso del cuerpo, `y_data` el peso de la tenaza, ambos en miligramos. La variable `T_data` es la suma, que representa el peso total del cangrejo. El criterio de madurez del enunciado dice que ocurre cuando ese total supera 1100 mg, y vamos a usarlo en el próximo paso."

---

## 3-a) Polinomio interpolante y umbral de madurez

```python
P_lagrange = ml.lagrange(x_data, y_data)
P_func = sp.lambdify(x_sym, P_lagrange)

f_madurez = lambda xv: xv + float(P_func(xv)) - 1100.0
x_madurez = c.Biseccion(f_madurez, 743.3, 872.4, 1e-4)
y_madurez = float(P_func(x_madurez))

print(f"Cuerpo en la madurez:  x* = {x_madurez:.4f} mg")
print(f"Tenaza en la madurez:  y* = {y_madurez:.4f} mg")
print(f"Total en la madurez:   T* = {x_madurez + y_madurez:.4f} mg")
```

**Salida:**

```
Cuerpo en la madurez:  x* = 871.1412 mg
Tenaza en la madurez:  y* = 228.8661 mg
Total en la madurez:   T* = 1100.0072 mg
```

> "Primero construimos el polinomio de Lagrange que pasa por todos los puntos (cuerpo vs tenaza). Igual que en 1-b, usamos SymPy para tener una expresión simbólica y `sp.lambdify` para poder evaluarla numéricamente.
>
> Ahora viene el truco interesante. Queremos encontrar el peso del cuerpo `x*` en el que la suma cuerpo + tenaza pasa los 1100 mg. Eso es equivalente a resolver la ecuación `x + P(x) − 1100 = 0`. Esa es justamente la función `f_madurez`: para cada `x`, devuelve cuánto le falta a la suma para llegar a 1100. Donde esa función vale cero, está nuestro `x*`.
>
> Para encontrar la raíz aplicamos **bisección**, que está en el módulo `Ceros` (importado como `c`). Bisección necesita un intervalo donde la función cambie de signo. Eligimos `[743.3, 872.4]` porque son dos datos consecutivos: en 743.3 el total es 1062.5 (menor a 1100) y en 872.4 el total es 1290 (mayor a 1100). Por el teorema del valor intermedio, sabemos que en algún punto entre esos dos `f_madurez` cruza el cero.
>
> El resultado: `x* = 871.14 mg`. La tenaza en ese punto vale `y* = 228.87 mg` y el total cuadra en `T* = 1100.007 mg`, prácticamente la frontera exacta. Este `x*` es lo que vamos a usar para separar las dos fases."

---

## 3-b) Modelo no lineal en dos fases

```python
cangrejo_joven  = T_data < 1100
cangrejo_maduro = T_data > 1100
x_joven,  y_joven  = x_data[cangrejo_joven],  y_data[cangrejo_joven]
x_maduro, y_maduro = x_data[cangrejo_maduro], y_data[cangrejo_maduro]

a_joven,  log_c_joven  = ml.minimos_cuadrados(np.log(x_joven),  np.log(y_joven))
a_maduro, log_c_maduro = ml.minimos_cuadrados(np.log(x_maduro), np.log(y_maduro))
c_joven  = np.exp(log_c_joven)
c_maduro = np.exp(log_c_maduro)
R2_joven  = ml.coeficiente_determinacion(np.log(x_joven),  np.log(y_joven))
R2_maduro = ml.coeficiente_determinacion(np.log(x_maduro), np.log(y_maduro))

modelo_joven  = lambda x: c_joven  * x**a_joven
modelo_maduro = lambda x: c_maduro * x**a_maduro

print(f"Modelo joven : y = {c_joven:.6f} * x^{a_joven:.6f}   (R^2 = {R2_joven:.6f})")
print(f"Modelo maduro: y = {c_maduro:.6f} * x^{a_maduro:.6f}   (R^2 = {R2_maduro:.6f})")
```

**Salida:**

```
Modelo joven : y = 0.006935 * x^1.625746   (R^2 = 0.996128)
Modelo maduro: y = 0.072752 * x^1.274184   (R^2 = 0.997207)
```

> "Aquí construimos **dos modelos de potencia separados**, uno para cada fase.
>
> Primero separamos los datos: `T_data < 1100` y `T_data > 1100` son **máscaras booleanas**, arreglos de Verdadero/Falso del mismo tamaño que `T_data`. Cuando los usamos para indexar `x_data` y `y_data`, NumPy se queda solo con los puntos donde la máscara es Verdadera. Así obtenemos los subconjuntos jóvenes y maduros.
>
> Para cada subconjunto aplicamos exactamente la misma lógica que en 1-c: pasamos a escala log–log, hacemos mínimos cuadrados, recuperamos el coeficiente con `np.exp`, y armamos el modelo `y = c · x^a`. La pendiente la guardamos como `a` (que es el exponente alométrico) y el intercepto como `log_c`.
>
> También calculamos R² para cada fase. Los dos R² son altísimos (0.9961 y 0.9972), lo que confirma que **dos curvas separadas se ajustan mucho mejor** que una sola al conjunto completo.
>
> Definimos `modelo_joven` y `modelo_maduro` como dos funciones lambda para poder usarlos después como predictores."

---

## 3-c) Crecimiento alométrico vs isométrico (solo texto)

> "Este ítem es solo conceptual; no hay código nuevo. La idea es que el exponente `a` en `y = c · x^a` nos dice cómo crece la tenaza respecto al cuerpo:
>
> - Si `a = 1`, el crecimiento es **isométrico**: cuerpo y tenaza crecen a la par, las proporciones se mantienen.
> - Si `a ≠ 1`, el crecimiento es **alométrico**: una parte gana o pierde proporción. Si `a > 1`, la tenaza crece más rápido que el cuerpo. Si `a < 1`, se queda atrás.
>
> En nuestro caso, como ambos exponentes salieron mayores que 1, el crecimiento es **alométrico positivo**: la tenaza crece proporcionalmente más rápido que el cuerpo en las dos fases."

---

## 3-d) Comparación de los exponentes por fase

```python
print(f"a_joven  = {a_joven:.4f}")
print(f"a_maduro = {a_maduro:.4f}")
```

**Salida:**

```
a_joven  = 1.6257
a_maduro = 1.2742
```

> "Aquí simplemente imprimimos los dos exponentes alométricos para tener la respuesta numérica. `a_joven = 1.6257` y `a_maduro = 1.2742`. Ambos son mayores que 1, lo que confirma alometría positiva en las dos fases; y `a_joven > a_maduro`, lo que nos dice que el efecto es **más fuerte en la juventud**. Biológicamente tiene sentido: el cangrejo joven invierte mucha energía en desarrollar la tenaza (para cortejo y defensa); al madurar, esa energía se redistribuye a reproducción y mantenimiento, y el crecimiento relativo de la tenaza se atenúa."

---

## 3-e) Etapa de mayor crecimiento proporcional

```python
print(f"Fase joven : a = {a_joven:.4f}")
print(f"Fase madura: a = {a_maduro:.4f}")
print("--> La tenaza crece proporcionalmente mas en la fase joven.")
```

**Salida:**

```
Fase joven : a = 1.6257
Fase madura: a = 1.2742
--> La tenaza crece proporcionalmente mas en la fase joven.
```

> "Es la pregunta directa del enunciado: ¿en qué etapa crece más la tenaza en proporción al cuerpo? Comparando los dos exponentes, `a_joven` (1.6257) es mayor que `a_maduro` (1.2742). Como el exponente `a` mide cuánto crece la tenaza por cada unidad que crece el cuerpo, la respuesta es directa: **la tenaza crece proporcionalmente más en la fase joven**."

---

## 3-f) Estimación de la tenaza para x = 500 y x = 2000

```python
def estimar_tenaza(x_cuerpo):
    if x_cuerpo < x_madurez:
        return "joven",  modelo_joven(x_cuerpo)
    return "madura", modelo_maduro(x_cuerpo)

pesos = [500.0, 2000.0]

for x_test in pesos:
    fase, y_pred = estimar_tenaza(x_test)
    print(f"Cuerpo x = {x_test:6.1f} mg -> fase {fase} | tenaza y = {y_pred:8.2f} mg")
```

**Salida:**

```
Cuerpo x =  500.0 mg -> fase joven | tenaza y =   169.38 mg
Cuerpo x = 2000.0 mg -> fase madura | tenaza y =  1169.40 mg
```

> "Definimos una pequeña función `estimar_tenaza` que decide qué modelo usar según el peso del cuerpo: si `x` es menor que `x_madurez` (los 871 mg que encontramos con bisección), usa el modelo joven; si no, usa el modelo maduro. Devuelve dos cosas: el nombre de la fase y la predicción.
>
> Aplicamos esa función a los dos pesos que pide el enunciado: 500 mg y 2000 mg.
>
> - Para `x = 500 mg`, como 500 < 871, cae en la fase **joven** → tenaza estimada = **169.38 mg**.
> - Para `x = 2000 mg`, como 2000 > 871, cae en la fase **madura** → tenaza estimada = **1169.40 mg**.
>
> Si hubiéramos usado un solo modelo (joven o maduro) para los dos casos, una de las dos predicciones quedaría mal. Es justamente por eso que dividir en dos fases es necesario."

---

## 3-g) Predicción para x = 3000 mg

```python
x_pred = 3000.0
y_pred_poli     = float(P_func(x_pred))
y_pred_dosfases = modelo_maduro(x_pred)

print(f"Polinomio de Lagrange = {y_pred_poli: .4e} mg")
print(f"Modelo de dos fases = {y_pred_dosfases: .4f} mg")
```

**Salida:**

```
Polinomio de Lagrange = -2.2311e+21 mg
Modelo de dos fases =  1960.3582 mg
```

> "Aquí comparamos los dos modelos del ejercicio 3 cuando los obligamos a extrapolar a `x = 3000 mg`, que está muy lejos del último dato (2235 mg).
>
> Evaluamos el polinomio de Lagrange (`P_func`) y el modelo de dos fases (en la rama madura, porque 3000 > 871).
>
> Los resultados son contundentes: el polinomio entrega un número **absurdo** del orden de `-2.23 × 10²¹` (negativo y descomunal: el fenómeno de Runge en su máxima expresión), mientras que el modelo de dos fases da `1960 mg`, un valor totalmente razonable.
>
> Es la misma moraleja del ejercicio 1: para predecir fuera del rango medido, conviene un modelo de **tendencia** y no uno que pase por todos los puntos."

---

# Ejercicio 4 — Lotka-Volterra: compradores y vendedores

**Idea general:** El modelo de Lotka-Volterra describe dos poblaciones que crecen, compiten entre sí y se limitan mutuamente. En este caso son **compradores `x`** y **vendedores `v`**, con condición inicial `x(0) = 75`, `v(0) = 20`. Como no hay solución cerrada, simulamos con Euler para distintos juegos de parámetros y vemos qué pasa.

El sistema general es:

```
x' = x · (a − b·x − m·v)
v' = v · (c − d·v − n·x)
```

donde:
- `a`, `c` son las tasas de crecimiento propias.
- `b`, `d` miden la competencia interna (cada grupo se estorba a sí mismo).
- `m`, `n` miden la interferencia cruzada entre los dos grupos.

---

## 4-a) Parámetros "suaves"

```python
def lotka_a(t, y):
    x, v = y[0], y[1]
    a, b, m_ = 0.3, 0.01, 0.06
    c_, d, n = 0.03, 0.009, 0.0055
    return np.array([x*(a  - b*x - m_*v),
                     v*(c_ - d*v - n*x)])

t, sol = ec.Euler(lotka_a, 0, 200, 0.05, np.array([75.0, 20.0]))
sol = np.array(sol)
x_t, v_t = sol[:, 0], sol[:, 1]

print(f"x(T) = {x_t[-1]:.4f}    v(T) = {v_t[-1]:.4f}")

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
axes[0].plot(t, x_t, 'b-'); axes[0].set_title('Compradores x(t)')
axes[1].plot(t, v_t, 'r-'); axes[1].set_title('Vendedores v(t)')
axes[2].plot(x_t, v_t, 'g-'); axes[2].set_title('Plano de fase x vs v')
plt.tight_layout()
plt.show()
```

**Salida:**

```
x(T) = 30.0000    v(T) = 0.0000
```

> "La función `lotka_a` define el sistema con los parámetros que da el enunciado. Notar que algunos nombres llevan guion bajo (`m_`, `c_`) para no chocar con el módulo `m` o variables reservadas.
>
> Llamamos a `ec.Euler` desde `t = 0` hasta `t = 200` con paso `0.05` (un poco fino, porque las dinámicas son lentas y queremos buena resolución) y arrancando con `[75, 20]`. La solución sale como una lista de pares `(x, v)`; la convertimos a arreglo y separamos en `x_t` y `v_t`.
>
> Imprimimos los valores finales para ver dónde quedó el sistema: `x(T) = 30, v(T) = 0`. Es decir, **los compradores se estabilizan en 30 y los vendedores se extinguen**.
>
> Las tres gráficas muestran: la curva temporal de cada población y el **plano de fase** (`x` vs `v`), que nos dice el camino conjunto del sistema. El plano de fase termina pegado al eje horizontal en `(30, 0)`, confirmando la extinción de los vendedores.
>
> Interpretación: aunque el enunciado dice que coexisten, con esos parámetros las ecuaciones no permiten coexistencia real (el punto de equilibrio con ambas poblaciones positivas no existe). Gana la población con mejor tasa de crecimiento propia."

---

## 4-b) b grande (mucha competencia entre compradores)

```python
def lotka_b(t, y):
    x, v = y[0], y[1]
    a, b, m_ = 0.26, 0.2, 0.06
    c_, d, n = 0.06, 0.01, 0.015
    return np.array([x*(a  - b*x - m_*v),
                     v*(c_ - d*v - n*x)])

t, sol = ec.Euler(lotka_b, 0, 200, 0.05, np.array([75.0, 20.0]))
sol = np.array(sol)
x_t, v_t = sol[:, 0], sol[:, 1]

print(f"x(T) = {x_t[-1]:.4f}    v(T) = {v_t[-1]:.4f}")
```

**Salida:**

```
x(T) = 0.0000    v(T) = 6.0000
```

> "El cambio importante respecto al caso anterior es que `b = 0.2`, mucho más alto. Eso significa que los compradores se **estorban mucho entre sí**: la propia competencia interna los frena.
>
> El resultado es el opuesto al ítem a: **los compradores se extinguen** (`x → 0`) y **los vendedores se estabilizan en 6**. Es decir, demasiada competencia interna hunde a una población y deja vivir a la otra. El plano de fase termina pegado al eje vertical en `(0, 6)`."

---

## 4-c) n muy grande (compradores aplastan vendedores)

```python
def lotka_c(t, y):
    x, v = y[0], y[1]
    a, b, m_ = 0.26, 0.02, 0.06
    c_, d, n = 0.26, 0.9, 4.2
    return np.array([x*(a  - b*x - m_*v),
                     v*(c_ - d*v - n*x)])

t, sol = ec.Euler(lotka_c, 0, 50, 0.001, np.array([75.0, 20.0]))
sol = np.array(sol)
x_t, v_t = sol[:, 0], sol[:, 1]

print(f"x(T) = {x_t[-1]:.4f}    v(T) = {v_t[-1]:.4f}")
```

**Salida:**

```
x(T) = 13.0000    v(T) = 0.0000
```

> "Aquí `n = 4.2` es enorme: cada comprador frena fortísimo a los vendedores. Para evitar que Euler se vaya a infinito por una caída brusca, **bajamos el paso a `h = 0.001`** y acortamos el intervalo a 50 unidades de tiempo, suficiente para ver el equilibrio.
>
> El resultado: los **vendedores colapsan rápidamente** y los **compradores se estabilizan en 13**. El plano de fase muestra una caída casi vertical de `v` y luego una estabilización horizontal de `x`."

---

## 4-d) Parámetros con equilibrio inestable

```python
def lotka_d(t, y):
    x, v = y[0], y[1]
    a, b, m_ = 0.26, 0.021, 0.06
    c_, d, n = 0.06, 0.01, 0.01
    return np.array([x*(a  - b*x - m_*v),
                     v*(c_ - d*v - n*x)])

t, sol = ec.Euler(lotka_d, 0, 500, 0.1, np.array([75.0, 20.0]))
sol = np.array(sol)
x_t, v_t = sol[:, 0], sol[:, 1]

print(f"x(T) = {x_t[-1]:.4f}    v(T) = {v_t[-1]:.4f}")
```

**Salida:**

```
x(T) = 0.0000    v(T) = 6.0000
```

> "Este último caso tiene la particularidad de que existe un punto donde ambas poblaciones podrían coexistir en equilibrio (aproximadamente `(2.56, 3.44)`). Pero ese punto es **inestable**: cualquier desviación lo aleja para uno u otro lado, como una bola encima de una loma.
>
> Con las condiciones iniciales `(75, 20)`, la simulación termina exactamente en `(0, 6)`: los compradores se extinguen y los vendedores se estabilizan. El sistema **no se queda** en el punto inestable, sino que cae al equilibrio estable más cercano.
>
> Usamos un intervalo más largo (`t = 0` a `500`) con paso `0.1`, porque queremos darle tiempo al sistema para mostrar el comportamiento de largo plazo.
>
> Idea importante: que un sistema **pueda** tener equilibrio en el papel no quiere decir que la realidad se quede ahí. Las condiciones iniciales **deciden** hacia cuál de los finales posibles cae todo."

---

# Resumen final: ¿qué método se usó y cuándo?

| Situación                                       | Herramienta del taller                          | Archivo            |
|-------------------------------------------------|--------------------------------------------------|---------------------|
| Visualizar datos antes de modelar              | Gráficas y `escalas`                             | `modelos.py`        |
| Pasar exactamente por todos los puntos          | `lagrange` (Lagrange)                            | `modelos.py`        |
| Ajustar tendencia con potencia                  | `minimos_cuadrados` en log-log                   | `modelos.py`        |
| Comparar calidad de ajustes                     | `coeficiente_determinacion` (R²)                 | `modelos.py`        |
| Encontrar la raíz de una ecuación               | `Biseccion`                                      | `Ceros.py`          |
| Resolver una EDO de primer orden                | `Euler` (rápido, orden 1) y `Rk4` (más preciso)  | `ecuaciones.py`     |

---

# Frases listas para defender el taller

1. **"Primero graficamos"** — siempre que se trabaja con datos, la primera lección de análisis numérico es mirarlos antes de ajustar.
2. **"Probamos dos filosofías"** — pasar por todos los puntos (Lagrange) vs capturar la tendencia (mínimos cuadrados). Cada una tiene su cuándo.
3. **"Linealizamos con logaritmo"** — para llevar una potencia a una recta y poder aplicar mínimos cuadrados.
4. **"Comparamos con R²"** — para elegir con número, no a ojo.
5. **"Extrapolar es arriesgado"** — Lagrange explota fuera del rango; los modelos de tendencia se comportan mejor.
6. **"Convertimos la EDO a sistema de primer orden"** — porque los integradores trabajan con vectores de estado, no con derivadas sueltas.
7. **"Euler es O(h), RK4 es de orden superior"** — al duplicar `n`, el error de Euler se parte a la mitad; RK4 baja más rápido aún.
8. **"Dos fases en el cangrejo"** — porque un solo modelo mezcla biologías distintas.
9. **"En Lotka-Volterra, las condiciones iniciales deciden"** — el sistema puede tener varios equilibrios; el inicial nos lleva a uno.

---

*Documento de apoyo al Taller 2 — Análisis Numérico. Se debe leer junto con el notebook `Taller_2.ipynb`.*
