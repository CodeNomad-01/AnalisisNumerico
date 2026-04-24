import sympy as sp
from math import factorial

x=sp.symbols('x')

def Taylor (f, x0, n):
  polinomio = 0

  for k in range(n+1):
    df = sp.diff(f, x, k)
    df_val = sp.lambdify(x, df)
    polinomio += (df_val(x0)/factorial(k))*(x-x0)**k
  return polinomio

Taylor(sp.atan(x), 0, 5)
