import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

f = lambda x: (x + np.sqrt(x)) * (20 - x + np.sqrt(20 -  x)) - 155.55

print("Biseccion")
Biseccion(f, 5, 7.5, 1e-4)

print("")
print("Posicion Falsa")
PosicionFalsa(f, 12.5, 15, 1e-10000)
print("")



ux =  np.linspace(-20, 20, 100)
plt.plot(ux, f(ux), 'b')
plt.axhline(y=0, color='red', linestyle='--')
plt.grid()

x = sp.symbols('x')

f = (x + np.sqrt(x)) * (20 - x + np.sqrt(20 -  x)) - 155.55


x_number = Newton(f, 6, 1e-4)
y_number = Newton(f, 7, 1e-4)

print(f'El numero es {x_number + y_number}')

f = lambda x: x**2-8

Secante(f, 2, 3, 1e-4)



x = sp.symbols('x')

f = x**2-8

Newton(f, 2, 1e-4)
