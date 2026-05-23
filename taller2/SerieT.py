import sympy as sp
import pandas as pd
from math import factorial

x = sp.symbols('x')


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
