from pathlib import Path
import sys
# Agrega la raíz del proyecto al path de Python
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
'''
Ejercicio

Se sospecha que las grandes cantidades de tanino en las hojas maduras de los robles inhiben el crecimiento de la larva de 

polilla de invierno (Operophtera bromata L., Geometridae) que daña en exceso estos árboles en ciertos años. La siguiente tabla enumera el peso promedio de dos muestras de la larva en los primeros 28 días después de su nacimiento. Mientras la primera muestra se crió en las hojas jóvenes de roble, la segunda muestra se crió en las hojas maduras.



|	Día	|  	0	|	 6 	|	10	 |	13	|	17	|	20	|	28	|

|---------------|---------------|---------------|----------------|--------------|---------------|---------------|---------------|

|muestra 1 (mg) |	6.67	|	17.33	|	42.67    |	 37.33	|	30.10	|	29.31	|    28.74 	|

|muestra 2(mg)  |	6.67	|	16.11	|	18.89	 |	15.00	|	10.56	|9.44		|	8.89	|



1. Construir un polinomio para obtener la curva de peso promedio para cada muestra

2. Encuentre un peso promedio máximo aproximado para cada muestra( determinando el máximo del polinomio, usando un método de ceros de funciones)
'''
import numpy as np
import modelos as m
import Ceros as c

import matplotlib.pyplot as plt

dias = np.array([0, 6, 10, 13, 17, 20, 28], float)
peso_joven = np.array([6.67, 17.33, 42.67, 37.33, 30.10, 29.31, 28.74])
peso_maduro = np.array([6.67, 16.11, 18.89, 15.00, 10.56, 9.44, 8.89])

A = m.matriz(dias)
# eliminacion_DD_pivoteo solo triangula la matriz aumentada; no devuelve la solución del sistema
coef = np.linalg.solve(A, peso_joven)
coef_maduro = np.linalg.solve(A, peso_maduro)


def P(coef, x):
    x = np.asarray(x, dtype=float)
    return sum(coef[i] * (x ** i) for i in range(len(coef)))


def dP(coef, x):
    """Derivada del polinomio P respecto a x (coef[i] es el término en x^i)."""
    x = float(x)
    return sum(i * coef[i] * (x ** (i - 1)) for i in range(1, len(coef)))


def ceros_derivada_biseccion(coef, a, b, tol=1e-7):
    """Ceros de P' en [a, b] por bisección en subintervalos donde hay cambio de signo."""
    xs = np.linspace(a, b, 2501)
    raices = []
    for i in range(len(xs) - 1):
        fa, fb = dP(coef, xs[i]), dP(coef, xs[i + 1])
        if fa == 0:
            raices.append(xs[i])
        elif fa * fb < 0:
            z = c.Biseccion(lambda t: dP(coef, t), xs[i], xs[i + 1], tol)
            raices.append(z)
    # sin duplicados cercanos
    raices = sorted(set(round(r, 8) for r in raices))
    return raices


def peso_maximo_intervalo(coef, a, b):
    """Máximo de P en [a, b]: candidatos = extremos + puntos críticos (P' = 0) en el interior."""
    criticos = ceros_derivada_biseccion(coef, a, b)
    candidatos = [a, b] + [x for x in criticos if a < x < b]
    valores = [P(coef, x) for x in candidatos]
    k = int(np.argmax(valores))
    return candidatos[k], valores[k]


u_dias = np.linspace(min(dias), max(dias), 500)
P_joven = lambda x: P(coef, x)
P_maduro = lambda x: P(coef_maduro, x)

plt.plot(dias, peso_joven, 'gp', label='Larvas jovenes (datos)')
plt.plot(u_dias, P_joven(u_dias), 'b', label='Polinomio muestra 1')
plt.plot(dias, peso_maduro, 'or', label='Larvas maduras (datos)')
plt.plot(u_dias, P_maduro(u_dias), 'r', label='Polinomio muestra 2')
plt.xlabel('Día')
plt.ylabel('Peso (mg)')
plt.legend()
plt.grid()
plt.show()

x_max_j, w_max_j = peso_maximo_intervalo(coef, float(min(dias)), float(max(dias)))
x_max_m, w_max_m = peso_maximo_intervalo(coef_maduro, float(min(dias)), float(max(dias)))

print(f'Peso maximo aproximado (muestra 1, hojas jovenes): {w_max_j:.4f} mg en dia x ~ {x_max_j:.4f}')
print(f'Peso maximo aproximado (muestra 2, hojas maduras): {w_max_m:.4f} mg en dia x ~ {x_max_m:.4f}')
