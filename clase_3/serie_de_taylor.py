import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt
from math import factorial

f = lambda x: np.arctan(x) # usando numpy arctan tan inversa

p = lambda x: x

values = [1, 5]

def evaluacion(values, f, p):
  lista = []
  for i in values:
    lista.append([i,f(i), p(i), abs(f(i) - p(i)), abs((f(i)-p(i))/f(i))])

  lista = pd.DataFrame(lista, columns=["values_x", "f(x)", "p(x)", "|f(x)-p(x)| ", "E_r"])

  return lista

evaluacion(values, f, p)




delta = 2
x0 = 0
ux = np.linspace(x0-delta, x0+delta, 100)
plt.plot(ux, f(ux),  'b', label='$F(x) = \tan^{-1}x$')
plt.plot(ux, p(ux),  'r', label='$P(x) =  x$')
plt.legend()
plt.grid()
plt.xlabel('Eje X')
plt.xlabel('Eje y')

x = sp.symbols('x')

F = sp.atan(x)
y_prime = sp.diff(F, x)
y_double_prime = sp.diff(F, x, 2)

df_val = sp.lambdify(x, y_double_prime)

print(df_val(0))

y_prime
y_double_prime


f = lambda x: np.arctan(x) # usando numpy arctan tan inversa

p = lambda x: x-2/factorial(3)*x**3+24/factorial(5)*x**5

values = [1, 3.5, 5]

evaluacion(values, f, p)

delta = 2
x0 = 0
ux = np.linspace(x0-delta, x0+delta, 100)
plt.plot(ux, f(ux),  'b', label='$F(x) = \tan^{-1}x$')
plt.plot(ux, p(ux),  'r', label='$P(x) =  x$')
plt.legend()
plt.grid()
plt.xlabel('Eje X')
plt.xlabel('Eje y')
