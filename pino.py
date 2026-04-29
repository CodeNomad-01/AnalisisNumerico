# Ejercicio 3

# En los siguientes datos, X representa el diámetro de un pino, e Y es una medida de volumen-número de pies tablares dividido por 10. 


# |x   |   17 |   19 |   20 |   22 |   23 |   25 |   31 |   32 |   33 |   36  |   37   |   38   |   39|    41|
# |----|------|------|------|------|------|------|------|------|------|-------|--------|--------|-----|------|
# |y   | 19   | 25   | 32   | 51   | 57   | 71   | 141  | 123  | 187  | 192   | 205    | 252    | 248 | 294  |

# 1. Hacer un diagrama de  los datos observados. 
# 2. Construir un polinomio de máximo grado  y  úselo para aproximar  P(18)  y  P(28)  y que puede concluir o interpretar
# 3.Construir un modelo lineal usando minimos cuadrados y aproxime   P(18)  y  P(28)  y que puede concluir o interpretar
# 4. Qué puede decir de los dos modelos?

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import modelos as m

x = sp.symbols('x')
x_data = np.array([17, 19, 20, 22, 23, 25, 31, 32, 33, 36, 37, 38, 39, 41])
y_data = np.array([19, 25, 32, 51, 57, 71, 141, 123, 187, 192, 205, 252, 248, 294])
x_values = np.linspace(min(x_data), max(x_data), 200)
plt.plot(x_data, y_data, 'pr', label='datos observados')
plt.legend()
plt.xlabel('Diametro')
plt.ylabel('Volumen')
plt.grid()
plt.show()

P = m.lagrange(x_data, y_data)
P = sp.lambdify(x, P)
print(P(18))
print(P(28))

x_values = np.linspace(min(x_data), max(x_data), 200)
plt.plot(x_data, y_data, 'pr', label='datos observados')
plt.plot(x_values, P(x_values), 'g', label='Polinomio de Lagrange')
plt.legend()
plt.xlabel('Diametro')
plt.ylabel('Volumen')
plt.grid()
plt.show()


m, b = m.minimos_cuadrados(x_data, y_data)
print(m, b)

P = lambda x: m*x + b
x_values = np.linspace(min(x_data), max(x_data), 200)
plt.plot(x_data, y_data, 'pr', label='datos observados')
plt.plot(x_values, P(x_values), 'g', label='MC')
plt.legend()
plt.grid()
plt.show()