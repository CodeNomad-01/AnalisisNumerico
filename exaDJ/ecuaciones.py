import numpy as np


def Euler(f, a, b, h, c_inicial):
    yeu = [c_inicial]
    n = int((b - a) / h)
    for i in range(n):
        yeu.append(yeu[i] + h * f(a + i*h, yeu[i]))
    return np.linspace(a, b, n+1), yeu
