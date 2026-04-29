import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import modelos as ml

x = sp.symbols('x')

t_data = np.array([1814, 1824, 1834, 1844, 1854, 1864], float)
P_data = np.array([125, 275, 830, 1200, 1750, 1650], float)

x_values = np.linspace(min(t_data), max(t_data), 200)

# a) Polinomio de Lagrange
P = ml.lagrange(t_data, P_data)
print(f'El polinomio de Lagrange es: {P}')
P = sp.lambdify(x, P)

# b) Estimaciones
print(f'La poblacion estimada en 1858 es: {P(1858)}')
print(f'La poblacion estimada en 1817 es: {P(1817)}')

# c) Grafica solo datos observados
plt.plot(t_data, P_data, 'pr', label='datos observados')
plt.legend()
plt.xlabel('Año')
plt.ylabel('Poblacion')
plt.grid()
plt.show()

# d) Grafica simultanea datos observados y polinomio de Lagrange
plt.plot(t_data, P_data, 'pr', label='datos observados')
plt.plot(x_values, [P(t) for t in x_values], 'g', label='Polinomio de Lagrange')
plt.legend()
plt.xlabel('Año')
plt.ylabel('Poblacion')
plt.grid()
plt.show()
