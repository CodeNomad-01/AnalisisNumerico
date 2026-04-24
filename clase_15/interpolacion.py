import numpy as np
import sympy as sp

x = sp.symbols('x')

x_data = np.array([0, 0.6, 0.9])
y_data = np.array([1.000, 1.264911, 1.378404])

def lagrange(x_data, y_data):
    sumPolinomio = 0
    for i in range(len(x_data)):
        Li = 1
        for j in range(len(x_data)):
            if j != i:
                Li *= (x - x_data[j]) / (x_data[i] - x_data[j])
        sumPolinomio += Li * y_data[i]
    return sumPolinomio

P = lagrange(x_data, y_data)
print(P)
# print(P.evalf(subs = {x:0.45}))

