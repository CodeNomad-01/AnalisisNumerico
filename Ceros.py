import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt
from math import factorial


def Biseccion(f, a, b, tol):
  if (f(a) * f(b) > 0):
    print("bye bye, no hay nada en el intervalo")
  else:
    contador = 0

    while (abs(b - a) > tol):
      p = (a + b) / 2
      contador += 1

      if contador > 100:
        break

      if f(a) * f(p) < 0:
        b = p
      else:
        a = p

    print(f'La solucion de al funcion: {p}')
    print(f'La cantidad de iteraciones necesarias fueron {contador}')

  return p


def PosicionFalsa(f, a, b, tol):
  if (f(a) * f(b) > 0):
    print("bye bye, no hay nada en el intervalo")
  else:
    contador = 0
    p = b - f(b) * (a-b) / (f(a) - f(b))
    while (abs(f(p)) > tol):
      p = b - f(b) * (a-b) / (f(a) - f(b))
      contador += 1

      if contador > 1000:
        break

      if f(a) * f(p) < 0:
        b = p
      else:
        a = p

    print(f'La solucion de al funcion: {p}')
    print(f'La cantidad de iteraciones necesarias fueron {contador}')

  return p


def evaluacion(values, f, p):
  lista = []
  for i in values:
    lista.append([i,f(i), p(i), abs(f(i) - p(i)), abs((f(i)-p(i))/f(i))])

  lista = pd.DataFrame(lista, columns=["values_x", "f(x)", "p(x)", "|f(x)-p(x)| ", "E_r"])

  return lista


def Taylor (f, x0, n):
  polinomio = 0

  for k in range(n+1):
    df = sp.diff(f, x, k)
    df_val = sp.lambdify(x, df)
    polinomio += (df_val(x0)/factorial(k))*(x-x0)**k
  return polinomio


def Newton(f, x0, tol):
  x = sp.symbols('x')
  df = sp.diff(f, x)
  newton = x-f/df
  contador = 0
  error = float('inf')
  while error > tol and contador < 20:
    x1 = newton.subs(x, x0)
    error = abs(x1-x0)
    x0 = x1
    contador += 1
  return float(x1), contador


def Secante(f, x0, x1, tol):
    error = 1
    contador = 0
    while error > tol:
      x2 = x1 - (f(x1) * (x1-x0)) / (f(x1) - f(x0))
      error = abs(x2-x1)
      x0 = x1
      x1 = x2
      contador += 1
    return x2, contador