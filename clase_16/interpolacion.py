import numpy as np
import matplotlib.pyplot as plt


x_h = np.array([0, 1.525, 3.050 , 4.575, 6.10, 7.625, 9.150])
y_h = np.array([1, 0.86117, 0.7385, 0.6292, 0.5327, 0.4481, 0.3741])

def minimos_cuadrados(x_data, y_data):
    n = len(x_data)
    Sx = sum(x_data)
    Sy = sum(y_data)
    Sxy = sum(x_data * y_data)
    Sx2 = sum(x_data ** 2)
    m = (n * Sxy - Sx * Sy) / (n * Sx2 - Sx ** 2)
    b = (Sy - m * Sx) / n
    return m, b

m, b = minimos_cuadrados(x_h, y_h)
print(f"m: {m}, b: {b}")

P = lambda x: m * x + b

x_values = np.linspace(min(x_h), max(x_h), 10)

plt.plot(x_h, y_h, 'gd', label='Datos Observados')
plt.plot(x_values, P(x_values), 'k', label='Minimos cuadrados')
plt.legend()
plt.grid()
plt.show()